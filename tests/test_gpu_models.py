"""GPU image model list must match the harvest bench grid."""

import ast
import tomllib
from pathlib import Path


def test_gpu_prefetch_models_match_toml():
    tree = ast.parse(Path("scripts/gpu_models.py").read_text())
    models = next(
        ast.literal_eval(n.value)
        for n in tree.body
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "MODELS"
    )
    assert models == tomllib.loads(Path("verse-cue.toml").read_text())["bench"]["models"]
