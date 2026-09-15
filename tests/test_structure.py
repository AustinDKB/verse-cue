"""Anti-slop structure gates the radon script cannot express: total SLOC, call depth, ceremony names."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MODULES = ["verse_cue.py", "harvest.py"]
FORBIDDEN = re.compile(r"(Factory|Manager)$|^Base[A-Z]")
MAX_TOTAL_SLOC = 1000
MAX_DEPTH = 3


def calls_by_function(tree: ast.Module) -> dict[str, set[str]]:
    graph = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            graph[node.name] = {
                n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            }
    return graph


def depth(graph: dict[str, set[str]], name: str, seen: tuple = ()) -> int:
    if name in seen:
        return 0
    children = [c for c in graph.get(name, ()) if c in graph]
    return 1 + max((depth(graph, c, (*seen, name)) for c in children), default=0)


@pytest.mark.parametrize("path", MODULES)
def test_call_depth_from_main_at_most_3(path):
    graph = calls_by_function(ast.parse((REPO / path).read_text()))
    assert "main" in graph
    assert depth(graph, "main") - 1 <= MAX_DEPTH


@pytest.mark.parametrize("path", MODULES)
def test_no_ceremony_names(path):
    tree = ast.parse((REPO / path).read_text())
    names = [n.name for n in ast.walk(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef))]
    assert not [n for n in names if FORBIDDEN.search(n)]


def test_total_production_sloc_under_cap():
    total = 0
    for path in MODULES:
        lines = (REPO / path).read_text().splitlines()
        total += sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))
    assert total <= MAX_TOTAL_SLOC
