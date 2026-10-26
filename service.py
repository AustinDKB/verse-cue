"""Saved services: review, spoken commentary, replay. verse-cue-harvest review / comment / bench --service run these."""

from __future__ import annotations

import json
import math
import os
import time
import urllib.request
import uuid
import wave
from pathlib import Path

import numpy as np

import harvest as hv
import verse_cue as vc

REVERT_S = 5.0  # an operator step back this soon after our fire means the fire was early
THIN = 10  # fewer operator-changed slides than this is too little truth to score a service
STT_URL = "https://api.x.ai/v1/stt"
STT_MODEL = "grok-voice-transcribe-2.0"
STT_FIELDS = (("model", STT_MODEL), ("language", "en"), ("format", "true"))


def stepped_back(slides: list[dict], j: int) -> bool:
    """We advanced to slide j and the operator went back to j-1 within REVERT_S; later is a Next onto a repeat."""
    return (
        0 < j < len(slides) - 1
        and slides[j]["change"] == "ours"
        and slides[j + 1]["change"] == "operator"
        and slides[j + 1]["uuid"] == slides[j - 1]["uuid"]
        and slides[j + 1]["start"] - slides[j]["start"] <= REVERT_S
    )


def read_log(service: Path) -> list[dict]:
    return [json.loads(x) for x in (service / "slides.jsonl").read_text().splitlines() if x.strip()]


def start_time(service: Path, rows: list[dict]) -> float:
    """t0: meta.json's capture time of audio.wav's first sample, else the first enter."""
    meta = service / "meta.json"
    if meta.exists():
        return json.loads(meta.read_text())["t0"]
    return next((r["entered"] for r in rows if r["event"] == "enter"), 0.0)


def slides_from(rows: list[dict], t0: float) -> list[dict]:
    """One dict per enter row; a fire row sets fired on the slide it fired from."""
    slides: list[dict] = []
    last_fire = None
    for r in rows:
        if r["event"] == "enter":
            change = "ours" if r["entered"] == last_fire else "operator"
            keep = {
                "start": round(r["entered"] - t0, 2),
                "uuid": r["uuid"],
                "words": r.get("words"),
                "blank": r["blank"],
            }
            slides.append({**keep, "change": change, "fired": None, "early_reverted": False})
            last_fire = None
        elif slides:
            last_fire = r["fired_at"]
            slides[-1]["fired"] = round(last_fire - t0, 2)
    return slides


def service_slides(service: Path) -> list[dict]:
    """slides.jsonl -> one dict per slide: start and fired (audio s), words, change, early_reverted.

    A change is ours only when the slide entered at our press time (verse_cue.entered_at); a press that
    changed nothing leaves the next change to the operator.
    """
    rows = read_log(service)
    slides = slides_from(rows, start_time(service, rows))
    if slides:
        slides[0]["change"] = "start"
    # we advanced to j, the operator stepped straight back to j-1: that fire was early
    for j in range(1, len(slides) - 1):
        slides[j - 1]["early_reverted"] = stepped_back(slides, j)
    return slides


def mark_misses(slides: list[dict]) -> None:
    """miss = the operator made the next change; a slide we entered that the operator undid at once is not one."""
    nexts = [s["change"] for s in slides[1:]] + [None]
    undone = [False] + [s["early_reverted"] for s in slides[:-1]]
    for sl, nxt, back in zip(slides, nexts, undone, strict=False):
        sl["miss"] = nxt == "operator" and not back


def review_counts(slides: list[dict]) -> dict:
    return {
        "slide_changes": max(len(slides) - 1, 0),
        "ours": sum(s["change"] == "ours" for s in slides),
        "operator_overrides": sum(s["change"] == "operator" for s in slides),
        "misses": sum(s["miss"] for s in slides),
        "early_reverted": sum(s["early_reverted"] for s in slides),
    }


def review(service: Path) -> dict:
    """Mistakes from slides.jsonl alone: operator overrides, misses (we never fired), early fires reverted."""
    slides = service_slides(service)
    mark_misses(slides)
    out = {
        "service": service.name,
        "counts": review_counts(slides),
        "slides": [{k: v for k, v in s.items() if k != "words"} for s in slides],
    }
    (service / "review.json").write_text(json.dumps(out, indent=1))
    return out


def mistake(s: dict) -> str:
    """What went wrong on one reviewed slide; empty when nothing did."""
    if s["early_reverted"]:
        return "early fire reverted"
    return "missed" if s["miss"] else "operator override" if s["change"] == "operator" else ""


def print_review(r: dict) -> None:
    c = r["counts"]
    print(f"{r['service']}: {c['slide_changes']} slide changes")
    print(
        f"  ours {c['ours']} | operator overrides {c['operator_overrides']} | misses {c['misses']}"
        f" | early fires reverted {c['early_reverted']}"
    )
    bad = [(i, s, what) for i, s in enumerate(r["slides"]) if (what := mistake(s))]
    for i, s, what in bad[:20]:
        print(f"  slide {i} at {s['start']:.1f}s: {what}")
    if len(bad) > 20:
        print(f"  ... {len(bad) - 20} more in review.json")


def merged(slides: list[dict]) -> list[dict]:
    """Drop each fire the operator stepped back from within REVERT_S and the step back: one slide remains."""
    # slides[j]["early_reverted"] means slides j + 1 (our fire) and j + 2 (the step back) go
    back = [False, False] + [s["early_reverted"] for s in slides]
    return [s for s, two, one in zip(slides, back, back[1:], strict=False) if not (two or one)]


def replay(service: Path, slides: list[dict], model, cfg: dict) -> tuple[list[float], list[float]]:
    """Run audio.wav through verse_cue.run against these slides: (slide starts, fire per change, nan = missed)."""
    if any(s["words"] is None for s in slides):
        raise SystemExit(f"{service}: slides.jsonl has no slide text (saved by an older verse-cue); cannot replay")
    timeline = [(s["start"], " ".join(s["words"])) for s in slides]
    cell = [0.0]
    pp = hv.FakePP(timeline, lambda: cell[0])
    frames = hv.wav_frames(service / "audio.wav", cfg["model"]["hop_s"], cell)
    vc.run(frames, pp, model, {**cfg, "metrics_file": os.devnull}, wait=lambda _t: None)
    starts = [t for t, _ in timeline]
    return starts, (pp.fires + [math.nan] * len(starts))[: len(starts) - 1]


def bench_service(service: Path, model, cfg: dict) -> dict:
    """Replay audio.wav against the slides the live run saw. Truth = the operator's own slide changes only.

    Slides we advanced are replayed at our fire time but not scored: our own press is not ground truth.
    A fire the operator stepped back from within REVERT_S replays as one slide, true at the operator's next change.
    """
    slides = merged(service_slides(service))
    starts, fires = replay(service, slides, model, cfg)
    scored = [i for i in range(1, len(slides)) if slides[i]["change"] == "operator"]
    return {
        "deltas": [fires[i - 1] - starts[i] for i in scored],
        "lengths": [starts[i] - starts[i - 1] for i in scored],
        "operator_changes": len(scored),
    }


def print_bench(r: dict) -> None:
    if r["operator_changes"] < THIN:
        print(
            f"only {r['operator_changes']} operator-changed slides (< {THIN}): too thin to score;"
            " the replay inputs are audio.wav + slides.jsonl"
        )
    print(hv.summarize(r["deltas"], r["lengths"]))


def key_in_file(path: Path) -> str | None:
    """The XAI_API_KEY value of a KEY=VALUE file; None when the file or the line is missing."""
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        name, _, value = line.partition("=")
        if name.strip() == "XAI_API_KEY" and value.strip():
            return value.strip().strip("\"'")
    return None


def load_key(cfg: dict, env=os.environ) -> str:
    """XAI_API_KEY from the environment, else the KEY=VALUE line in [commentary].key_file. Never printed."""
    if env.get("XAI_API_KEY"):
        return env["XAI_API_KEY"].strip()
    key = key_in_file(Path(cfg.get("commentary", {}).get("key_file", "~/.config/dictate/xai.env")).expanduser())
    if key is None:
        raise SystemExit("no xAI key: set XAI_API_KEY or put XAI_API_KEY=... in [commentary].key_file")
    return key


def stt_post(audio: bytes, key: str) -> dict:
    """POST one audio file to xAI speech-to-text (multipart by hand: no extra dependency)."""
    b = uuid.uuid4().hex
    head = lambda name, extra="": f'--{b}\r\nContent-Disposition: form-data; name="{name}"{extra}\r\n\r\n'.encode()  # noqa: E731
    fields = b"".join(head(name) + value.encode() + b"\r\n" for name, value in STT_FIELDS)
    file = head("file", '; filename="commentary.wav"\r\nContent-Type: audio/wav') + audio
    req = urllib.request.Request(
        STT_URL,
        fields + file + f"\r\n--{b}--\r\n".encode(),
        {"Authorization": "Bearer " + key, "Content-Type": f"multipart/form-data; boundary={b}", "User-Agent": hv.UA},
    )
    with urllib.request.urlopen(req, timeout=600) as response:
        return json.load(response)


def final_texts(segs: list[dict]) -> list[str]:
    """Stripped text of each final segment; one without is_final counts as final."""
    return [(s.get("text") or "").strip() for s in segs if s.get("is_final", True)]


def stt_text(body: dict) -> str:
    """Plain text of the response: its `text`, else the final segments joined."""
    if body.get("text"):
        return body["text"].strip()
    return " ".join(filter(None, final_texts(body.get("segments") or body.get("events") or [])))


def input_names(devices) -> dict[int, str]:
    """{index: name} of every device that can record."""
    return {i: d["name"] for i, d in enumerate(devices) if d["max_input_channels"] > 0}


def pick_device(names: dict[int, str], want: str) -> int | None:
    """Index of the first input whose name contains want (any case); None = the default input."""
    return next((i for i, name in names.items() if want.lower() in name.lower()), None) if want else None


def unmatched(names: dict[int, str], want: str) -> str:
    found = ", ".join(names.values()) or "none"
    return f"no input device matching {want!r}; recording from the default input. Found: {found}"


def to_16k(audio: np.ndarray, rate: int) -> np.ndarray:
    """Linear resample of mono float audio from rate to 16 kHz."""
    if rate == vc.SR or not audio.size:
        return audio
    n = round(len(audio) * vc.SR / rate)
    return np.interp(np.arange(n) * rate / vc.SR, np.arange(len(audio)), audio).astype(np.float32)


def record_until_enter(path: Path, want: str) -> None:  # pragma: no cover - needs audio hardware
    """Mic named like want (else the default) -> 16 kHz mono wav until Enter.

    A mic that refuses 16 kHz (the Snowball on Windows) records at its own rate and is resampled.
    """
    import sounddevice as sd

    names = input_names(sd.query_devices())
    device = pick_device(names, want)
    if want and device is None:
        print(unmatched(names, want))
    try:
        sd.check_input_settings(device=device, channels=1, dtype="float32", samplerate=vc.SR)
        rate = vc.SR
    except sd.PortAudioError:
        rate = int(sd.query_devices(device, "input")["default_samplerate"])
    chunks: list[np.ndarray] = [np.zeros(0, np.float32)]

    def on_audio(data, _frames, _time, _status) -> None:
        chunks.append(data[:, 0].copy())

    with sd.InputStream(device=device, samplerate=rate, channels=1, dtype="float32", callback=on_audio):
        input("Recording your comments. Press Enter to stop. ")
    audio = to_16k(np.concatenate(chunks), rate)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(vc.SR)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes())


def is_take(service: Path, file: Path | None) -> bool:
    """file is already one of this service's commentary takes: a retry after a failed upload."""
    return file is not None and file.resolve().parent == service.resolve() and file.name.startswith("commentary-")


def comment(service: Path, cfg: dict, file: Path | None = None, post=stt_post) -> str:
    """Record (or take --file) one take of spoken comments, transcribe with Grok STT, save next to the service.

    Each take keeps its own commentary-<HHMMSS>.wav/.json/.txt; commentary.txt gets every take appended in order.
    """
    key = load_key(cfg)
    if is_take(service, file):
        wav = file  # retrying a take this service already has
    else:
        wav = vc.unused(service / time.strftime("commentary-%H%M%S.wav"))
        if file is None:
            record_until_enter(wav, cfg.get("commentary", {}).get("device", "Snowball"))
        else:
            wav.write_bytes(file.read_bytes())
    audio = wav.read_bytes()
    try:
        body = post(audio, key)
    except OSError as e:
        raise SystemExit(f"xAI STT failed ({e}); the recording is kept: retry with --file {wav}") from None
    wav.with_suffix(".json").write_text(json.dumps(body, indent=1))
    text = stt_text(body)
    wav.with_suffix(".txt").write_text(text + "\n")
    with (service / "commentary.txt").open("a") as f:
        f.write(f"[{wav.stem}] {text}\n")
    return text


def main(args, cfg: dict, error) -> None:
    """review / comment / bench --service; harvest.main parsed args and calls error() on a bad command line."""
    if args.command == "bench":
        print_bench(bench_service(args.service, hv.get_model(*vc.model_spec(cfg)), cfg))
        return
    if not args.service_dir:
        error(f"{args.command} needs a service folder")
    if args.command == "review":
        print_review(review(args.service_dir))
        return
    if args.device is not None:
        cfg.setdefault("commentary", {})["device"] = args.device
    print(f"saved {args.service_dir}/commentary.txt:\n{comment(args.service_dir, cfg, args.file)}")
