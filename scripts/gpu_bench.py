"""Max even Whisper copies per size that fit in 60GB, plus batched decode.

Official grid still FakePP-per-song. Concurrency is replicas × batch_size ×
num_workers, not packing idle copies of one size.
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path
from queue import Empty, Queue

sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]

import harvest as hv  # noqa: E402
import numpy as np  # noqa: E402
import verse_cue as vc  # noqa: E402
from gpu_models import MODELS  # noqa: E402

HEADROOM_FRAC = float(os.environ.get("HEADROOM_FRAC", "0.0"))
VRAM_CAP_MB = int(os.environ.get("VRAM_CAP_MB", "61440"))
# large-v3-turbo is 4GB; others are padded CT2 float16 footprints.
COST_MB = {
    "tiny.en": 80,
    "base.en": 150,
    "small.en": 500,
    "distil-large-v3": 1500,
    "large-v3-turbo": 4096,
}
_BURN = np.zeros(16000 * 4, dtype=np.float32)


def max_even(names: list[str] | None = None, cost: dict[str, int] = COST_MB, cap: int | None = None) -> int:
    names = names or MODELS
    return max(1, (cap if cap is not None else VRAM_CAP_MB) // sum(cost[n] for n in names))


def replica_n(raw: str | None = None) -> int:
    n = int(raw if raw is not None else os.environ.get("REPLICAS_PER_MODEL", str(max_even())))
    return max(1, n)


def plan_counts(
    names: list[str],
    free_mb: int,
    cost: dict[str, int] = COST_MB,
    headroom: int | None = None,
    replicas: int | None = None,
) -> dict[str, int]:
    """Same replica count for every size. Drop evenly if it would exceed the 60GB cap."""
    capped = min(free_mb, VRAM_CAP_MB) if VRAM_CAP_MB else free_mb
    hr = int(capped * HEADROOM_FRAC) if headroom is None else headroom
    r = replica_n(str(replicas) if replicas is not None else None)
    budget = max(0, capped - hr)
    while r >= 1:
        used = sum(cost[n] * r for n in names)
        if used <= budget:
            return {n: r for n in names}
        r -= 1
    return {n: 1 for n in names}


def smi_mb(query: str) -> int:
    out = subprocess.check_output(
        ["nvidia-smi", f"--query-gpu={query}", "--format=csv,nounits,noheader"], text=True
    )
    return int(out.strip().splitlines()[0])


def free_mb() -> int:
    return smi_mb("memory.free")


def total_mb() -> int:
    return smi_mb("memory.total")


def headroom_mb(total: int) -> int:
    return max(int(total * HEADROOM_FRAC), int(os.environ.get("HEADROOM_MB", "0") or 0))


def pkey(p: dict) -> tuple:
    return (p["name"], p["window_s"], p["hop_s"], p["prompt_mode"])


def burn(model) -> None:
    segs, _ = model.transcribe(
        _BURN, language="en", beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False
    )
    list(segs)


class _Batched:
    """Pass batch_size into BatchedInferencePipeline.transcribe (verse_cue does not)."""

    def __init__(self, pipe, batch_size: int):
        self._pipe = pipe
        self._batch_size = batch_size

    def transcribe(self, audio, **kw):
        return self._pipe.transcribe(audio, batch_size=self._batch_size, **kw)


def load_pack(names: list[str], ctype: str) -> dict[str, list]:
    from faster_whisper import BatchedInferencePipeline, WhisperModel

    n_rep = replica_n()
    n_workers = int(os.environ.get("WHISPER_NUM_WORKERS", "4"))
    batch = int(os.environ.get("BATCH_SIZE", "16"))
    counts = plan_counts(names, free_mb(), replicas=n_rep)
    print(
        f"pack plan={counts} workers={n_workers} batch={batch} free_mb={free_mb()} total_mb={total_mb()}",
        flush=True,
    )
    models: dict[str, list] = {n: [] for n in names}
    for n, k in counts.items():
        for _ in range(k):
            raw = WhisperModel(n, device="cuda", compute_type=ctype, cpu_threads=1, num_workers=n_workers)
            pipe = BatchedInferencePipeline(model=raw)
            models[n].append(_Batched(pipe, batch))
            print(f"loaded {n} replicas={len(models[n])} free_mb={free_mb()}", flush=True)
    return models


def rows_from_bag(bag: dict, points: list[dict], ctype: str) -> list[dict]:
    rows = []
    for point in points:
        runs = bag.get(pkey(point), [])
        if not runs:
            continue
        stats = {**point, "compute_type": ctype, **hv.summarize(hv.flat(runs, "deltas"), hv.flat(runs, "lengths"))}
        stats["rtf"] = round(float(np.mean([r["rtf"] for r in runs])), 2)
        print(stats, flush=True)
        rows.append({**stats, "deltas": hv.flat(runs, "deltas"), "timeline": runs[0]["timeline"]})
    return rows


def persist() -> None:
    """Write commit-sized rows.json and mirror artifacts to /workspace on a pod."""
    import json
    import shutil

    metrics = Path("docs/metrics")
    bench_path = metrics / "bench.json"
    if not bench_path.exists():
        return
    bench = json.loads(bench_path.read_text())
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=int(os.environ.get("SONG_LIMIT", "99")))
    parser.add_argument("--compute-type", default=os.environ.get("COMPUTE_TYPE", "float16"))
    parser.add_argument("--budget-s", type=int, default=int(os.environ.get("BUDGET_S", "6900")))
    args = parser.parse_args()
    os.environ["SONG_LIMIT"] = str(args.limit)
    os.environ["COMPUTE_TYPE"] = args.compute_type
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    cfg = vc.load_config()
    cfg["aliases"] = vc.load_aliases()
    points = hv.grid(cfg["bench"])
    wavs = hv.songs(args.limit)
    if not wavs:
        raise SystemExit("no songs in data/")
    print(
        f"points={len(points)} songs={len(wavs)} free_mb={free_mb()} compute={args.compute_type} budget_s={args.budget_s}",
        flush=True,
    )
    packed = load_pack(MODELS, args.compute_type)
    print("replicas", {n: len(ms) for n, ms in packed.items()}, "free_mb", free_mb(), flush=True)
    subprocess.run(["nvidia-smi"], check=False)

    queues: dict[str, Queue] = {n: Queue() for n in MODELS}
    n_jobs = 0
    for point in points:
        for wav in wavs:
            queues[point["name"]].put((point, wav))
            n_jobs += 1
    bag: dict[tuple, list] = defaultdict(list)
    bag_lock = threading.Lock()
    stop = threading.Event()
    flushed = threading.Event()
    flush_lock = threading.Lock()
    official_left = [n_jobs]
    official_lock = threading.Lock()

    def flush() -> None:
        with flush_lock:
            if flushed.is_set():
                persist()
                return
            rows = rows_from_bag(dict(bag), points, args.compute_type)
            if not rows:
                return
            hv.report(rows, cfg)
            persist()
            flushed.set()

    def on_stop(*_a) -> None:
        stop.set()
        flush()

    signal.signal(signal.SIGTERM, on_stop)
    signal.signal(signal.SIGINT, on_stop)

    def worker(name: str, model) -> None:
        q = queues[name]
        while not stop.is_set():
            try:
                point, wav = q.get(timeout=0.2)
            except Empty:
                try:
                    burn(model)
                except RuntimeError as e:
                    if "out of memory" not in str(e).lower():
                        raise
                    time.sleep(0.5)
                continue
            retry = False
            try:
                if stop.is_set():
                    continue
                m = {**cfg["model"], **point, "compute_type": args.compute_type}
                run = hv.bench_song(wav, model, {**cfg, "model": m})
                with bag_lock:
                    bag[pkey(point)].append(run)
            except RuntimeError as e:
                if "out of memory" not in str(e).lower():
                    raise
                print("oom retry", name, wav.name, flush=True)
                q.put((point, wav))
                retry = True
                time.sleep(0.5)
            finally:
                q.task_done()
                if not retry:
                    with official_lock:
                        official_left[0] -= 1

    threads = [
        threading.Thread(target=worker, args=(n, model), daemon=True) for n, ms in packed.items() for model in ms
    ]
    print(f"threads={len(threads)} official_jobs={n_jobs}", flush=True)
    end = time.monotonic() + args.budget_s
    for t in threads:
        t.start()
    while time.monotonic() < end:
        with official_lock:
            if official_left[0] <= 0:
                print("official grid done", flush=True)
                break
        time.sleep(0.25)
    timed_out = time.monotonic() >= end
    if timed_out:
        stop.set()
        flush()
    else:
        flush()
        left = end - time.monotonic()
        if left > 0:
            print(f"burn {left:.0f}s", flush=True)
            stop.wait(timeout=left)
        stop.set()
    time.sleep(0.5)
    flush()


if __name__ == "__main__":
    main()
