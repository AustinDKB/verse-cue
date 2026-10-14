# anti-slop-toolkit

Agent skills, Cursor/Pi harness config, and quality-gate tooling for keeping
AI-assisted code lean — metrics-against-slop, parallel
pytest hooks, and product-gate personas.

This repo is **not** an application. Copy (or submodule) the pieces you want
into a consuming project. Scripts expect a typical layout with `app/`, `tests/`,
and optional `docs/metrics/` ledgers created by the record hooks — **this repo
does not ship history ledgers**.

## Contents

| Path | What |
|------|------|
| `.cursor/` | parallel-pytest / commit-on-main rules, force-parallel-pytest + protect-pyproject hooks |
| `.agents/skills/` | PR Lens |
| `.pi/` | Product-gate skill + persona agents (union/fizzy/kanban stripped), project-safety extension |
| `scripts/` | `metrics_against_slop`, `slop_gate`, radon/halstead/commit metric recorders + checks |
| `docs/guides/` | Metrics-against-slop guide + machine-readable thresholds |
| `packaging/` | Drop-in `pyproject` gate snippets + pre-commit excerpt |

## Clone

```bash
git clone https://github.com/AustinDKB/anti-slop-toolkit.git
```

## Install into a project (sketch)

1. Copy `.cursor/skills`, `.cursor/rules`, `.cursor/hooks`, and merge `hooks.json`.
2. Copy `.agents/skills` (or symlink) and point your agent skill paths at them.
3. Copy `.pi/agents`, `.pi/skills`, `.pi/extensions` as needed; sanitize paths in `.pi/settings.json`.
4. Copy `scripts/*.py` and wire the hooks from `packaging/pre-commit-gates.yaml`.
5. Merge `[tool.*]` tables from `packaging/pyproject.gates.toml` into your `pyproject.toml`.
6. Install Superpowers via the Superpowers Cursor plugin if you want it.

## License

MIT — see [LICENSE](LICENSE).
