---
name: logging-best-practices
description: "Knowledge base from the video \"12 Logging BEST Practices in 12 minutes\" by Better Stack. Use when designing or reviewing application logging, choosing log levels, structured logging, log context, sampling, canonical log lines, log aggregation, retention policies, log security, logging performance, or deciding between logs and metrics."
---

<!-- argument-hint: [topic, framework name, or section number] -->

# 12 Logging Best Practices
**Source**: Better Stack | 12 minutes | Published 2024-11-17

## How to Use This Skill

- **Without arguments** — load the core frameworks and decision rules.
- **With a topic** — ask about `sampling`, `retention`, or another indexed topic.
- **With a section** — ask for `ch03` to load that section.
- **Browse** — ask which sections or supporting files cover a topic.

When a question needs detail outside Core Frameworks, read the relevant section file before answering.

## Core Frameworks & Mental Models

### 1. Log with objectives
Use **objectives-first logging** when you start a new code path or a new service. Before you write a log statement, answer three questions: what are the application's main goals, what critical operations need monitoring, and which KPIs matter. An error log's objective is not to scream that something broke. The objective is to give enough context to fix the problem. Log more first, then trim. It is easier to remove noise than to add missing information in production. Review the strategy periodically.

### 2. Use log levels as a scale
Use **log levels** to sort events by severity. **INFO** is business as usual: a successful login or a completed checkout. **WARNING** is the early warning system: something is not right, but nothing failed yet. **ERROR** is a real problem: a failed payment or a failed database connection. **FATAL** is the everything-went-wrong level: the application or part of the stack crashed. Production usually defaults to INFO. Plan to raise verbosity temporarily while you hunt a bug, and give the application a way to change verbosity at runtime.

### 3. Log in structured fields
Use **structured logging** when machines must read the logs. Give every piece of information its own field instead of a wall of text. Structured logs let you filter, search, and analyze: find all timeout errors, or count the errors from last Tuesday. Use a logging framework that emits structured records. When a service only emits text logs, use a tool such as Vector to transform them into parseable JSON. Unstructured logs are expensive text files.

### 4. Log the context to replay the incident
Use **rich context** so the log entry tells the who, what, where, and why in one place. Capture request IDs for tracing across microservices, user IDs for session context, system state such as database or cache status, and full error context such as stack traces. Treat logs as the system's black box recorder. Make them detailed enough to replay and understand any scenario, not just know that it happened.

### 5. Sample high-volume logs
Use **sampling** when log volume drives cost. At high traffic, storing every log is expensive and mostly unnecessary. Store a representative sample instead. Be selective: during an error spike, keep all error logs and sample success logs. Sample aggressively on high-traffic endpoints and keep full logs for critical parts. An observability framework such as OpenTelemetry has built-in sampling. Sampling can cut logging cost by 80 percent or more. Implement it early, before the cost spikes.

### 6. Write canonical log lines
Use **canonical log lines** for request-oriented services. Instead of separate event logs for each step (button clicked, credentials checked, login successful), write one log entry at the end of the request that tells the whole story: what the user tried to do, who they were, what went wrong, how long it took, and how much time the database used. One canonical line per request gives you a post-incident report without scrolling hundreds of logs. For multi-service journeys, prefer distributed tracing: OpenTelemetry traces link the spans of one request across all services.

### 7. Centralize and aggregate logs
Use **centralized logging** when more than a couple of services run. Funnel all logs into one place so the team searches across everything at once. Correlation is the payoff: a user checkout failure shows the payment service was slow, which timed out the cart service, which made the front end error, all in one view. Do not SSH into twenty servers to debug one issue. Start centralizing early, before the need becomes urgent.

### 8. Set tiered retention
Use **tiered retention** to control storage cost. Keep recent logs readily available for quick debugging. Move older logs to cheaper cold storage. Delete logs that no one needs. Not all logs are equal: keep error logs about 90 days, debug logs about 7 days, and security audit logs about a year. Set the policy before the first large cloud bill.

### 9. Secure logs in transit, at rest, and by access
Use **three layers of protection** for logs. Encrypt in transit while logs move from the application to storage. Encrypt at rest while they are stored. Apply access controls so only the right people read them: junior developers see basic application logs, senior engineers see sensitive system logs, and the security team gets full access for investigations. Use a log manager with audit logging to track who accessed what and when.

### 10. Never log sensitive data
Use **sensitive-data hygiene** because logs leak. Logs contain user IDs, IP addresses, database queries, and authentication attempts. Twitter forced a full password reset in 2018 after logging plain-text passwords. GitHub had a similar incident. Mask sensitive fields at the source: Go's `slog` logs only the ID when someone logs a whole user object. Add filters in the logging pipeline to redact credit card numbers, social security numbers, and API keys before storage. The OpenTelemetry Collector can do this. The best leak is the one that never happens because the data was never logged.

### 11. Mind the performance cost
Use **performance-aware logging** because logging consumes CPU and memory. In the video's benchmark, a Go web server handled about 192,000 requests per second without logging. Basic logging with `logrus` caused a 20 percent drop. Go's newer `slog` package caused only a 3 percent drop. Four mitigations: choose an efficient logging library, sample high-traffic paths, log to a separate disk partition, and run load tests to catch logging bottlenecks early.

### 12. Use metrics for monitoring, logs for debugging
Use **the right observability tool** for the question. Logs tell you what happened. Metrics tell you how often things happen. To answer "is my service healthy right now", do not grep logs and count errors. Use metrics for trends, alerts, and early warnings. Use logs to debug problems after a metric or alert points at them.

### Default decision sequence

1. Define the logging objectives for the code path: goals, critical operations, KPIs.
2. Assign a log level to each event: INFO, WARNING, ERROR, or FATAL.
3. Emit structured fields instead of prose.
4. Add the context to replay the incident: request ID, user ID, system state, error context.
5. Sample high-volume paths and keep critical logs complete.
6. Centralize the logs, set tiered retention, secure them, and redact sensitive data.
7. Watch the performance cost and the metrics side of the story.

## Section Index

| File | Section | Frameworks |
|------|---------|------------|
| [ch01](chapters/ch01-objectives-and-levels.md) | Objectives and log levels | Log with objectives, Log levels as a scale |
| [ch02](chapters/ch02-structure-and-context.md) | Structure and context | Structured fields, Context to replay |
| [ch03](chapters/ch03-volume-control.md) | Volume control | Sampling, Canonical log lines |
| [ch04](chapters/ch04-aggregation-and-retention.md) | Aggregation and retention | Centralize, Tiered retention |
| [ch05](chapters/ch05-security.md) | Security | Secure logs, Never log sensitive data |
| [ch06](chapters/ch06-performance-and-monitoring.md) | Performance and monitoring | Performance cost, Metrics vs logs |

## Topic Index

- **Canonical log lines** → ch03
- **Centralization and correlation** → ch04
- **Context and black box recorder** → ch02
- **Cost control** → ch03, ch04
- **Log levels** → ch01
- **Metrics and monitoring** → ch06
- **Objectives and planning** → ch01
- **Performance** → ch06
- **Retention** → ch04
- **Sampling** → ch03
- **Security and sensitive data** → ch05
- **Structured logging** → ch02
- **Tracing** → ch03

## Supporting Files

- [glossary.md](glossary.md) — key terms and definitions.
- [patterns.md](patterns.md) — techniques and design patterns.
- [cheatsheet.md](cheatsheet.md) — decision rules and quick reference.

## Scope & Limits

This skill covers *12 Logging Best Practices* content and navigation to its six section files. It reflects the video's overview method only. The transcript came from auto-generated captions, so exact quotes and numbers may contain caption errors. The performance benchmark (192,000 requests per second, 20 percent, 3 percent) and the retention figures (90 days, 7 days, 1 year) are the video's own examples, not standards. Consult framework documentation for implementation detail. Read a section file when a decision needs more context.
