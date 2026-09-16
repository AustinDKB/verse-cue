---
name: codebase-atlas
description: Expand and verify the local Codebase Atlas. Use when the user asks to add Atlas structures, pipes, districts, source references, recorded traces, payload views, controls, visual rules, or map accuracy checks.
---

# Codebase Atlas

Use this skill for Atlas work only.

## Read first

1. `AGENTS.md`
2. `CONTEXT.md`
3. `docs/specs/codebase-atlas-preferences.md`
4. `docs/codebase-atlas-connection-audit.md`
5. `docs/plans/codebase-atlas-build-plan.md`
6. `data/codebase-atlas/manifest.json`
7. `static/codebase-atlas/atlas.js`
8. `tests/test_codebase_atlas.py`

Read route, service, model, schema, and test files for the requested map area.

## Atlas terms

Use the terms in `CONTEXT.md`.

Do not use a file, class, or helper as an Atlas structure by default. Add a structure only for a high-level runtime role.

## Map data rules

- Edit `data/codebase-atlas/manifest.json` first.
- Keep one source, destination, and relationship in each pipe.
- Add source path, line range, symbol, short label, and district to each structure.
- Keep paths repository-relative.
- Do not put secrets, member data, or local paths in map data.
- Add an import pipe when both direct import endpoints have Atlas structures.
- Add request, guard, response, and data-return pipes when source code shows the runtime relationship.
- Do not add pipes for helper-only modules unless the user asks.
- Keep these districts: Entry & Control, Business Logic, Data, Integrations, and Infrastructure.

## Viewer rules

- Keep the system view visible by default.
- Keep default pipes thin and low contrast.
- Use the cyan accent only for selection and active traces.
- Keep short labels in the global map.
- Put full names and source details in the inspector.
- Keep payload metadata synthetic and sanitized.
- Do not add application requests to recorded traces.
- Keep the local HTTP server as the delivery method.

## Work procedure

1. Inspect the current manifest, snapshot, viewer, tests, and source evidence.
2. Write missing map facts to the manifest.
3. Run `npm run atlas:refresh`.
4. Change `static/codebase-atlas/` only when the user asks for viewer behavior or visual changes.
5. Add or adjust `tests/test_codebase_atlas.py` for new map guarantees.
6. Run the checks.

## Connection audit

Use this audit when the user asks for map accuracy:

1. List direct `app.*` imports from the relevant source files.
2. Map each import to an existing Atlas structure.
3. Add a pipe for each missing high-level relationship.
4. Check FastAPI request order for middleware, guard, response, and database return pipes.
5. Record helper-only exclusions in `docs/codebase-atlas-connection-audit.md`.
6. Do not claim full symbol-level coverage. State the audit scope.

## Checks

Run these checks after Atlas work:

```bash
npm run atlas:refresh
node --check static/codebase-atlas/atlas.js
uv run pytest
uv run pre-commit run --all-files
git diff --check
```

Use `npm run atlas:serve` to serve the page. The Tailscale URL uses the VPS Tailscale address and port `8765`.

## Report

Report these fields:

- Status
- Changed files
- Audit scope
- Checks
- Failures
- Decision needed
