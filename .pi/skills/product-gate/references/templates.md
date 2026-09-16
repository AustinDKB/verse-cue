# Templates and fixed vocabularies

## Fixed vocabulary

Use these values exactly. Do not invent synonyms.

- Evidence level: `E0`, `E1`, `E2`, `E3`, `E4`
- Decision: `reject`, `defer`, `integrate`, `configure`, `build-minimal`, `build`
- Bucket: `core-job`, `trust-infrastructure`, `premature-sophistication`, `edge-case`
- Source: `user-request`, `team-idea`, `strategy-doc`, `job-posting`, `workflow-observation`, `interview`, `support-case`, `posthog`, `competitor`

## MVP audit buckets

| Bucket | Meaning | Default action |
|--------|---------|----------------|
| `core-job` | Without it, the module cannot accomplish its purpose | Keep |
| `trust-infrastructure` | Prevents bad or ambiguous data, makes errors recoverable, makes the next action obvious | Keep |
| `premature-sophistication` | Useful but unsupported by sufficient evidence for the MVP | Remove or defer |
| `edge-case` | Exists in reality but waits for demonstrated demand | Remove or defer |

## Demand ledger entry

Append to `problem_database` or `demand_ledger` in `docs/product/ledger.yaml`.

```yaml
- id: F-001
  feature: "Human-readable feature name"
  module: "members"
  requested_at: "2026-08-11"
  source: "user-request"
  evidence:
    interviews: 0
    customers_requesting: 1
    support_cases: 0
    observed_workarounds: 0
  market_relevance_estimate: 0.5
  frequency: "low"
  pain_when_occurs: "medium"
  existing_solution: "external calendar and notes"
  architecture_blocked_without_feature: false
  complexity:
    schema: "low"
    ui: "medium"
    permissions: "low"
    maintenance: "low"
  evidence_level: "E1"
  decision: "defer"
  trigger_to_reconsider:
    - "5 independent customers request it"
    - "repeated workaround visible in PostHog"
  decision_record: "docs/product/decisions/D-001.md"
```

Rules:

- `id` is monotonic: `F-001`, `F-002`. Never reuse an id.
- Append only. Never delete a past entry.
- A decision that changes updates the entry in place and adds a `history` list.
- `evidence_level` and `decision` use the fixed vocabulary.

## Problem database entry

The problem database holds observed work, not features. Cluster related problems before you propose a feature.

```yaml
- id: P-001
  problem: "Employer roster arrives by email and staff reconcile it manually against member records."
  source: "workflow-observation"
  module: "members"
  frequency: "weekly"
  time_required_minutes: 45
  failure_modes:
    - "stale address"
    - "missed termination"
  who_performs: "office administrator"
  systems_involved:
    - "email"
    - "member spreadsheet"
  status: "active"
  linked_features: []
```

## Decision record

Write one file per decision at `docs/product/decisions/D-XXX.md`. The Product Judge returns this structure.

```markdown
# D-001: <feature name>

Decision: <reject | defer | integrate | configure | build-minimal | build>
Core job: <one sentence>
Evidence level: <E0-E4>
Confidence: <high | medium | low>
Date: <ISO date>

## Rationale
- <claim> — <evidence>

## MVP implementation
<what to build now>

## Explicitly excluded
- <item>

## Future extension path
<how the model extends later>

## Reconsider when
- <trigger>
```

## PostHog signals

| Signal | What it suggests |
|--------|------------------|
| Adoption | Which features and screens are actually used |
| Flow | Where users abandon or loop repeatedly |
| Friction | Dead clicks, rage clicks, repeated searching, excessive navigation |
| Workarounds | Users do work manually; a capability may be missing |
| Unused complexity | Something can be removed because almost nobody uses it |
| Better structure | Two areas should merge instead of adding another feature |
