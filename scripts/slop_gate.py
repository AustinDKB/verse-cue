#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
# ruff: file-ignore[docstring-missing-returns]
"""C1 slop gate: score staged defs with fan-in/depth from .codegraph/codegraph.db."""

from __future__ import annotations

import re
import ast
import sys
from pathlib import Path
import sqlite3
import argparse
import datetime as dt
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import collections

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.metrics_against_slop import (  # ruff: ignore[module-import-not-at-top-of-file]
    ROOT,
    Role,
    ScoreResult,
    VerdictKind,
    SymbolMetrics,
    score,
)

DEF_RE = re.compile(r"^\+\s*(?:async\s+)?def\s+(\w+)\s*\(", re.MULTILINE)
FILE_RE = re.compile(r"^\+\+\+ b/(.+)$", re.MULTILINE)
GIT_FILE_RE = re.compile(r"^a/(.+?) b/(.+)$", re.MULTILINE)
FAIL_AFTER = "2026-09-03"  # mirrors rollout.fail_after
DEFAULT_DB = ROOT / ".codegraph" / "codegraph.db"

# Real schema (read-only dump 2026-09-03): nodes(id, name, kind, file_path, ...);
# edges(source, target, kind, ...) with kind='calls' for call edges.
EDGE_SQL = (
    "SELECT s.name, t.name FROM edges e "
    "JOIN nodes s ON s.id = e.source JOIN nodes t ON t.id = e.target "
    "WHERE e.kind = 'calls'"
)
ENTRY_SQL = (
    "SELECT name FROM nodes WHERE kind = 'function' "
    "AND file_path LIKE 'app/routes/%' AND name NOT LIKE '\\_%' ESCAPE '\\'"
)


def _diff_path(chunk: str) -> str | None:
    """Return the b/ path for one diff --git chunk, or None."""
    match = FILE_RE.search(chunk) or GIT_FILE_RE.search(chunk)
    if not match:
        return None
    path = match.group(match.lastindex)
    return None if path == "/dev/null" else path


def changed_defs(diff: str) -> set[tuple[str, str]]:
    """Return (path, def_name) pairs added in a unified diff."""
    out: set[tuple[str, str]] = set()
    for chunk in diff.split("diff --git ")[1:]:
        path = _diff_path(chunk)
        if path is None:
            continue
        out.update((path, name) for name in DEF_RE.findall(chunk))
    return out


def depth_from_entries(entries: set[str], callees: dict[str, set[str]]) -> dict[str, int]:
    """BFS depth from public entries along callee edges."""
    depth = dict.fromkeys(entries, 0)
    queue: collections.deque[str] = collections.deque(entries)
    while queue:
        cur = queue.popleft()
        for nxt in callees.get(cur, ()):
            if nxt not in depth:
                depth[nxt] = depth[cur] + 1
                queue.append(nxt)
    return depth


def is_fail_mode(today: dt.date, *, fail_after: str) -> bool:
    """Return True on/after fail_after (ISO date)."""
    return today >= dt.date.fromisoformat(fail_after)


def load_call_graph(db: Path) -> tuple[dict[str, set[str]], collections.Counter[str], set[str]]:
    """Return callees, fan_in, public entries (non-underscore defs under app/routes/)."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    # ponytail: name-keyed, not id-keyed; same-named symbols in two files merge. Upgrade: key by (file, name).
    # No exemptions: same-file callers count as fan-in 1 like any other caller; no allowlist lookup here.
    callees: dict[str, set[str]] = collections.defaultdict(set)
    fan_in: collections.Counter[str] = collections.Counter()
    for src, dst in con.execute(EDGE_SQL):
        callees[src].add(dst)
        fan_in[dst] += 1
    entries = {row[0] for row in con.execute(ENTRY_SQL)}
    return callees, fan_in, entries


def _body_stmts(path: Path, name: str) -> int:
    """Return statement count for def `name` in path, or 0 if missing."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return len(node.body)
    return 0


def _git_diff(*, base: str | None) -> str:
    args = ["git", "diff", "-U0", "--", "app"]
    if base is None:
        args.insert(2, "--cached")
    else:
        args.insert(2, base)
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        args,
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return result.stdout


def _metrics_for(
    file: str,
    name: str,
    graph: tuple[collections.Counter[str], dict[str, set[str]], dict[str, int], set[str]],
) -> tuple[SymbolMetrics, ScoreResult]:
    fan_in, callees, depth, entries = graph
    role = Role.A if file.startswith("app/routes/") else Role.B
    private = name.startswith("_")
    # Depth fail targets private helper ladders (S1). Public module APIs may sit
    # deeper without being slop; leave their depth unmeasured here.
    metrics = SymbolMetrics(
        name=name,
        role=role,
        loc=_body_stmts(ROOT / file, name),
        cyclomatic=0,
        cognitive=0,
        nest=0,
        fan_in=fan_in[name],
        fan_out=len(callees.get(name, ())),
        depth_from_entry=depth.get(name) if private else None,
        is_private=private,
        public_entry=name in entries,
    )
    return metrics, score(metrics)


def score_defs_payload(defs: set[tuple[str, str]], db: Path) -> list[dict]:
    """Return serializable C1 score rows for defs; empty defs skip db lookup.

    Raises
    ------
    FileNotFoundError
        When defs is non-empty and db is missing.
    """
    if not defs:
        return []
    if not db.is_file():
        raise FileNotFoundError(db)
    callees, fan_in, entries = load_call_graph(db)
    graph = (fan_in, callees, depth_from_entries(entries, callees), entries)
    rows: list[dict] = []
    for file, name in sorted(defs):
        metrics, result = _metrics_for(file, name, graph)
        rows.append(
            {
                "file": file,
                "name": name,
                "fan_in": metrics.fan_in,
                "fan_out": metrics.fan_out,
                "depth_from_entry": metrics.depth_from_entry,
                "verdict": result.verdict.value,
                "reasons": list(result.reasons),
                "warnings": list(result.warnings),
                "henry_kafura_ifc": result.henry_kafura_ifc,
                "role": metrics.role.value,
            }
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    """Score staged (or --base) defs; warn-only until FAIL_AFTER, then exit 1 on DENY."""
    parser = argparse.ArgumentParser(description="C1 slop gate (staged defs + codegraph)")
    parser.add_argument("--base", default=None, help="git diff base (default: staged --cached)")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="codegraph sqlite path")
    args = parser.parse_args(argv)

    defs = changed_defs(_git_diff(base=args.base))
    if not defs:
        sys.stdout.write("no staged defs under app/\n")
        return 0
    if not args.db.is_file():
        sys.stderr.write(f"codegraph db missing: {args.db}\n")
        return 1

    denies = 0
    for row in score_defs_payload(defs, args.db):
        if row["verdict"] == VerdictKind.DENY.value:
            denies += 1
        warn = f"  warnings={row['warnings']}" if row["warnings"] else ""
        sys.stdout.write(f"{row['verdict']}  {row['file']}:{row['name']}  reasons={row['reasons']}{warn}\n")
    if denies and is_fail_mode(dt.datetime.now(dt.UTC).date(), fail_after=FAIL_AFTER):
        return 1
    if denies:
        sys.stdout.write(f"warn-only until {FAIL_AFTER}: {denies} DENY (exit 0)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
