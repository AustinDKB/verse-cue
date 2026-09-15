# Section 3: Volume Control

## Core Idea
High-volume systems generate hundreds of gigabytes or terabytes of logs per day. Storing everything is expensive and mostly unnecessary. Sample what you store, and write one complete story per request instead of many fragments.

## Frameworks Introduced
- **Sample high-volume logs**: Store a representative sample instead of every log. The model is a poll: you do not ask everyone, you ask a good sample. With a 20 percent sampling rate on an authentication service, 10 identical login events store only 2. Sample selectively:
  - During an error spike, keep all error logs and sample success logs.
  - On a high-traffic endpoint, sample more aggressively.
  - Keep full logs for critical parts.
  - Use the built-in sampling of an observability framework such as OpenTelemetry.
  - Sampling can cut logging cost by 80 percent or more while keeping insights.
- **Write canonical log lines**: For request-oriented services, write one log entry at the end of the request that tells the whole story: what the user tried to do, who they were, what went wrong, how long it took, and how much time the database used. This is a movie summary instead of watching every scene separately, or a post-incident report for every request. For multi-service journeys, prefer **distributed tracing**: OpenTelemetry traces link the spans of one request across all services, keeping each individual step visible as a span.

## Key Concepts
- **Sampling rate**: The fraction of log events that are stored, for example 20 percent.
- **Representative sample**: A subset that still shows the shape of the full traffic.
- **Canonical log line**: One structured entry per request that summarizes the whole journey.
- **Trace**: The complete journey of a request across services.
- **Span**: One individual step inside a trace.
- **Error spike**: A period with an unusual number of failures.

## Mental Models
- **The poll model**: A good sample answers the question without the full population.
- **Selective sampling beats uniform sampling**: Keep what is rare and critical; sample what is repetitive.
- **One story per request**: A single complete entry beats a hundred fragments.
- **Implement early**: Sampling is easy to add before the cost spike, hard to retrofit after.

## Anti-patterns
- **Storing every log**: Paying for terabytes that mostly repeat the same events.
- **Waiting for the cost spike**: Adding sampling only after the bill explodes.
- **Playing detective across fragments**: Jumping between unrelated entries to reconstruct a request.
- **Sampling errors away**: Dropping the logs that are rarest and most valuable.

## Worked Example
A checkout fails. Event-style logging leaves separate entries: button clicked, credentials checked, payment attempted, error shown. The engineer scrolls hundreds of logs to assemble the story. A canonical log line at the end of the request holds all of it: user, action, failure, duration, database time. One query finds the answer. With distributed tracing, the same journey appears as linked spans across the payment and cart services.

## Key Takeaways
1. Store a representative sample at high volume.
2. Sample selectively: keep errors and critical paths complete.
3. Use OpenTelemetry's built-in sampling.
4. Write one canonical log line per request.
5. Prefer distributed tracing for multi-service journeys.
6. Implement sampling before the cost spikes.

## Connects To
- **Section 1, Objectives and Levels**: Levels identify which logs are critical and must stay complete.
- **Section 2, Structure and Context**: Structured fields make canonical lines meaningful.
- **Section 4, Aggregation and Retention**: Sampled and canonical logs still flow to the central store.
- **Section 6, Performance and Monitoring**: Sampling is also a performance mitigation.
