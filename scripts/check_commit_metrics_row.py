#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
# ruff: file-ignore[docstring-missing-returns]
"""Verify HEAD has a row in the commit metrics ledger (pre-push / CI)."""

from __future__ import annotations

import os
import sys
import json
import shutil
from pathlib import Path
import argparse
import datetime as dt
import subprocess  # ruff: ignore[suspicious-subprocess-import]

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.slop_gate import is_fail_mode  # ruff: ignore[module-import-not-at-top-of-file]

COMMIT_METRICS_FAIL_AFTER = "2026-09-12"
DEFAULT_HISTORY = ROOT / "docs" / "metrics" / "commit" / "history.jsonl"
_GIT = shutil.which("git") or "git"


def _history_path() -> Path:
    override = os.environ.get("COMMIT_METRICS_HISTORY")
    return Path(override) if override else DEFAULT_HISTORY


def _history_shas(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    shas: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            shas.add(json.loads(line)["git_sha"])
        except (json.JSONDecodeError, KeyError):
            continue
    return shas


def check_head_recorded(*, sha: str) -> int:
    """Return 0 when sha is in history, 1 when missing."""
    return 0 if sha in _history_shas(_history_path()) else 1


def _git_head() -> str:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [_GIT, "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        msg = (result.stderr or result.stdout).strip() or "git rev-parse HEAD failed"
        raise RuntimeError(msg)
    return result.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    """Exit 1 when HEAD missing from ledger (warn-only until COMMIT_METRICS_FAIL_AFTER)."""
    parser = argparse.ArgumentParser(description="Check commit metrics ledger includes HEAD")
    parser.add_argument("--sha", default=None, help="commit SHA (default: HEAD)")
    parser.add_argument("--fail", action="store_true", help="always exit 1 when missing (CI)")
    args = parser.parse_args(argv)

    sha = args.sha or _git_head()
    if check_head_recorded(sha=sha) == 0:
        return 0

    msg = f"HEAD {sha} missing from commit metrics ledger ({_history_path().relative_to(ROOT)})"
    fail = args.fail or is_fail_mode(dt.datetime.now(dt.UTC).date(), fail_after=COMMIT_METRICS_FAIL_AFTER)
    if fail:
        sys.stderr.write(f"{msg}\n")
        return 1
    sys.stderr.write(f"warn-only until {COMMIT_METRICS_FAIL_AFTER}: {msg} (exit 0)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
