---
name: assert-sweep
description: >
  Quick sweep of pytest asserts and small tests: flag noise that should not
  exist, and missing checks that should. Logs every run to an append-only
  ledger and reuses past patterns so later sweeps get sharper. Use when the
  user says "assert sweep", "/assert-sweep", "find useless asserts", "which
  tests are noise", "missing asserts", or "audit the test suite for YAGNI".
---

# Assert sweep

Find **drop** (unneeded) and **need** (missing) asserts. Report only unless
asked to apply. Always log the run so the next sweep learns.

Canonical rule: [docs/solutions/best-practices/assert-what-breaks-behavior.md](../../../docs/solutions/best-practices/assert-what-breaks-behavior.md)

## Before hunting

1. Read `docs/metrics/assert-sweep/latest.json` if present (last summary).
2. Read the last ~40 lines of `docs/metrics/assert-sweep/history.jsonl`.
3. Read `docs/metrics/assert-sweep/patterns.json` (learned drop/need fingerprints).
4. Skip any finding whose `fingerprint` is `resolved` or `dismissed` in history
   unless the cited path’s assert text changed.

## Hunt — drop (noise)

Prefer these smells (extend from `patterns.json` `drop_smells`):

- Import tautology: `assert pkg.__name__ == "pkg"`
- Constant echo: asserting a dict/enum label equals its source literal
- Absence nostalgia: `assert not hasattr(...)` / “field X must never exist”
- Layout cosmetics: magic spacing, min pipe/node counts, snapshot chrome
- Future-field guards: asserting a name that is not in the product model
- Coverage sponges: `isinstance(empty, dict)` with no behavior under test

## Hunt — need (gaps)

Prefer money, auth, and trust-boundary branches with no outcome assert
(extend from `patterns.json` `need_smells`):

- Review/reason strings on matcher conflict paths
- Session expiry / revoke / soft-delete predicates
- Unique / allowlist validators with no negative test
- Pinning / ordering rules that pick which row wins
- Fail-closed auth / encryption gates

One check per non-trivial path. Prefer outcome fields (`review_reason`,
`job_id`, status) over structural mirrors.

## Output (chat)

Two short lists, max five each unless asked for more:

```
drop: <why>. [path:line or test name]
need: <invariant that should fail if broken>. [module or function]
```

End with `logged: docs/metrics/assert-sweep/history.jsonl (+N)`.
Do not apply edits unless the user asks.

## Log (always)

After the report, append **one JSON object per finding** plus **one run
summary** to `docs/metrics/assert-sweep/history.jsonl`, then rewrite
`docs/metrics/assert-sweep/latest.json`.

### Finding line

```json
{
  "recorded_at": "<ISO-8601 UTC>",
  "run_id": "<short uuid or yyyymmdd-HHMM>",
  "git_sha_short": "<7-char sha or unknown>",
  "kind": "drop|need",
  "fingerprint": "<stable id, see below>",
  "path": "tests/... or app/...",
  "symbol": "<test or function name if known>",
  "summary": "<one line>",
  "status": "open",
  "evidence": "<assert snippet or missing branch>"
}
```

### Run summary line

```json
{
  "recorded_at": "<ISO-8601 UTC>",
  "run_id": "<same as findings>",
  "git_sha_short": "<7-char>",
  "kind": "run",
  "drop_count": 0,
  "need_count": 0,
  "skipped_known": 0,
  "patterns_updated": false
}
```

### Fingerprint

`{kind}:{path}:{normalized_symbol_or_snippet}` — lowercase, collapse
whitespace, strip quotes. Same fingerprint across runs = same finding.

### latest.json

```json
{
  "recorded_at": "...",
  "run_id": "...",
  "drop_open": [],
  "need_open": [],
  "recent_resolved": []
}
```

Fill `*_open` from this run’s open findings (fingerprint + one-line summary).
`recent_resolved`: fingerprints whose status flipped to `resolved` since the
prior run (from history), max 10.

## Get smarter

After logging, update `docs/metrics/assert-sweep/patterns.json` when:

| Signal | Action |
|--------|--------|
| Same `drop` smell class appears in ≥2 open findings this run, or ≥3 historically | Add/refresh a `drop_smells` entry with the regex/cue and an example path |
| Same `need` domain (dues/auth/validation) appears as a gap twice | Add/refresh a `need_smells` entry naming the module and invariant |
| User applies a drop/need and confirms | Append a history line with `"status":"resolved"` for that fingerprint (same fields + `"resolution":"removed|added"`) |
| User rejects a finding | Append `"status":"dismissed"` with `"reason"` |

Never delete history lines. Status changes are new appends.

`patterns.json` shape:

```json
{
  "updated_at": "...",
  "drop_smells": [{"id": "...", "cue": "...", "example": "...", "hits": 0}],
  "need_smells": [{"id": "...", "cue": "...", "module": "...", "hits": 0}]
}
```

Increment `hits` when a smell produces a finding this run.

## Boundaries

- Tests and runnable checks only (not product feature review).
- Report by default; apply only when asked.
- Do not invent coverage-percentage goals; ponytail one-check rule wins.
- If ledger dirs are missing, create `docs/metrics/assert-sweep/` before write.
