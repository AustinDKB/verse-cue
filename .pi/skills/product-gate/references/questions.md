# Questions every feature must survive

Ask every question. Answer each with evidence from the brief, the ledger, or the persona findings. Mark a question `unknown` when evidence is missing. Do not guess.

| # | Question | Evidence that answers it |
|---|----------|--------------------------|
| 1 | Does the product fail at its core purpose without this? | Module core job; product doctrine |
| 2 | Does the need affect a large percentage of target users? | Evidence researcher; domain research |
| 3 | Does it occur frequently? | Usage data; domain research |
| 4 | Is the pain substantial when it occurs? | Support cases; domain research |
| 5 | Does the same underlying need repeat across organizations even if their exact process differs? | JTBD Researcher; problem clustering |
| 6 | Can one generalized primitive solve several variants? | JTBD Researcher; Simplicity Critic; Data Architect |
| 7 | Could existing software or an integration solve it adequately? | Evidence Researcher; Simplicity Critic |
| 8 | Can it be postponed without creating an architectural dead end? | Data Architect |
| 9 | Does adding it create new decisions that users now have to understand? | UX Critic |
| 10 | Is there actual evidence, or is the team designing from imagination? | Ledger; Evidence Researcher; Usage Researcher |

## Scoring

- Six or more answers of `yes` to questions 1-6 with evidence: the feature is a serious candidate.
- Any `yes` to questions 7-9: prefer integrate, configure, or defer.
- Question 10 answers `no evidence`: default to defer or reject.

## Evidence levels

| Level | Meaning | Typical response |
|-------|---------|------------------|
| E0 | Hypothesis — the team imagines the need | Record it. Do not build. |
| E1 | Anecdotal — one person or one org asks for it | Capture the request and context. |
| E2 | Repeated signal — several unrelated users meet the same problem | Investigate seriously. |
| E3 | Behavioral — users repeatedly work around the missing capability | Consider a narrow implementation. |
| E4 | Broad validated need — a meaningful portion of the market experiences it | Consider a first-class capability. |

Large subsystems do not get built at E0 or E1. A deferred decision states the exact trigger that justifies reconsideration.

## Value and cost

```
Feature Value =
    Market Coverage
  × Frequency
  × Pain
  × Strategic Alignment
  × Evidence Confidence

Feature Cost =
    Implementation Complexity
  + UX Complexity
  + Data Model Complexity
  + Permission Complexity
  + Ongoing Maintenance

Priority = Feature Value / Feature Cost
```

The arithmetic supports judgment. It does not replace it. AI makes code cheaper. It does not make product complexity cheaper.
