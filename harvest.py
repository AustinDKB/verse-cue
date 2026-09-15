"""verse-cue-harvest: download songs and lyrics, mine Whisper mis-hearings, bench configurations.

verse-cue-harvest download [--limit N]   songs.txt -> data/<slug>.wav + .lrc + .txt
verse-cue-harvest aliases  [--limit N]   data/*.wav (mix) -> aliases.json
verse-cue-harvest vocals   [--limit N]   data/*.wav -> data/vocals/*.wav (Demucs; mix untouched)
verse-cue-harvest bench    [--limit N]   prefers data/vocals/ when present
verse-cue-harvest graphs                 docs/metrics/*.json -> docs/metrics/*.png
"""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import math
import os
import re
import subprocess
import time
import urllib.parse
import urllib.request
import wave
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

import verse_cue as vc

DATA = Path("data")
METRICS_DIR = Path("docs/metrics")
UA = "verse-cue/0.1 (https://github.com/AustinDKB/verse-cue)"
LRC_RE = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
MISS_GRACE_S = 2.0  # how long a simulated operator waits before advancing a missed slide


def slug(line: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", line.lower()).strip("-")


def download_audio(query: str, wav: Path) -> bool:
    """yt-dlp first search hit -> 16 kHz mono wav next to the requested path."""
    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "--no-playlist",
        "-x",
        "--audio-format",
        "wav",
        "--postprocessor-args",
        "ffmpeg:-ar 16000 -ac 1",
        "-o",
        str(wav.with_suffix("")) + ".%(ext)s",
        "-q",
    ]
    return subprocess.run(cmd, check=False).returncode == 0 and wav.exists()


def lrclib(path: str):
    """GET https://lrclib.net<path> as JSON, None on any failure."""
    req = urllib.request.Request("https://lrclib.net" + path, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.load(response)
    except (OSError, ValueError):
        return None


def fetch_lyrics(artist: str, title: str) -> dict | None:
    """First lrclib search hit that has synced lyrics."""
    query = urllib.parse.urlencode({"artist_name": artist.strip(), "track_name": title.strip()})
    hits = lrclib(f"/api/search?{query}") or []
    return next((h for h in hits if h.get("syncedLyrics")), None)


def parse_lrc(text: str) -> list[tuple[float, str]]:
    """[mm:ss.xx] line -> (seconds, text). Empty-text lines are kept: they mark instrumental breaks."""
    return [(int(m[1]) * 60 + float(m[2]), m[3].strip()) for m in LRC_RE.finditer(text)]


def save_lyrics(rec: dict | None, base: Path) -> bool:
    """Write <base>.lrc (synced) and <base>.txt (plain, derived from the LRC so they always agree)."""
    if not rec:
        print("no synced lyrics:", base.stem)
        return False
    base.with_suffix(".lrc").write_text(rec["syncedLyrics"])
    base.with_suffix(".txt").write_text("\n".join(s for _, s in parse_lrc(rec["syncedLyrics"]) if s))
    return True


def songs(limit: int) -> list[Path]:
    """Wavs in data/ that also have .lrc and .txt, sorted, capped."""
    ready = (p for p in DATA.glob("*.wav") if p.with_suffix(".lrc").exists() and p.with_suffix(".txt").exists())
    return sorted(ready)[:limit]


def download(limit: int) -> None:
    """songs.txt -> data/. Resumable: existing files are skipped. Lines without ' - ' are ignored."""
    DATA.mkdir(exist_ok=True)
    for line in Path("songs.txt").read_text().splitlines()[:limit]:
        if " - " not in line:
            continue
        base = DATA / slug(line)
        if not base.with_suffix(".wav").exists():
            download_audio(line, base.with_suffix(".wav"))
        if not base.with_suffix(".txt").exists():
            save_lyrics(fetch_lyrics(*line.split(" - ", 1)), base)
    print(len(songs(limit)), "songs ready")


def isolate(src: Path, dest: Path) -> bool:
    """Demucs vocal stem to dest as 16 kHz mono. Mix path is never overwritten."""
    if dest.exists():
        return True
    tmp = dest.parent / "_demucs"
    # uv --with: demucs stays out of .venv (aliases may be running)
    cmd = ["uv", "run", "--with", "demucs", "python", "-m", "demucs"]
    cmd += ["--two-stems=vocals", "-n", "htdemucs", "-o", str(tmp), str(src)]
    if subprocess.run(cmd, check=False).returncode:
        print("demucs failed:", src.name)
        return False
    stem = tmp / "htdemucs" / src.stem / "vocals.wav"
    ff = ["ffmpeg", "-y", "-i", str(stem), "-ar", "16000", "-ac", "1", str(dest)]
    return subprocess.run(ff, check=False).returncode == 0 and dest.exists()


def vocals(limit: int) -> None:
    """data/vocals/*.wav for bench. aliases() still reads the YouTube mix."""
    (DATA / "vocals").mkdir(exist_ok=True)
    print(sum(isolate(w, DATA / "vocals" / w.name) for w in songs(limit)), "vocal tracks")


def group_lines(lines: list[tuple[float, str]], per: int) -> list[list[tuple[float, str]]]:
    """Non-empty LRC lines in chunks of `per` (a ProPresenter slide is usually 2 lines)."""
    lyric = [(t, s) for t, s in lines if s]
    return [lyric[i : i + per] for i in range(0, len(lyric), per)]


def pseudo_slides(groups: list[list[tuple[float, str]]], gap_s: float, blank_after_s: float = 5.0) -> list:
    """(start, text) per slide. A gap > gap_s before a group inserts a blank slide blank_after_s after the last line."""
    slides: list[tuple[float, str]] = []
    prev_line = -blank_after_s
    for group in groups:
        if group[0][0] - prev_line > gap_s:
            slides.append((max(prev_line + blank_after_s, 0.0), ""))
        slides.append((group[0][0], " ".join(s for _, s in group)))
        prev_line = group[-1][0]
    return slides


class FakePP:
    """ProPresenter stand-in driven by a truth timeline. Advances like an operator when a slide is missed."""

    def __init__(self, slides: list[tuple[float, str]], now) -> None:
        self.slides, self.now, self.i, self.fires = slides, now, 0, []

    def slide(self) -> tuple[str, str]:
        if self.i + 1 < len(self.slides) and self.now() > self.slides[self.i + 1][0] + MISS_GRACE_S:
            self.fires.append(math.nan)
            self.i += 1
        if self.i >= len(self.slides):
            return "", ""
        return str(self.i), self.slides[self.i][1]

    def next(self, at: float) -> None:
        self.fires.append(at)
        self.i += 1


def wav_frames(path: Path, hop_s: float, cell: list[float]):
    """Slice a 16 kHz mono wav into hops; cell[0] tracks the latest t_end so FakePP can read the clock."""
    with wave.open(str(path)) as w:
        if w.getframerate() != vc.SR or w.getnchannels() != 1:
            raise ValueError(f"{path}: need {vc.SR} Hz mono, got {w.getframerate()} Hz x{w.getnchannels()}")
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    hop = int(hop_s * vc.SR)
    for i in range(0, len(pcm) - hop + 1, hop):
        cell[0] = (i + hop) / vc.SR
        yield cell[0], pcm[i : i + hop]


@functools.cache
def get_model(name: str, compute_type: str):
    """One WhisperModel per (name, compute_type) for the whole process."""
    from faster_whisper import WhisperModel

    return WhisperModel(name, device="auto", compute_type=compute_type)


def song_tokens(model, frames, m: dict) -> list[str]:
    """Transcribe non-overlapping windows of a song; return the normalized words in order."""
    out: list[str] = []
    for _t, chunk in frames:
        out += [w for _, w in vc.transcribe(model, chunk, 0.0, m, "")[0]]
    return [w for w in out if w]


def mishearings(lyric: list[str], heard: list[str]) -> list[tuple[str, str]]:
    """(canonical, heard) pairs from equal-length 'replace' spans of a word-level alignment."""
    ops = SequenceMatcher(None, lyric, heard, autojunk=False).get_opcodes()
    return [
        (lyric[i1 + k], heard[j1 + k])
        for tag, i1, i2, j1, j2 in ops
        if tag == "replace" and i2 - i1 == j2 - j1
        for k in range(i2 - i1)
    ]


def alias_table(counts: Counter, min_count: int, max_per_word: int) -> dict[str, dict[str, int]]:
    """{canonical: {alias: count}} keeping count >= min_count, top max_per_word per word, never alias == canonical."""
    table: dict[str, dict[str, int]] = defaultdict(dict)
    for (canon, alias), n in counts.most_common():
        if n >= min_count and alias != canon and len(table[canon]) < max_per_word:
            table[canon][alias] = n
    return dict(table)


def saturated(curve: list[int], window: int = 10, pct: float = 1.0) -> bool:
    """True when each of the last `window` songs grew the alias set by less than pct percent."""
    if len(curve) <= window:
        return False
    base = curve[-window - 1] or 1
    return all((b - a) * 100 / base < pct for a, b in zip(curve[-window - 1 :], curve[-window:], strict=False))


def alias_passes(cfg: dict) -> list[tuple[object, float]]:
    """Hot passes with the tiny model at each temperature, then one pass with the real runtime model."""
    a, m = cfg["alias"], cfg["model"]
    real = (m["name"], m["compute_type"]) if m["name"] else vc.pick_model(cfg["hardware"], vc.gpu_gb())
    return [(get_model(a["model"], "int8"), t) for t in a["temperatures"]] + [(get_model(*real), 0.0)]


def mine_song(wav: Path, passes: list, m: dict) -> Counter:
    """All (canonical, heard) pairs for one song across all passes."""
    lyric = vc.tokens(wav.with_suffix(".txt").read_text())
    counts: Counter = Counter()
    for model, temperature in passes:
        settings = {**m, "temperature": temperature, "beam_size": 1, "prompt_mode": "none"}
        counts.update(mishearings(lyric, song_tokens(model, wav_frames(wav, m["window_s"], [0.0]), settings)))
    return counts


def aliases(cfg: dict, wavs: list[Path]) -> None:
    """Mine every song until the alias set saturates; write aliases.json and the saturation curve."""
    a = cfg["alias"]
    passes = alias_passes(cfg)
    counts, curve = Counter(), []
    for wav in wavs:
        counts.update(mine_song(wav, passes, cfg["model"]))
        curve.append(sum(n >= a["min_count"] for n in counts.values()))
        print(f"{wav.stem}: {curve[-1]} aliases")
        if saturated(curve):
            break
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    (METRICS_DIR / "alias_saturation.json").write_text(json.dumps(curve))
    vc.ALIASES.write_text(json.dumps(alias_table(counts, a["min_count"], a["max_per_word"]), indent=1))


def bench_song(wav: Path, model, cfg: dict) -> dict:
    """Replay one song through verse_cue.run against a FakePP built from its LRC. Missed = nan."""
    b = cfg["bench"]
    slides = pseudo_slides(
        group_lines(parse_lrc(wav.with_suffix(".lrc").read_text()), b["lines_per_slide"]), b["blank_gap_s"]
    )
    cell = [0.0]
    pp = FakePP(slides, lambda: cell[0])
    t0 = time.monotonic()
    quiet = {**cfg, "metrics_file": os.devnull}
    audio = DATA / "vocals" / wav.name
    vc.run(
        wav_frames(audio if audio.exists() else wav, cfg["model"]["hop_s"], cell),
        pp,
        model,
        quiet,
        wait=lambda _t: None,
    )
    starts = [t for t, _ in slides]
    fires = (pp.fires + [math.nan] * len(starts))[: len(starts) - 1]
    return {
        "deltas": [f - s for f, s in zip(fires, starts[1:], strict=True)],
        "lengths": np.diff(starts).tolist(),
        "rtf": cell[0] / (time.monotonic() - t0),
        "timeline": {"song": wav.stem, "starts": starts, "fires": fires},
    }


def flat(runs: list[dict], key: str) -> list:
    return [x for r in runs for x in r[key]]


def summarize(deltas: list[float], lengths: list[float]) -> dict:
    """delta = fire - truth (negative = early). false = fired before the slide's midpoint. nan = missed."""
    d = np.array(deltas, dtype=float)
    fired = ~np.isnan(d)
    hit = d[fired]
    n = max(len(d), 1)
    half = np.array(lengths, dtype=float) / 2
    return {
        "n": len(d),
        "median_delta": float(np.median(hit)) if hit.size else None,
        "p90_abs_delta": float(np.percentile(np.abs(hit), 90)) if hit.size else None,
        "early_pct": round(100.0 * int((hit < 0).sum()) / n, 1),
        "late_pct": round(100.0 * int((hit > 1.0).sum()) / n, 1),
        "missed_pct": round(100.0 * int((~fired).sum()) / n, 1),
        "false_pct": round(100.0 * int((fired & (d < -half)).sum()) / n, 1),
    }


def grid(b: dict) -> list[dict]:
    keys = ("name", "window_s", "hop_s", "prompt_mode")
    return [
        dict(zip(keys, combo, strict=True))
        for combo in itertools.product(b["models"], b["window_s"], b["hop_s"], b["prompt_mode"])
    ]


def bench(cfg: dict, wavs: list[Path]) -> list[dict]:
    """Every grid point over every song. Returns rows with stats plus raw deltas and one timeline."""
    rows = []
    for point in grid(cfg["bench"]):
        m = {**cfg["model"], **point}
        model = get_model(m["name"], m["compute_type"])
        runs = [bench_song(wav, model, {**cfg, "model": m}) for wav in wavs]
        stats = {**point, "compute_type": m["compute_type"], **summarize(flat(runs, "deltas"), flat(runs, "lengths"))}
        stats["rtf"] = round(float(np.mean([r["rtf"] for r in runs])), 2)
        print(stats)
        rows.append({**stats, "deltas": flat(runs, "deltas"), "timeline": runs[0]["timeline"]})
    return rows


def select(rows: list[dict], b: dict) -> dict | None:
    """Fast enough and not trigger-happy, then the tightest P90."""
    ok = [
        r
        for r in rows
        if r["rtf"] >= b["min_rtf"] and r["false_pct"] <= b["max_false_pct"] and r["p90_abs_delta"] is not None
    ]
    return min(ok, key=lambda r: r["p90_abs_delta"], default=None)


def write_auto(row: dict, path: Path) -> None:
    path.write_text(
        "[model]\n"
        f'name = "{row["name"]}"\ncompute_type = "{row["compute_type"]}"\n'
        f"window_s = {row['window_s']}\nhop_s = {row['hop_s']}\n"
        f'prompt_mode = "{row["prompt_mode"]}"\nbeam_size = 1\n'
    )


def write_summary(rows: list[dict], path: Path) -> None:
    keys = (
        "name",
        "window_s",
        "hop_s",
        "prompt_mode",
        "rtf",
        "median_delta",
        "p90_abs_delta",
        "early_pct",
        "late_pct",
        "missed_pct",
        "false_pct",
    )
    ordered = sorted(rows, key=lambda r: (r["p90_abs_delta"] is None, r["p90_abs_delta"] or 0.0))
    lines = ["| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    lines += ["| " + " | ".join(str(r[k]) for k in keys) + " |" for r in ordered]
    path.write_text("\n".join(lines) + "\n")


def report(rows: list[dict], cfg: dict) -> None:
    """Pick the winner, write verse-cue.auto.toml, docs/metrics/bench.json and summary.md."""
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    best = select(rows, cfg["bench"])
    (METRICS_DIR / "bench.json").write_text(json.dumps({"rows": rows, "best": best}))
    write_summary(rows, METRICS_DIR / "summary.md")
    if best:
        write_auto(best, vc.AUTO)
    print("best:", best and {k: best[k] for k in ("name", "window_s", "hop_s", "prompt_mode", "rtf", "p90_abs_delta")})


def plot_hist(best: dict, out: Path) -> None:
    import matplotlib.pyplot as plt

    deltas = [d for d in best["deltas"] if not math.isnan(d)]
    plt.figure(figsize=(7, 3.5))
    plt.hist(deltas, bins=30, color="#4a7")
    plt.axvline(0, color="k", linewidth=1)
    plt.xlabel("fire - truth (s); negative = early")
    plt.title(f"{best['name']}  window {best['window_s']}s  hop {best['hop_s']}s  prompt {best['prompt_mode']}")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()


def plot_rtf(rows: list[dict], out: Path) -> None:
    import matplotlib.pyplot as plt

    best_rtf: dict[str, float] = {}
    for r in rows:
        best_rtf[r["name"]] = max(best_rtf.get(r["name"], 0.0), r["rtf"])
    plt.figure(figsize=(7, 3.5))
    plt.bar(list(best_rtf), list(best_rtf.values()), color="#47a")
    plt.axhline(4, color="k", linestyle="--", linewidth=1, label="4x real time")
    plt.ylabel("audio seconds per wall second")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()


def plot_saturation(curve: list[int], out: Path) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 3.5))
    plt.plot(range(1, len(curve) + 1), curve, marker="o", color="#a47")
    plt.xlabel("songs harvested")
    plt.ylabel("distinct aliases")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()


def plot_timeline(tl: dict, out: Path) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(9, 2.5))
    plt.vlines(tl["starts"], 0, 1, color="k", label="slide start (truth)")
    plt.vlines([f for f in tl["fires"] if not math.isnan(f)], 0, 0.6, color="#4a7", label="verse-cue fired")
    plt.yticks([])
    plt.xlabel(f"{tl['song']} (s)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()


def graphs(metrics_dir: Path = METRICS_DIR) -> None:
    """Render docs/metrics/*.png from bench.json (+ alias_saturation.json when present)."""
    import matplotlib

    matplotlib.use("Agg")
    bench_data = json.loads((metrics_dir / "bench.json").read_text())
    best = bench_data["best"] or bench_data["rows"][0]  # nothing passed the gates: still show the first row
    plot_hist(best, metrics_dir / "delta_hist.png")
    plot_rtf(bench_data["rows"], metrics_dir / "rtf_vs_model.png")
    plot_timeline(best["timeline"], metrics_dir / "timeline.png")
    saturation = metrics_dir / "alias_saturation.json"
    if saturation.exists():
        plot_saturation(json.loads(saturation.read_text()), metrics_dir / "alias_saturation.png")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="verse-cue-harvest", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("command", choices=["download", "aliases", "vocals", "bench", "graphs"])
    parser.add_argument("--limit", type=int, default=None, help="max songs (bench defaults to [bench].songs)")
    args = parser.parse_args(argv)
    cfg = vc.load_config()
    cfg["aliases"] = vc.load_aliases()
    limit = args.limit if args.limit is not None else 10_000
    steps = {
        "download": lambda: download(limit),
        "aliases": lambda: aliases(cfg, songs(limit)),
        "bench": lambda: report(bench(cfg, songs(min(limit, cfg["bench"]["songs"]))), cfg),
        "graphs": graphs,
        "vocals": lambda: vocals(limit),
    }
    steps[args.command]()


if __name__ == "__main__":
    main()
