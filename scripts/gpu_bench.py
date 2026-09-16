"""Parallel harvest.bench_song on CUDA. Spawn (not fork): CUDA + fork deadlocks.

WORKERS replicas, each loads one WhisperModel. Grid points are the tasks.
SONG_LIMIT songs per point (99 fills ~3h at ~16 workers on a 6000-class GPU).
"""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import sys
from pathlib import Path

# docker WORKDIR /app; scripts/ is not a package
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]

import harvest as hv  # noqa: E402
import verse_cue as vc  # noqa: E402


def one(point: dict) -> dict:
    from faster_whisper import WhisperModel

    cfg = vc.load_config()
    cfg["aliases"] = vc.load_aliases()
    limit = int(os.environ.get("SONG_LIMIT", "99"))
    ctype = os.environ.get("COMPUTE_TYPE", "float16")
    wavs = hv.songs(limit)
    if not wavs:
        raise SystemExit("no songs in data/")
    m = {**cfg["model"], **point, "compute_type": ctype}
    model = WhisperModel(point["name"], device="cuda", compute_type=ctype)
    runs = [hv.bench_song(wav, model, {**cfg, "model": m}) for wav in wavs]
    stats = {**point, "compute_type": ctype, **hv.summarize(hv.flat(runs, "deltas"), hv.flat(runs, "lengths"))}
    stats["rtf"] = round(float(__import__("numpy").mean([r["rtf"] for r in runs])), 2)
    print(stats, flush=True)
    return {**stats, "deltas": hv.flat(runs, "deltas"), "timeline": runs[0]["timeline"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=int(os.environ.get("SONG_LIMIT", "99")))
    parser.add_argument("--workers", type=int, default=int(os.environ.get("WORKERS", "16")))
    parser.add_argument("--compute-type", default=os.environ.get("COMPUTE_TYPE", "float16"))
    args = parser.parse_args()
    os.environ["SONG_LIMIT"] = str(args.limit)
    os.environ["COMPUTE_TYPE"] = args.compute_type
    cfg = vc.load_config()
    cfg["aliases"] = vc.load_aliases()
    points = hv.grid(cfg["bench"])
    print(f"points={len(points)} songs={len(hv.songs(args.limit))} workers={args.workers} compute={args.compute_type}", flush=True)
    ctx = mp.get_context("spawn")
    with ctx.Pool(args.workers) as pool:
        rows = pool.map(one, points)
    hv.report(rows, cfg)
    persist()


def persist() -> None:
    """Write commit-sized rows.json and mirror artifacts to /workspace on a pod."""
    import json
    import shutil

    metrics = Path("docs/metrics")
    bench = json.loads((metrics / "bench.json").read_text())
    slim = [{k: v for k, v in r.items() if k != "deltas"} for r in bench["rows"]]
    best = bench["best"]
    if isinstance(best, dict):
        best = {k: v for k, v in best.items() if k != "deltas"}
    (metrics / "rows.json").write_text(json.dumps({"rows": slim, "best": best}))
    print("results:", (metrics / "rows.json").resolve(), flush=True)
    ws = Path("/workspace")
    if not ws.is_dir():
        return
    dest = ws / "verse-cue-results"
    dest.mkdir(exist_ok=True)
    for name in ("bench.json", "rows.json", "summary.md"):
        src = metrics / name
        if src.exists():
            shutil.copy2(src, dest / name)
    auto = Path("verse-cue.auto.toml")
    if auto.exists():
        shutil.copy2(auto, dest / auto.name)


if __name__ == "__main__":
    main()
