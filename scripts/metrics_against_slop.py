#!/usr/bin/env python3
# Copyright (C) 2026 Austin Bakanec
# ruff: file-ignore[docstring-missing-returns]
"""Metrics Against Slop - fixture scorer and repo dry-run (slice A).

Hard gate (fail): FI1 tiny private, depth > 3, ceremony, 0 affected tests on
behavior change. Soft smell warns only. Henry-Kafura IFC is teaching only.

Thresholds mirror docs/guides/machine-readable-thresholds.yaml; constants pinned
to the YAML by test_constants_match_yaml. Pair with Ruff/complexipy/radon - do
not replace them.
"""

from __future__ import annotations

import ast
import sys
from enum import StrEnum
from pathlib import Path
import collections
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"

MAX_BODY_FOR_FI1_FAIL = 4
DEPTH_FAIL_GT = 3
SOFT_FI1 = 3
SOFT_DEPTH = 2
SOFT_LOCAL = 1

ROLE_A_COG_MAX = 12
ROLE_A_CYCLO_MAX = 12
ROLE_A_NEST_MAX = 2
ROLE_B_COG_MAX = 8
ROLE_B_CYCLO_MAX = 8
ROLE_B_NEST_MAX = 2
ROLE_C_COG_MAX = 4
ROLE_C_CYCLO_MAX = 5
ROLE_C_NEST_MAX = 1
ROLE_C_MATCH_COG_MAX = 5
SKIP_PRIVATE_NAMES = frozenset({"__init__", "__post_init__"})


class Role(StrEnum):
    """Function role for band checks."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class VerdictKind(StrEnum):
    """Gate outcome."""

    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass(frozen=True)
class SymbolMetrics:
    """Measured (or fixture-supplied) quantities for one symbol."""

    name: str
    role: Role
    loc: int
    cyclomatic: int
    cognitive: int
    nest: int
    fan_in: int
    fan_out: int
    depth_from_entry: int | None
    is_private: bool
    ceremony: bool = False
    flat_match_allowlist: bool = False
    public_entry: bool = False
    behavior_changed: bool = True
    affected_tests: int | None = None


@dataclass(frozen=True)
class ScoreResult:
    """Hard verdict plus soft smell and teaching IFC."""

    verdict: VerdictKind
    reasons: tuple[str, ...]
    soft_smell: int
    henry_kafura_ifc: int
    graph_ok: bool
    local_ok: bool
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class Fi1Hit:
    """One approximate FI1 tiny private hit."""

    path: str
    line: int
    name: str
    stmts: int


def henry_kafura_ifc(length: int, fan_in: int, fan_out: int) -> int:
    """Return classic IFC = length * (FI * FO)^2 (teaching only)."""
    return length * (fan_in * fan_out) ** 2


def soft_smell(metrics: SymbolMetrics, *, local_outside_band: bool) -> int:
    """Return warn-only smell; never sole fail for role A when graph_ok."""
    fi1 = SOFT_FI1 if _fi1_tiny_private(metrics) else 0
    depth = SOFT_DEPTH * max(0, (metrics.depth_from_entry or 0) - DEPTH_FAIL_GT)
    local = SOFT_LOCAL if local_outside_band else 0
    return fi1 + depth + local


def _fi1_tiny_private(metrics: SymbolMetrics) -> bool:
    return (
        metrics.is_private and metrics.fan_in == 1 and metrics.loc <= MAX_BODY_FOR_FI1_FAIL and not metrics.public_entry
    )


def _local_outside_band(m: SymbolMetrics) -> bool:
    """Return True when locals sit outside the role band (D/E exempt)."""
    if m.role in {Role.D, Role.E}:
        return False
    if m.flat_match_allowlist:
        return m.cognitive > ROLE_C_MATCH_COG_MAX
    cog_max, cyc_max, nest_max = {
        Role.A: (ROLE_A_COG_MAX, ROLE_A_CYCLO_MAX, ROLE_A_NEST_MAX),
        Role.B: (ROLE_B_COG_MAX, ROLE_B_CYCLO_MAX, ROLE_B_NEST_MAX),
        Role.C: (ROLE_C_COG_MAX, ROLE_C_CYCLO_MAX, ROLE_C_NEST_MAX),
    }[m.role]
    return m.cognitive > cog_max or m.cyclomatic > cyc_max or m.nest > nest_max


def _graph_reasons(metrics: SymbolMetrics) -> tuple[list[str], list[str]]:
    """Return (hard deny reasons, soft warnings) for graph/test gates."""
    reasons: list[str] = []
    warnings: list[str] = []
    if _fi1_tiny_private(metrics):
        reasons.append("FI1 tiny private")
    if metrics.depth_from_entry is None:
        warnings.append("depth_from_entry unmeasured")
    elif metrics.depth_from_entry > DEPTH_FAIL_GT:
        reasons.append(f"depth {metrics.depth_from_entry} > {DEPTH_FAIL_GT}")
    if metrics.ceremony:
        reasons.append("ceremony (Protocol x1 / Factory / Manager)")
    if metrics.behavior_changed:
        if metrics.affected_tests is None:
            warnings.append("affected_tests unmeasured")
        elif metrics.affected_tests < 1:
            reasons.append("behavior change with 0 affected tests")
    return reasons, warnings


def score(metrics: SymbolMetrics) -> ScoreResult:
    """Apply hard graph gates, then role-local band."""
    reasons, warnings = _graph_reasons(metrics)
    graph_ok = not reasons
    local_outside = _local_outside_band(metrics)
    local_ok = not local_outside
    if graph_ok and not local_ok:
        reasons.append(f"local metrics outside role {metrics.role} band")

    verdict = VerdictKind.ALLOW if graph_ok and local_ok else VerdictKind.DENY
    return ScoreResult(
        verdict=verdict,
        reasons=tuple(reasons),
        soft_smell=soft_smell(metrics, local_outside_band=local_outside),
        henry_kafura_ifc=henry_kafura_ifc(metrics.loc, metrics.fan_in, metrics.fan_out),
        graph_ok=graph_ok,
        local_ok=local_ok,
        warnings=tuple(warnings),
    )


GOLDEN_FIXTURES: tuple[tuple[str, VerdictKind, SymbolMetrics], ...] = (
    (
        "deny-fi1",
        VerdictKind.DENY,
        SymbolMetrics(
            name="is_active_user",
            role=Role.C,
            loc=2,
            cyclomatic=1,
            cognitive=0,
            nest=0,
            fan_in=1,
            fan_out=0,
            depth_from_entry=1,
            is_private=True,
            affected_tests=1,
        ),
    ),
    (
        "deny-ladder",
        VerdictKind.DENY,
        SymbolMetrics(
            name="ensure_items",
            role=Role.B,
            loc=5,
            cyclomatic=2,
            cognitive=2,
            nest=1,
            fan_in=1,
            fan_out=0,
            depth_from_entry=5,
            is_private=True,
            behavior_changed=True,
            affected_tests=0,
        ),
    ),
    (
        "allow-orchestrator",
        VerdictKind.ALLOW,
        SymbolMetrics(
            name="place_order",
            role=Role.A,
            loc=28,
            cyclomatic=6,
            cognitive=6,
            nest=1,
            fan_in=1,
            fan_out=4,
            depth_from_entry=0,
            is_private=False,
            public_entry=True,
            affected_tests=2,
        ),
    ),
    (
        "allow-helper",
        VerdictKind.ALLOW,
        SymbolMetrics(
            name="parse_money",
            role=Role.B,
            loc=12,
            cyclomatic=3,
            cognitive=3,
            nest=1,
            fan_in=3,
            fan_out=1,
            depth_from_entry=1,
            is_private=False,
            affected_tests=3,
        ),
    ),
    (
        "allow-match",
        VerdictKind.ALLOW,
        SymbolMetrics(
            name="http_label",
            role=Role.C,
            loc=14,
            cyclomatic=8,
            cognitive=2,
            nest=1,
            fan_in=4,
            fan_out=0,
            depth_from_entry=1,
            is_private=False,
            flat_match_allowlist=True,
            affected_tests=1,
        ),
    ),
    (
        "deny-ceremony",
        VerdictKind.DENY,
        SymbolMetrics(
            name="OrderProcessor",
            role=Role.A,
            loc=8,
            cyclomatic=1,
            cognitive=1,
            nest=0,
            fan_in=1,
            fan_out=1,
            depth_from_entry=2,
            is_private=False,
            ceremony=True,
            affected_tests=1,
        ),
    ),
)


def _record_defs_and_calls(
    tree: ast.AST,
    mod: str,
    defs: dict[str, tuple[str, int, int]],
    calls: collections.Counter[str],
) -> None:
    """Fill defs/calls maps from one module AST."""

    class _Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._fn(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._fn(node)

        def _fn(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            if node.name.startswith("_"):
                defs[f"{mod}:{node.name}"] = (mod, node.lineno, len(node.body))
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:
            func = node.func
            if isinstance(func, ast.Name):
                calls[func.id] += 1
            elif isinstance(func, ast.Attribute):
                calls[func.attr] += 1
            self.generic_visit(node)

    _Visitor().visit(tree)


def scan_fi1_tiny_private(app_root: Path = APP) -> list[Fi1Hit]:
    """Return approx private defs with <=4 stmts and bare name called once."""
    defs: dict[str, tuple[str, int, int]] = {}
    calls: collections.Counter[str] = collections.Counter()
    for path in sorted(app_root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        _record_defs_and_calls(tree, str(path.relative_to(ROOT)), defs, calls)

    hits: list[Fi1Hit] = []
    for key, (mod, line, stmts) in defs.items():
        name = key.rsplit(":", 1)[-1]
        if name in SKIP_PRIVATE_NAMES:
            continue
        if calls[name] == 1 and stmts <= MAX_BODY_FOR_FI1_FAIL:
            hits.append(Fi1Hit(path=mod, line=line, name=name, stmts=stmts))
    return sorted(hits, key=lambda hit: (hit.path, hit.line))


def dry_run_report(app_root: Path = APP, *, limit: int = 40) -> str:
    """Return human report of baseline FI1 debt (C2); C1 is PR-scoped only."""
    hits = scan_fi1_tiny_private(app_root)
    by_dir: collections.Counter[str] = collections.Counter()
    for hit in hits:
        parts = hit.path.split("/")
        folder = parts[1] if parts[2:] else parts[-1]
        by_dir[folder] += 1
    lines = [
        "Metrics Against Slop - dry-run (slice A)",
        f"Approx FI1 tiny private in {app_root}: {len(hits)}",
        "Note: C1 (recommended fail gate) only flags NEW/changed symbols on a PR.",
        "      C2 (whole-tree fail) would require cleaning the baseline below.",
        "",
        "Top directories:",
    ]
    for folder, count in by_dir.most_common(12):
        label = f"app/{folder}/" if not folder.endswith(".py") else f"app/{folder}"
        lines.append(f"  {count:4d}  {label}")
    lines.extend(("", f"Sample (first {limit}):"))
    lines.extend(f"  {hit.path}:{hit.line}  {hit.name}  stmts={hit.stmts}" for hit in hits[:limit])
    if len(hits) > limit:
        lines.append(f"  ... +{len(hits) - limit} more")
    return "\n".join(lines) + "\n"


def _run_fixtures() -> int:
    """Print golden fixture results; return process exit code."""
    failed = 0
    for fixture_id, expected, metrics in GOLDEN_FIXTURES:
        result = score(metrics)
        ok = result.verdict is expected
        mark = "ok" if ok else "FAIL"
        sys.stdout.write(
            f"{mark}  {fixture_id}: got {result.verdict} "
            f"smell={result.soft_smell} hk={result.henry_kafura_ifc} "
            f"reasons={list(result.reasons)}\n"
        )
        if not ok:
            failed += 1
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    """Run `fixtures` golden checks or `dry-run` repo FI1 debt report."""
    args = argv if argv is not None else sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        sys.stdout.write("usage: metrics_against_slop.py [fixtures|dry-run]\n")
        return 0
    if args[0] == "fixtures":
        return _run_fixtures()
    if args[0] == "dry-run":
        sys.stdout.write(dry_run_report())
        return 0
    sys.stderr.write(f"unknown command: {args[0]}\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
