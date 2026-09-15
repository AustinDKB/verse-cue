#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
"""Fail the process when Radon complexity or maintainability gates fail.

Gates (strict pack):
- Cyclomatic complexity: fail any block graded B or worse
- Average cyclomatic complexity (`radon cc -a`): must stay grade A with score <= 5.0
- Maintainability Index: fail any module graded below A (B or C)
- Raw SLOC: fail any file with SLOC above MAX_SLOC_PER_FILE

Radon itself exits 0 even when findings exist, so this wrapper inspects output.
"""

from __future__ import annotations

import re
import sys
import json
from pathlib import Path
import operator
import subprocess  # ruff: ignore[suspicious-subprocess-import]

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
TESTS = ROOT / "tests"
MAIN = ROOT / "main.py"
SLOC_PATHS = [APP, TESTS, MAIN]

# Radon A rank is complexity 1-5. Strict average gate requires grade A and score <= 5.
MAX_AVERAGE_SCORE = 5.0
MAX_SLOC_PER_FILE = 300

# radon cc -a / --total-average prints: Average complexity: A (2.01...)
_AVERAGE_RE = re.compile(
    r"Average complexity:\s*([A-F])\s*\((?P<score>[0-9.]+)\)",
    re.IGNORECASE,
)


def _run(args: list[str]) -> str:
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 and not result.stdout.strip():
        sys.stderr.write(result.stderr or result.stdout)
        sys.exit(result.returncode or 1)
    return result.stdout


def _fail(message: str, detail: str = "") -> None:
    sys.stderr.write(f"FAIL: {message}\n")
    if detail.strip():
        sys.stderr.write(detail.rstrip() + "\n")
    sys.exit(1)


def check_cyclomatic() -> None:
    """Fail on B+ blocks and on average complexity worse than strict A."""
    # Full-population average (`-a` + `--total-average`). Do not use `-n` here.
    full_output = _run(
        [
            sys.executable,
            "-m",
            "radon",
            "cc",
            str(APP),
            "-s",
            "-a",
            "--total-average",
        ]
    )
    average_match = _AVERAGE_RE.search(full_output)
    if average_match is None:
        _fail("Could not parse Radon average cyclomatic complexity.", full_output)

    average_grade = average_match.group(1).upper()
    average_score = float(average_match.group("score"))

    if average_grade != "A" or average_score > MAX_AVERAGE_SCORE:
        _fail(
            "Average cyclomatic complexity gate failed "
            f"(need grade A and score <= {MAX_AVERAGE_SCORE}, "
            f"got {average_grade} ({average_score})).",
            full_output,
        )

    # Per-block gate: any B or worse fails.
    bad_blocks = _run(
        [
            sys.executable,
            "-m",
            "radon",
            "cc",
            str(APP),
            "-s",
            "-n",
            "B",
        ]
    ).strip()
    bad_block_lines = [
        line
        for line in bad_blocks.splitlines()
        if not line.startswith("Average complexity:") and "blocks (classes, functions, methods) analyzed." not in line
    ]
    bad_block_text = "\n".join(bad_block_lines).strip()
    if bad_block_text:
        _fail(
            "Cyclomatic complexity gate failed (blocks graded B or worse).",
            bad_block_text,
        )


def check_maintainability() -> None:
    """Fail when any module MI grade is below A."""
    output = _run(
        [
            sys.executable,
            "-m",
            "radon",
            "mi",
            str(APP),
            "-s",
            "-n",
            "B",
        ]
    ).strip()
    if output:
        _fail(
            "Maintainability Index gate failed (modules graded below A).",
            output,
        )


def check_sloc() -> None:
    """Fail when any scanned file exceeds MAX_SLOC_PER_FILE source lines."""
    existing = [str(path) for path in SLOC_PATHS if path.exists()]
    if not existing:
        _fail("No paths found for SLOC check.")

    payload = json.loads(
        _run(
            [
                sys.executable,
                "-m",
                "radon",
                "raw",
                *existing,
                "-j",
            ]
        )
    )
    offenders = sorted(
        (
            (path, int(metrics.get("sloc") or 0))
            for path, metrics in payload.items()
            if int(metrics.get("sloc") or 0) > MAX_SLOC_PER_FILE
        ),
        key=operator.itemgetter(1),
        reverse=True,
    )
    if offenders:
        detail = "\n".join(f"{sloc:4d} SLOC  {path}" for path, sloc in offenders)
        _fail(
            f"SLOC gate failed (max {MAX_SLOC_PER_FILE} source lines per file).",
            detail,
        )


def main() -> None:
    """Run all Radon gates and exit non-zero on failure."""
    if not APP.is_dir():
        _fail(f"Missing app directory: {APP}")
    check_cyclomatic()
    check_maintainability()
    check_sloc()
    print(
        "OK: Radon gates passed "
        f"(cc blocks < B, cc -a grade A and score <= {MAX_AVERAGE_SCORE}, "
        f"mi grade A, sloc <= {MAX_SLOC_PER_FILE}/file)."
    )


if __name__ == "__main__":
    main()
