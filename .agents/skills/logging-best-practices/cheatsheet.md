# Cheatsheet

## Decision rules

- New code path or service → define logging objectives first.
- Routine event, business as usual → INFO.
- Something is off, nothing failed → WARNING.
- Real problem, failure occurred → ERROR.
- Application or stack crashed → FATAL.
- Investigating an incident → raise verbosity temporarily.
- High log volume drives cost → sample.
- Error spike → keep error logs, sample success logs.
- High-traffic endpoint → sample aggressively.
- Request-oriented service → write one canonical log line per request.
- More than a couple of services → centralize and aggregate.
- Storage cost grows → tiered retention.
- Logs move or rest → encrypt.
- Access must be limited → role-based access controls.
- Sensitive data may be logged → mask at source, redact in the pipeline.
- Hot path logging → efficient library, sampling, separate partition, load tests.
- Question is "how often" → metrics and alerts.
- Question is "what happened" → logs.

## Quick reference

| Topic | Rule | Section |
|-------|------|---------|
| Objectives | Define goals, critical operations, KPIs before logging | ch01 |
| INFO | Successful login, completed checkout | ch01 |
| WARNING | Slower than usual, not failed | ch01 |
| ERROR | Failed payment, failed database connection | ch01 |
| FATAL | Out of memory, application shutdown | ch01 |
| Structure | One field per piece of information | ch02 |
| Context | Request ID, user ID, system state, error context | ch02 |
| Sampling | 20 percent stores 2 of 10 identical events | ch03 |
| Cost | Sampling can cut logging cost by 80 percent or more | ch03 |
| Canonical line | One entry per request: who, what, why, duration | ch03 |
| Tracing | OpenTelemetry spans link one request across services | ch03 |
| Retention | Errors 90 days, debug 7 days, audit 1 year | ch04 |
| Security | Encrypt in transit, at rest, control access | ch05 |
| Redaction | Redact cards, social security numbers, API keys | ch05 |
| Benchmark | No logging 192k rps; logrus -20%; slog -3% | ch06 |
| Monitoring | Metrics for trends and alerts; logs for debugging | ch06 |

## The core sentence

Good logging is not about logging everything. It is about logging the right things, in the right way, at the right time.
