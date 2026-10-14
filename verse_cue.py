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
import unicodedata
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
DEFAULT_ALIASES = Path(__file__).with_name("aliases.json")
WORD_RE = re.compile(r"[^a-z']+")
QUOTES = str.maketrans("\u2018\u2019\u02bc", "'''")  # curly apostrophes -> plain '
# One folding for slide and heard text: plain apostrophes, accents stripped, ASCII lowercase.
fold = lambda text: unicodedata.normalize("NFKD", text.translate(QUOTES)).encode("ascii", "ignore").decode().lower()  # noqa: E731


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
    """Slide text -> lowercase words of letters and apostrophes; empties dropped. Same fold() as transcribe()."""
    return [w for w in WORD_RE.sub(" ", fold(text)).split() if w.strip("'")]


def lan_ip() -> str:
    """This machine's LAN address, for the setup printout. 127.0.0.1 if we cannot tell."""
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("1.1.1.1", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def _alias_file(path: Path) -> Path:
    """CWD aliases.json, else the copy shipped next to this module."""
    return DEFAULT_ALIASES if path == ALIASES and not path.exists() else path


def load_aliases(path: Path = ALIASES) -> dict[str, str]:
    """Invert {canonical: {alias: count}} into {alias: canonical}; highest count wins; canonicals stay."""
    path = _alias_file(path)
    table = json.loads(path.read_text()) if path.exists() else {}
    best: dict[str, tuple[int, str]] = {}
    for canon, al in table.items():
        for alias, n in al.items():
            best[alias] = max(best.get(alias, (0, "")), (n, canon))
    return {alias: best[alias][1] for alias in best.keys() - table.keys()}


def canon(heard: list[tuple[float, str]], vocab: set[str], aliases: dict[str, str], cutoff: float) -> list:
    """Map heard words onto the slide vocabulary: slide words stay, then alias table, then difflib, else unchanged."""
    out = []
    for t, heard_word in heard:
        w = heard_word if heard_word in vocab else aliases.get(heard_word, heard_word)
        if w not in vocab:
            w = (get_close_matches(w, vocab, n=1, cutoff=cutoff) or [w])[0]
        out.append((t, w))
    return out


def align(slide_words: list[str], heard: list[tuple[float, str]]) -> list[tuple[int, float]]:
    """(slide index, capture time) for every heard word that lines up with the slide, in slide order."""
    matcher = SequenceMatcher(None, slide_words, [w for _, w in heard], autojunk=False)
    return [(i + k, heard[j + k][0]) for i, j, n in matcher.get_matching_blocks() for k in range(n)]


def predict(pairs: list[tuple[int, float]], n_words: int, d: dict) -> float | None:
    """Capture-clock time to fire: last-word start from singing rate, minus lead. None when evidence is thin."""
    if len(pairs) < min(d["min_matched"], math.ceil(n_words / 2)):
        return None
    need = n_words - d["tail_words"]
    if d.get("first_half", True):
        need = max(need, n_words // 2)
    if pairs[-1][0] < need:
        return None
    (i0, t0), (i1, t1) = pairs[0], pairs[-1]
    rate = (t1 - t0) / (i1 - i0) if i1 - i0 >= 2 else d["default_sec_per_word"]
    lo, hi = d["rate_bounds"]
    return t1 + (n_words - 1 - i1) * min(max(rate, lo), hi) - d["lead_s"]


@dataclass
class Slide:
    """Everything we know about the slide currently on screen. Reset whenever the uuid changes or we fire."""

    uuid: str = ""
    words: list[str] = field(default_factory=list)
    committed: list[tuple[float, str]] = field(default_factory=list)
    previous: list[tuple[float, str]] = field(default_factory=list)
    entered: float = 0.0
    predicted: float | None = None
    pairs: list[tuple[int, float]] = field(default_factory=list)
    any_match: bool = False
    raw: list[str] = field(default_factory=list)
    pressed: float | None = None  # our Next on this slide; the next slide dates from it, not from a lagging read
    changed: float | None = -math.inf  # last slide change (ours or the operator's); min_gap_s counts from it


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
    words = [(t_start + w.start, WORD_RE.sub("", fold(w.word))) for s in segments for w in s.words or []]
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

    def get(self, path: str) -> bytes:
        with urllib.request.urlopen(self.base + path, timeout=1) as response:
            return response.read()

    def slide(self) -> tuple[str, str] | None:
        """(uuid, text). ('', '') when nothing is showing; None when unreachable, so a stale value never fires."""
        try:
            current = json.loads(self.get("/status/slide"))["current"] or {"uuid": "", "text": ""}
            return current["uuid"], current["text"]
        except (OSError, ValueError, KeyError):
            print(f"verse-cue: ProPresenter unreachable at {self.base}", file=sys.stderr)
            return None

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
    """Blank slide: advance on the first voice after settling, or on a cue held for the gap. No slide: never."""
    if not slide.uuid:
        return None
    settled = t_end - slide.entered >= blank["blank_settle_s"]
    return t_end if slide.predicted is not None or (settled and speech_in(chunk, blank)) else None


def decide(slide: Slide, predicted: float | None, now: float, hop_s: float) -> float | None:
    """Keep the newest estimate; fire when it lands before the next tick would."""
    if predicted is not None:
        slide.predicted = predicted
    if slide.predicted is None or slide.predicted > now + hop_s:
        return None
    return max(slide.predicted, now)


def overdue(slide: Slide, d: dict, now: float) -> float | None:
    """Late salvage: click now if we ever matched and the slide has lasted a full reading."""
    if not d.get("deadline_fire") or not slide.any_match:
        return None
    rate = d.get("deadline_sec_per_word", d["default_sec_per_word"])
    if now - slide.entered < len(slide.words) * rate:
        return None
    return now


def lyric_tick(slide: Slide, ring: deque, t_end: float, model, cfg: dict) -> tuple[float | None, float]:
    """Transcribe the window, align to the slide, return (time to fire or None, now after inference)."""
    audio = np.concatenate(ring)
    start = t_end - len(audio) / SR
    latest, infer = transcribe(model, audio, start, cfg["model"], " ".join(slide.words))
    slide.raw = [w for _, w in latest]
    d = cfg["decide"]
    heard = merge(slide, latest, start, slide.entered + d["guard_s"])
    heard = canon(heard, set(slide.words), cfg["aliases"], d["fuzzy_cutoff"])
    slide.pairs = align(slide.words, heard)
    slide.any_match = slide.any_match or bool(slide.pairs)
    now = t_end + infer
    at = decide(slide, predict(slide.pairs, len(slide.words), d), now, cfg["model"]["hop_s"]) or overdue(slide, d, now)
    return at, now


def paint(words: list[str], matched: set[int], cue: set[int]) -> str:
    """Dim unmatched, green heard-on-slide, yellow tail matches that can arm Next."""
    parts = []
    for i, w in enumerate(words):
        code = "\033[33m" if i in cue else "\033[32m" if i in matched else "\033[2m"
        parts.append(f"{code}{w}\033[0m")
    return " ".join(parts)


def cue_set(n: int, matched: set[int], *, tail: int, first_half: bool) -> set[int]:
    """Slide indexes that are both matched and far enough along to arm a click."""
    need = n - tail
    if first_half:
        need = max(need, n // 2)
    return {i for i in matched if i >= need}


def show(slide: Slide, d: dict, file=sys.stderr) -> None:
    """One hop: raw Whisper line, then the current ProPresenter slide with cue colors."""
    if file is None:
        return
    matched = {i for i, _ in slide.pairs}
    cues = cue_set(len(slide.words), matched, tail=d["tail_words"], first_half=d.get("first_half", True))
    print(f"heard  {' '.join(slide.raw) or '…'}", file=file)
    print(f"slide  {paint(slide.words, matched, cues) or '(blank)'}", file=file)


def fire(pp, slide: Slide, cue: tuple[float, float], wait, cfg: dict) -> Slide:
    """Advance at cue = (fire time, now) unless the slide changed (or cannot be read) by the time we would press Next.

    A fire within min_gap_s of the last change waits for the gap to end; when that is more than
    one hop away, the cue is held on the slide and the loop retries it on a later tick.
    After a press, start the slide fresh from the fire time: the next slide may share this uuid
    or the status may lag, and neither may fire again on the evidence that just fired. A blank
    slide has no evidence to reset, so its settle starts only after the status lag has passed.
    """
    at, now = cue
    gap_end = slide.changed + cfg["decide"].get("min_gap_s", 2.0)
    if gap_end > now + cfg["model"]["hop_s"]:
        slide.predicted = at
        return slide
    at = max(at, gap_end)
    wait(at)
    read = pp.slide()
    if read is None or (read[0], tokens(read[1])) != (slide.uuid, slide.words):
        return slide
    pp.next(at)
    log_metrics(slide, at, cfg)
    lag = 0 if slide.words else max(cfg["blank"]["blank_settle_s"], 2 * cfg["model"]["hop_s"])
    return Slide(slide.uuid, slide.words, entered=at + lag, pressed=at, changed=at)


def entered_at(slide: Slide, t_end: float, hop_s: float) -> float:
    """When the newly read slide began: our press if the status is still lagging behind it, else now."""
    ours = slide.pressed is not None and t_end - slide.pressed <= 3 * hop_s
    return slide.pressed if ours else t_end


def track(pp, slide: Slide, t_end: float, cfg: dict) -> Slide | None:
    """This tick's slide: fresh when the uuid or text changed, None when the status read failed (stale, never fire)."""
    read = pp.slide()
    if read is None:
        return None
    words = tokens(read[1])
    if slide.changed is None or (read[0], words) != (slide.uuid, slide.words):
        entered = entered_at(slide, t_end, cfg["model"]["hop_s"])
        # the first slide seen at startup is not a change
        changed = -math.inf if slide.changed is None else entered
        slide = Slide(read[0], words, entered=entered, changed=changed)
        log_metrics(slide, None, cfg)
    return slide


def run(frames, pp, model, cfg: dict, wait=sleep_until) -> None:
    """The loop. frames yields (t_end, hop-sized float32 chunk); pp has .slide() (None = unreadable) and .next(at)."""
    m = cfg["model"]
    ring: deque = deque(maxlen=round(m["window_s"] / m["hop_s"]))
    slide = Slide(changed=None)  # nothing read yet: the first read is always a new slide
    for t_end, chunk in frames:
        ring.append(chunk)
        current = track(pp, slide, t_end, cfg)
        if current is None:  # skip this tick; the cue keeps its prediction and retries next hop
            continue
        slide = current
        cue = (
            (blank_tick(slide, chunk, t_end, cfg["blank"]), t_end)
            if not slide.words
            else lyric_tick(slide, ring, t_end, model, cfg)
        )
        show(slide, cfg["decide"], cfg.get("display", sys.stderr))
        if cue[0] is not None:
            slide = fire(pp, slide, cue, wait, cfg)


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


def pick_input() -> str:
    """Numbered list of capture devices; return the name the operator typed."""
    import sounddevice as sd

    inputs = [(i, d["name"]) for i, d in enumerate(sd.query_devices()) if d["max_input_channels"] > 0]
    for i, name in inputs:
        print(f"{i}: {name}")
    return dict(inputs)[int(input("Input device number: "))]


def setup(path: Path = CONFIG) -> None:
    """Interactive: pick the vocal input and ProPresenter host/port; print how to connect."""
    device = pick_input()
    host = input("ProPresenter IP [127.0.0.1]: ").strip() or "127.0.0.1"
    port = int(input("ProPresenter port [1025]: ").strip() or "1025")
    text = path.read_text()
    text = re.sub(r"(?m)^device = .*$", f'device = "{device}"', text)
    text = re.sub(r"(?m)^host = .*$", f'host = "{host}"', text)
    text = re.sub(r"(?m)^port = .*$", f"port = {port}", text)
    path.write_text(text)
    print(f"verse-cue will connect to ProPresenter at {host}:{port}")
    print(f"This computer's IP: {lan_ip()}")
    print(f"On ProPresenter: Preferences -> Network -> enable Network API, port {port}")
    print("device:", device, "| model:", load_config(path)["model"]["name"])


def main(argv: list[str] | None = None) -> None:
    """`verse-cue` runs the loop; `verse-cue --setup` writes the config."""
    args = sys.argv[1:] if argv is None else argv
    if not CONFIG.exists():
        CONFIG.write_text(DEFAULT_CONFIG.read_text())
    for flag, fn in (
        ("--setup", setup),
        ("--help", lambda: print("verse-cue [--setup]  auto-advance ProPresenter lyric slides from a vocal feed")),
        ("-h", lambda: print("verse-cue [--setup]  auto-advance ProPresenter lyric slides from a vocal feed")),
    ):
        if flag not in args:
            continue
        fn()
        return
    cfg = load_config()
    cfg["aliases"] = load_aliases()
    pp = ProPresenter(cfg["propresenter"]["host"], cfg["propresenter"]["port"])
    run(mic_frames(cfg["audio"]["device"], cfg["model"]["hop_s"]), pp, load_model(cfg), cfg)


if __name__ == "__main__":
    main()
