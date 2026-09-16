#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
# ruff: file-ignore[docstring-missing-returns]
"""Record per-commit quality metrics ledger (report-only).

Writes:
- docs/metrics/commit/latest.json  — newest commit snapshot
- docs/metrics/commit/history.jsonl — one JSON object per commit (append)

Run manually or from post-commit hook:
    uv run python scripts/record_commit_metrics.py

Set RECORD_COMMIT_METRICS_FULL=1 to also run radon and complexipy (slower).
"""

from __future__ import annotations

import os
import re
import sys
import json
import shutil
from pathlib import Path
from datetime import UTC, datetime
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import xml.etree.ElementTree as ET  # ruff: ignore[suspicious-xml-etree-import]

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import slop_gate  # ruff: ignore[module-import-not-at-top-of-file]

OUT_DIR = ROOT / "docs" / "metrics" / "commit"
LATEST = OUT_DIR / "latest.json"
HISTORY = OUT_DIR / "history.jsonl"
CODEGRAPH_DB = ROOT / ".codegraph" / "codegraph.db"
HALSTEAD_LATEST = ROOT / "docs" / "metrics" / "halstead" / "latest.json"
MUTMUT_LATEST = ROOT / "docs" / "metrics" / "mutmut" / "latest.json"
COVERAGE_XML = ROOT / "coverage.xml"
_APP = ROOT / "app"
_GIT = shutil.which("git") or "git"
_COMPLEXIPY_SCORE_RE = re.compile(r"^\s+\S.*? (\d+)\s+")


def _git_rev_parse(ref: str = "HEAD") -> str:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [_GIT, "rev-parse", ref],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        msg = (result.stderr or result.stdout).strip() or f"git rev-parse {ref} failed"
        raise RuntimeError(msg)
    return result.stdout.strip()


def _git_subject(sha: str) -> str:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [_GIT, "log", "-1", "--format=%s", sha],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _commit_diff(sha: str) -> str:
    parent = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [_GIT, "rev-parse", f"{sha}^"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if parent.returncode != 0:
        return ""
    parent_sha = parent.stdout.strip()
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [_GIT, "diff", "-U0", parent_sha, sha, "--", "app"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else ""


def _history_shas() -> set[str]:
    if not HISTORY.is_file():
        return set()
    shas: set[str] = set()
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            shas.add(json.loads(line)["git_sha"])
        except (json.JSONDecodeError, KeyError):
            continue
    return shas


def _metrics_match(existing: dict, snapshot: dict) -> bool:
    return (
        existing.get("git_sha") == snapshot.get("git_sha")
        and existing.get("subject") == snapshot.get("subject")
        and existing.get("families") == snapshot.get("families")
    )


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _slop_family(diff: str) -> dict:
    defs = slop_gate.changed_defs(diff)
    if not CODEGRAPH_DB.is_file():
        return {"status": "skipped", "changed_defs": len(defs), "deny": 0, "warn": 0, "allow": 0, "defs": []}
    rows = slop_gate.score_defs_payload(defs, CODEGRAPH_DB) if defs else []
    deny = sum(1 for row in rows if row["verdict"] == "DENY")
    allow = sum(1 for row in rows if row["verdict"] == "ALLOW")
    warn = sum(1 for row in rows if row["warnings"])
    return {
        "status": "ok",
        "changed_defs": len(defs),
        "deny": deny,
        "warn": warn,
        "allow": allow,
        "defs": rows,
    }


def _halstead_family() -> dict:
    payload = _load_json(HALSTEAD_LATEST)
    summary = payload.get("summary") if payload else None
    if not isinstance(summary, dict):
        return {"status": "skipped"}
    return {"status": "ok", "summary": summary}


def _mutmut_family() -> dict:
    payload = _load_json(MUTMUT_LATEST)
    stats = payload.get("stats") if payload else None
    if not isinstance(stats, dict):
        return {"status": "skipped", "stats": None}
    return {"status": "ok", "stats": stats}


def _coverage_rates(root: ET.Element) -> dict:
    line_rate = float(root.get("line-rate", "0") or 0)
    branch_rate = float(root.get("branch-rate", "0") or 0)
    lines_covered = int(root.get("lines-covered", "0") or 0)
    lines_valid = int(root.get("lines-valid", "0") or 0)
    branches_covered = int(root.get("branches-covered", "0") or 0)
    branches_valid = int(root.get("branches-valid", "0") or 0)
    denom = lines_valid + branches_valid
    combined = (lines_covered + branches_covered) / denom if denom else None
    return {
        "status": "ok",
        "line_rate": line_rate,
        "branch_rate": branch_rate,
        "combined_rate": combined,
    }


def _coverage_family() -> dict:
    skipped = {"status": "skipped", "line_rate": None, "branch_rate": None, "combined_rate": None}
    if not COVERAGE_XML.is_file():
        return skipped
    try:
        root = ET.parse(COVERAGE_XML).getroot()  # ruff: ignore[suspicious-xml-element-tree-usage]
    except (OSError, ET.ParseError):
        return skipped
    return _coverage_rates(root)


def _run_json_cmd(args: list[str]) -> dict | None:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _radon_cc_max(payload: dict) -> int:
    cc_max = 0
    for blocks in payload.values():
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if isinstance(block, dict):
                cc_max = max(cc_max, int(block.get("complexity") or 0))
    return cc_max


def _radon_mi_min(payload: dict) -> float | None:
    mis = [float(entry["mi"]) for entry in payload.values() if isinstance(entry, dict) and "mi" in entry]
    return min(mis) if mis else None


def _radon_sloc_max(payload: dict) -> int:
    return max(
        (int(metrics.get("sloc") or 0) for metrics in payload.values() if isinstance(metrics, dict)),
        default=0,
    )


def _radon_family() -> dict:
    skipped = {"status": "skipped", "cc_max": None, "mi_min": None, "sloc_max": None}
    if os.environ.get("RECORD_COMMIT_METRICS_FULL") != "1":
        return skipped
    cc_payload = _run_json_cmd([sys.executable, "-m", "radon", "cc", str(_APP), "-s", "-j"])
    mi_payload = _run_json_cmd([sys.executable, "-m", "radon", "mi", str(_APP), "-s", "-j"])
    raw_payload = _run_json_cmd([sys.executable, "-m", "radon", "raw", str(_APP), "-j"])
    if cc_payload is None and mi_payload is None and raw_payload is None:
        return skipped
    return {
        "status": "ok",
        "cc_max": _radon_cc_max(cc_payload) if cc_payload else 0,
        "mi_min": _radon_mi_min(mi_payload) if mi_payload else None,
        "sloc_max": _radon_sloc_max(raw_payload) if raw_payload else 0,
    }


def _complexipy_bin() -> str:
    candidate = Path(sys.executable).with_name("complexipy")
    return str(candidate if candidate.is_file() else "complexipy")


def _complexipy_family() -> dict:
    skipped = {"status": "skipped", "score_max": None}
    if os.environ.get("RECORD_COMMIT_METRICS_FULL") != "1":
        return skipped
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [_complexipy_bin(), str(_APP), "--max-complexity-allowed", "0"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    scores = [int(match.group(1)) for line in result.stdout.splitlines() if (match := _COMPLEXIPY_SCORE_RE.match(line))]
    if not scores and result.returncode != 0:
        return skipped
    return {"status": "ok", "score_max": max(scores) if scores else 0}


def record_commit_metrics(sha: str | None = None) -> dict:
    """Build snapshot for one commit and write latest (+ history when new)."""
    git_sha = sha or _git_rev_parse()
    diff = _commit_diff(git_sha)
    snapshot = {
        "recorded_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "git_sha": git_sha,
        "git_sha_short": git_sha[:7],
        "subject": _git_subject(git_sha),
        "families": {
            "slop_c1": _slop_family(diff),
            "halstead": _halstead_family(),
            "mutmut": _mutmut_family(),
            "coverage": _coverage_family(),
            "radon": _radon_family(),
            "complexipy": _complexipy_family(),
        },
    }
    existing_latest = _load_json(LATEST)
    if git_sha in _history_shas() and existing_latest and _metrics_match(existing_latest, snapshot):
        print(f"Commit metrics unchanged; skipped write ({LATEST}).")
        return existing_latest

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    if git_sha not in _history_shas():
        with HISTORY.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(snapshot, separators=(",", ":")) + "\n")
    return snapshot


def main() -> None:
    """CLI entry: record metrics for HEAD (or fail on git errors)."""
    snapshot = record_commit_metrics()
    slop = snapshot["families"]["slop_c1"]
    print(f"Wrote {LATEST.relative_to(ROOT)}")
    print(
        f"slop_c1: status={slop['status']} changed_defs={slop['changed_defs']} "
        f"deny={slop['deny']} allow={slop['allow']}"
    )


if __name__ == "__main__":
    main()
