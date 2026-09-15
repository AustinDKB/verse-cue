# Patterns

## Objectives-first logging
Use when you start a new code path or service.
1. List the application's main goals.
2. Name the critical operations that need monitoring.
3. Choose the KPIs that matter.
4. Write each log statement to serve one of these.

## Verbosity control
Use when an incident needs more detail than the production level provides.
1. Default the production level to INFO.
2. Add a runtime way to raise verbosity.
3. Raise verbosity while investigating.
4. Lower it again after the incident.

## Structured fields
Use for every log event.
1. Give each piece of information its own named field.
2. Use a structured logging framework for your language.
3. Transform legacy text logs into parseable JSON with a tool such as Vector.

## Black box context
Use for every log entry.
1. Add a request ID for tracing across microservices.
2. Add the user ID for session context.
3. Add system state such as database or cache status.
4. Add full error context such as stack traces.

## Selective sampling
Use when log volume drives cost.
1. Keep all error logs during an error spike.
2. Sample success logs instead.
3. Sample aggressively on high-traffic endpoints.
4. Keep full logs for critical parts.
5. Use an observability framework with built-in sampling, such as OpenTelemetry.

## Canonical request line
Use for request-oriented services.
1. Write one log entry at the end of each request.
2. Include what the user tried to do.
3. Include who they were and what went wrong.
4. Include total duration and database time.

## Distributed tracing
Use for multi-service journeys.
1. Use OpenTelemetry traces.
2. Keep each step as a span.
3. Link the spans into one full request.
4. Use tracing instead of detective work across services.

## Centralized correlation
Use when more than a couple of services run.
1. Funnel all logs into one store.
2. Search across everything at once.
3. Correlate events to find the chain of cause and effect.

## Tiered retention
Use to control storage cost.
1. Keep recent logs in hot storage.
2. Move older logs to cold storage.
3. Delete logs nobody needs.
4. Match the tier to the class: errors about 90 days, debug about 7 days, audit about a year.

## Role-based log access
Use to protect log content.
1. Give junior developers basic application logs.
2. Give senior engineers sensitive system logs.
3. Give the security team full access for investigations.
4. Enable audit logging in the log manager.

## Source masking
Use to keep sensitive data out of logs.
1. Mask sensitive fields at the source, for example with Go's `slog`.
2. Log only identifiers, never whole objects.
3. Never log passwords, tokens, or personal data.

## Pipeline redaction
Use as a second layer of protection.
1. Add filters to the logging pipeline.
2. Catch credit card numbers, social security numbers, and API keys.
3. Redact before the data reaches log storage.
4. Use the OpenTelemetry Collector for this.

## Performance-aware logging
Use in every hot path.
1. Choose an efficient logging library.
2. Sample high-traffic paths.
3. Write logs to a separate disk partition.
4. Run load tests to catch bottlenecks early.

## Metrics for monitoring
Use to know when a problem exists.
1. Use metrics for trends and rates.
2. Set alerts on metric thresholds.
3. Use logs to debug after an alert points at the problem.
