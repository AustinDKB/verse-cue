# anti-slop-toolkit

Agent skills, Cursor/Pi harness config, and quality-gate tooling for keeping
AI-assisted code lean — ponytail discipline, metrics-against-slop, parallel
pytest hooks, product-gate personas, book knowledge skills, and [Superpowers](https://github.com/obra/superpowers)
as a submodule.

This repo is **not** an application. Copy (or submodule) the pieces you want
into a consuming project. Scripts expect a typical layout with `app/`, `tests/`,
and optional `docs/metrics/` ledgers created by the record hooks — **this repo
does not ship history ledgers**.

## Contents

| Path | What |
|------|------|
| `.cursor/` | Ponytail + assert-sweep skills, parallel-pytest / ponytail / commit-on-main rules, force-parallel-pytest + protect-pyproject hooks |
| `.agents/skills/` | PR Lens + book skills (Getting Real, Shape Up, DDIA, Data Warehouse Toolkit, Logging Best Practices) |
| `.pi/` | Product-gate skill + persona agents (union/fizzy/kanban stripped), project-safety extension |
| `scripts/` | `metrics_against_slop`, `slop_gate`, radon/halstead/commit metric recorders + checks |
| `docs/guides/` | Metrics-against-slop guide + machine-readable thresholds |
| `packaging/` | Drop-in `pyproject` gate snippets + pre-commit excerpt |
| `vendor/superpowers/` | Git submodule → `https://github.com/obra/superpowers` |

## Clone

```bash
git clone --recurse-submodules https://github.com/AustinDKB/anti-slop-toolkit.git
# or later:
git submodule update --init --recursive
```

## Install into a project (sketch)

1. Copy `.cursor/skills`, `.cursor/rules`, `.cursor/hooks`, and merge `hooks.json`.
2. Copy `.agents/skills` (or symlink) and point your agent skill paths at them.
3. Copy `.pi/agents`, `.pi/skills`, `.pi/extensions` as needed; sanitize paths in `.pi/settings.json`.
4. Copy `scripts/*.py` and wire the hooks from `packaging/pre-commit-gates.yaml`.
5. Merge `[tool.*]` tables from `packaging/pyproject.gates.toml` into your `pyproject.toml`.
6. Init Superpowers: keep `vendor/superpowers` or install via the Superpowers Cursor plugin.

## License

MIT — see [LICENSE](LICENSE). Book skill text is educational summary material;
respect original book copyrights for redistribution beyond this toolkit.
