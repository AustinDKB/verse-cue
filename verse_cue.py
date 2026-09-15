"""verse-cue: auto-advance ProPresenter lyric slides from a live vocal feed.

One loop: listen -> transcribe the last few seconds -> align the words to the current
slide's text -> predict when the last word starts -> trigger the next slide a little early.
"""

from __future__ import annotations

import json
import math
import queue
import re
import subprocess
import sys
import time
import tomllib
import urllib.request
from collections import deque
from dataclasses import dataclass, field
from difflib import SequenceMatcher, get_close_matches
from pathlib import Path

import numpy as np

SR = 16000
CONFIG = Path("verse-cue.toml")
AUTO = Path("verse-cue.auto.toml")
ALIASES = Path("aliases.json")
METRICS = Path("metrics.jsonl")
DEFAULT_CONFIG = Path(__file__).with_name("verse-cue.toml")
WORD_RE = re.compile(r"[^a-z']+")


def load_config(path: Path = CONFIG, auto: Path = AUTO) -> dict:
    """Read the TOML (bundled default when absent); verse-cue.auto.toml overrides [model]."""
    cfg = tomllib.loads((path if path.exists() else DEFAULT_CONFIG).read_text())
    if auto.exists():
        cfg["model"].update(tomllib.loads(auto.read_text())["model"])
    return cfg


def gpu_gb() -> float:
    """Total VRAM in GB via nvidia-smi, 0.0 when there is no NVIDIA GPU."""
    cmd = ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=5, check=True).stdout
        return int(out.split()[0]) / 1024
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return 0.0


def pick_model(hw: dict, gb: float) -> tuple[str, str]:
    """(model name, compute_type) from the [hardware] table: first GPU row whose threshold fits, else CPU."""
    for threshold, name, compute_type in hw["gpu"]:
        if gb and gb >= threshold:
            return name, compute_type
    return tuple(hw["cpu"])


def load_model(cfg: dict):
    """faster-whisper model from [model], or from the hardware table when name is empty."""
    from faster_whisper import WhisperModel

    m = cfg["model"]
    name, compute_type = (m["name"], m["compute_type"]) if m["name"] else pick_model(cfg["hardware"], gpu_gb())
    return WhisperModel(name, device="auto", compute_type=compute_type)


def tokens(text: str) -> list[str]:
    """Slide text -> lowercase words of letters and apostrophes; empties dropped."""
    return [w for w in WORD_RE.sub(" ", text.lower()).split() if w.strip("'")]


def load_aliases(path: Path = ALIASES) -> dict[str, str]:
    """Invert {canonical: {alias: count}} into {alias: canonical}; highest count wins; canonicals stay."""
    table = json.loads(path.read_text()) if path.exists() else {}
    best: dict[str, tuple[int, str]] = {}
    for canon, al in table.items():
        for alias, n in al.items():
            best[alias] = max(best.get(alias, (0, "")), (n, canon))
    return {alias: best[alias][1] for alias in best.keys() - table.keys()}


def canon(heard: list[tuple[float, str]], vocab: set[str], aliases: dict[str, str], cutoff: float) -> list:
    """Map heard words onto the slide vocabulary: alias table first, then difflib, else unchanged."""
    out = []
    for t, heard_word in heard:
        w = aliases.get(heard_word, heard_word)
        if w not in vocab:
            w = (get_close_matches(w, vocab, n=1, cutoff=cutoff) or [w])[0]
        out.append((t, w))
    return out


def align(slide_words: list[str], heard: list[tuple[float, str]]) -> list[tuple[int, float]]:
    """(slide index, capture time) for every heard word that lines up with the slide, in slide order."""
    matcher = SequenceMatcher(None, slide_words, [w for _, w in heard], autojunk=False)
    return [(i + k, heard[j + k][0]) for i, j, n in matcher.get_matching_blocks() for k in range(n)]


def predict(pairs: list[tuple[int, float]], n_words: int, d: dict) -> float | None:
    """Capture-clock time to fire: predicted start of the last word minus lead. None when evidence is thin."""
    if len(pairs) < min(d["min_matched"], math.ceil(n_words / 2)):
        return None
    (i0, t0), (i1, t1) = pairs[0], pairs[-1]
    rate = (t1 - t0) / (i1 - i0) if i1 - i0 >= 2 else d["default_sec_per_word"]
    lo, hi = d["rate_bounds"]
    return t1 + (n_words - 1 - i1) * min(max(rate, lo), hi) - d["lead_s"]


@dataclass
class Slide:
    """Everything we know about the slide currently on screen. Reset whenever the uuid changes."""

    uuid: str = ""
    words: list[str] = field(default_factory=list)
    committed: list[tuple[float, str]] = field(default_factory=list)
    previous: list[tuple[float, str]] = field(default_factory=list)
    entered: float = 0.0
    predicted: float | None = None
    pairs: list[tuple[int, float]] = field(default_factory=list)


def transcribe(model, audio: np.ndarray, t_start: float, m: dict, prompt: str) -> tuple[list, float]:
    """One window -> [(capture-clock word start, normalized word)], inference seconds."""
    kw = {"slide": {"initial_prompt": prompt}, "hotwords": {"hotwords": prompt}}.get(m["prompt_mode"], {})
    t0 = time.monotonic()
    segments, _ = model.transcribe(
        audio,
        language="en",
        beam_size=m["beam_size"],
        temperature=m.get("temperature", 0.0),
        word_timestamps=True,
        condition_on_previous_text=False,
        vad_filter=False,
        **kw,
    )
    words = [(t_start + w.start, WORD_RE.sub("", w.word.lower())) for s in segments for w in s.words or []]
    return words, time.monotonic() - t0


def merge(slide: Slide, latest: list, window_start: float, guard_until: float) -> list[tuple[float, str]]:
    """Commit previous-window words that fell out of the window; the latest window wins for its own region."""
    slide.committed += [w for w in slide.previous if w[0] < window_start]
    slide.previous = latest
    return [w for w in slide.committed + latest if w[0] >= guard_until]


def speech_in(chunk: np.ndarray, blank: dict) -> bool:
    """Silero VAD (bundled with faster-whisper): is there voice in this hop?"""
    from faster_whisper.vad import VadOptions, get_speech_timestamps

    opts = VadOptions(min_speech_duration_ms=blank["min_speech_ms"])
    return bool(get_speech_timestamps(chunk, opts, sampling_rate=SR))


class ProPresenter:
    """Two endpoints: read the current slide, trigger the next one. Never raises into the loop."""

    def __init__(self, host: str, port: int) -> None:
        self.base = f"http://{host}:{port}/v1"
        self.last: tuple[str, str] = ("", "")

    def get(self, path: str) -> bytes:
        with urllib.request.urlopen(self.base + path, timeout=1) as response:
            return response.read()

    def slide(self) -> tuple[str, str]:
        """(uuid, text). ('', '') when nothing is showing; last known value when unreachable."""
        try:
            current = json.loads(self.get("/status/slide"))["current"] or {"uuid": "", "text": ""}
            self.last = (current["uuid"], current["text"])
        except (OSError, ValueError, KeyError):
            print(f"verse-cue: ProPresenter unreachable at {self.base}", file=sys.stderr)
        return self.last

    def next(self, at: float) -> None:  # noqa: ARG002 - `at` is recorded by the bench fake, ignored live
        try:
            self.get("/trigger/next")
        except OSError:
            print("verse-cue: trigger failed", file=sys.stderr)


def sleep_until(t: float) -> None:
    time.sleep(max(0.0, t - time.monotonic()))


def log_metrics(slide: Slide, at: float | None, cfg: dict) -> None:
    """One JSON line per slide entered and per fire; operator overrides are derived offline from the gaps."""
    row = {
        "ts": time.time(),
        "event": "enter" if at is None else "fire",
        "uuid": slide.uuid,
        "n_words": len(slide.words),
        "matched": len(slide.pairs),
        "idx_from_end": len(slide.words) - 1 - slide.pairs[-1][0] if slide.pairs else None,
        "predicted": slide.predicted,
        "entered": slide.entered,
        "fired_at": at,
        "blank": not slide.words,
        **{k: cfg["model"][k] for k in ("name", "window_s", "hop_s", "prompt_mode")},
    }
    with Path(cfg.get("metrics_file", METRICS)).open("a") as f:
        f.write(json.dumps(row) + "\n")


def blank_tick(slide: Slide, chunk: np.ndarray, t_end: float, blank: dict) -> float | None:
    """Blank slide: advance on the first voice after the settle period. No slide at all: never."""
    if not slide.uuid:
        return None
    settled = t_end - slide.entered >= blank["blank_settle_s"]
    return t_end if settled and speech_in(chunk, blank) else None


def decide(slide: Slide, predicted: float | None, now: float, hop_s: float) -> float | None:
    """Keep the newest estimate; fire when it lands before the next tick would."""
    if predicted is not None:
        slide.predicted = predicted
    if slide.predicted is None or slide.predicted > now + hop_s:
        return None
    return max(slide.predicted, now)


def lyric_tick(slide: Slide, ring: deque, t_end: float, model, cfg: dict) -> float | None:
    """Transcribe the window, align to the slide, return the time to fire or None."""
    audio = np.concatenate(ring)
    start = t_end - len(audio) / SR
    latest, infer = transcribe(model, audio, start, cfg["model"], " ".join(slide.words))
    d = cfg["decide"]
    heard = merge(slide, latest, start, slide.entered + d["guard_s"])
    heard = canon(heard, set(slide.words), cfg["aliases"], d["fuzzy_cutoff"])
    slide.pairs = align(slide.words, heard)
    return decide(slide, predict(slide.pairs, len(slide.words), d), t_end + infer, cfg["model"]["hop_s"])


def fire(pp, slide: Slide, at: float, wait, cfg: dict) -> None:
    """Advance, unless the slide changed while we were transcribing."""
    if pp.slide()[0] != slide.uuid:
        return
    wait(at)
    pp.next(at)
    log_metrics(slide, at, cfg)


def run(frames, pp, model, cfg: dict, wait=sleep_until) -> None:
    """The loop. frames yields (t_end, hop-sized float32 chunk); pp has .slide() and .next(at)."""
    m = cfg["model"]
    ring: deque = deque(maxlen=round(m["window_s"] / m["hop_s"]))
    slide = Slide()
    for t_end, chunk in frames:
        ring.append(chunk)
        uuid, text = pp.slide()
        if uuid != slide.uuid:
            slide = Slide(uuid, tokens(text), entered=t_end)
            log_metrics(slide, None, cfg)
        at = (
            blank_tick(slide, chunk, t_end, cfg["blank"])
            if not slide.words
            else lyric_tick(slide, ring, t_end, model, cfg)
        )
        if at is not None:
            fire(pp, slide, at, wait, cfg)


def mic_frames(device: str, hop_s: float):  # pragma: no cover - needs audio hardware
    """Yield (capture time, hop-sized mono float32 chunk) from the configured input device."""
    import sounddevice as sd

    q: queue.Queue = queue.Queue()

    def on_audio(data, _frames, _time, _status) -> None:
        q.put((time.monotonic(), data[:, 0].copy()))

    stream = sd.InputStream(
        device=device or None, samplerate=SR, channels=1, dtype="float32", blocksize=int(hop_s * SR), callback=on_audio
    )
    with stream:
        while True:
            yield q.get()


def setup(path: Path = CONFIG) -> None:
    """Interactive: pick the input device and ProPresenter port; rewrite those two lines in the TOML."""
    import sounddevice as sd

    inputs = [(i, d["name"]) for i, d in enumerate(sd.query_devices()) if d["max_input_channels"] > 0]
    for i, name in inputs:
        print(f"{i}: {name}")
    device = dict(inputs)[int(input("Input device number: "))]
    port = int(input("ProPresenter port [1025]: ").strip() or "1025")
    text = re.sub(r"(?m)^device = .*$", f'device = "{device}"', path.read_text())
    path.write_text(re.sub(r"(?m)^port = .*$", f"port = {port}", text))
    print("device:", device, "| port:", port, "| model:", pick_model(load_config(path)["hardware"], gpu_gb()))


def main(argv: list[str] | None = None) -> None:
    """`verse-cue` runs the loop; `verse-cue --setup` writes the config."""
    args = sys.argv[1:] if argv is None else argv
    if not CONFIG.exists():
        CONFIG.write_text(DEFAULT_CONFIG.read_text())
    if "--setup" in args:
        setup()
        return
    cfg = load_config()
    cfg["aliases"] = load_aliases()
    pp = ProPresenter(cfg["propresenter"]["host"], cfg["propresenter"]["port"])
    run(mic_frames(cfg["audio"]["device"], cfg["model"]["hop_s"]), pp, load_model(cfg), cfg)


if __name__ == "__main__":
    main()
