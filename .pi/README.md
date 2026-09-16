# Pi harness pieces (anti-slop-toolkit)

Ports Cursor safety netting into Pi and ships product-gate personas.

## Protections

| Protection | Source | Pi equivalent |
|---|---|---|
| `pyproject.toml` edit gate | `.cursor/hooks/protect-pyproject.py` | `extensions/project-safety.ts` |
| Shell output compaction | `rtk hook cursor` in `.cursor/hooks.json` | `extensions/project-safety.ts` |
| Quality gates | `packaging/pre-commit-gates.yaml` | `/gates` in the consuming project |

## Agents included

Generic product-committee personas only. Domain-specific union / Fizzy / kanban
agents are intentionally omitted.

## Notes

- Use `/reload` after changing files under `.pi/` in a Pi session.
- Product-gate expects the consuming project to provide `docs/product/` ledgers.
