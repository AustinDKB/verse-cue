#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
"""Record Halstead metrics for trend tracking (report-only, never a gate).

Writes:
- docs/metrics/halstead/latest.json  — newest full snapshot
- docs/metrics/halstead/history.jsonl — one JSON object per run (append)

Run manually or from a local habit / CI job:
    uv run python scripts/record_halstead.py
"""

from __future__ import annotations

import sys
import json
from pathlib import Path
from datetime import UTC, datetime
import subprocess  # ruff: ignore[suspicious-subprocess-import]

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
OUT_DIR = ROOT / "docs" / "metrics" / "halstead"
LATEST = OUT_DIR / "latest.json"
HISTORY = OUT_DIR / "history.jsonl"


def _run_halstead() -> dict:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [sys.executable, "-m", "radon", "hal", str(APP), "-j"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout)
        sys.exit(result.returncode or 1)
    return json.loads(result.stdout)


def _summarize(payload: dict) -> dict[str, float | int]:
    """Aggregate per-file totals into project-level summary fields.

    Returns
    -------
    dict of str to float or int
        Project-level Halstead summary fields.
    """
    total_volume = 0.0
    total_difficulty = 0.0
    total_effort = 0.0
    total_bugs = 0.0
    total_time = 0.0
    file_count = 0
    for file_data in payload.values():
        totals = file_data.get("total") or {}
        if not totals:
            continue
        file_count += 1
        total_volume += float(totals.get("volume") or 0)
        total_difficulty += float(totals.get("difficulty") or 0)
        total_effort += float(totals.get("effort") or 0)
        total_bugs += float(totals.get("bugs") or 0)
        total_time += float(totals.get("time") or 0)
    avg_difficulty = (total_difficulty / file_count) if file_count else 0.0
    return {
        "files": file_count,
        "volume": round(total_volume, 4),
        "difficulty_sum": round(total_difficulty, 4),
        "difficulty_avg": round(avg_difficulty, 4),
        "effort": round(total_effort, 4),
        "time": round(total_time, 4),
        "bugs": round(total_bugs, 6),
    }


def _latest_summary() -> dict[str, float | int] | None:
    if not LATEST.is_file():
        return None
    try:
        payload = json.loads(LATEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    summary = payload.get("summary")
    return summary if isinstance(summary, dict) else None


def main() -> None:
    """Write latest Halstead snapshot and append history.

    Skips writes when the summary matches ``latest.json`` so pre-push does not
    rewrite timestamps on every push.
    """
    if not APP.is_dir():
        sys.stderr.write(f"Missing app directory: {APP}\n")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = _run_halstead()
    summary = _summarize(payload)

    if summary == _latest_summary():
        print(f"Halstead summary unchanged; skipped write ({LATEST.relative_to(ROOT)}).")
        print(
            "Summary: "
            f"files={summary['files']} volume={summary['volume']} "
            f"difficulty_avg={summary['difficulty_avg']} "
            f"effort={summary['effort']} bugs={summary['bugs']}"
        )
        return

    recorded_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    snapshot = {
        "recorded_at": recorded_at,
        "tool": "radon hal",
        "path": "app",
        "summary": summary,
        "files": payload,
    }

    LATEST.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    with HISTORY.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "recorded_at": recorded_at,
                    "summary": summary,
                },
                separators=(",", ":"),
            )
            + "\n"
        )

    print(f"Wrote {LATEST.relative_to(ROOT)}")
    print(f"Appended {HISTORY.relative_to(ROOT)}")
    print(
        "Summary: "
        f"files={summary['files']} volume={summary['volume']} "
        f"difficulty_avg={summary['difficulty_avg']} "
        f"effort={summary['effort']} bugs={summary['bugs']}"
    )


if __name__ == "__main__":
    main()
