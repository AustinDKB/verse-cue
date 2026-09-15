# Section 4: Aggregation and Retention

## Core Idea
Funnel all logs into one central place, and decide how long each class of log stays. Centralization makes correlation possible; retention policy makes the storage bill sane.

## Frameworks Introduced
- **Centralize and aggregate logs**: When a modern application runs a web server, database, cache, authentication service, and a dozen microservices, every service generates logs in a different place. Funnel all logs into one place so the team can:
  - Search across everything at once.
  - See how a problem in one service impacted another.
  - Look at the same data as one team.
  - Avoid SSHing into twenty servers to debug one issue.
  - Correlate events: a user checkout failure shows the payment service was slow, which caused the cart service to time out, which made the front end show an error, all in one connected view.
- **Set tiered retention**: Storage is not free, and a busy application generates terabytes quickly. A retention policy example: keep recent logs readily available for quick debugging, move older logs to cheaper cold storage, and delete logs that are no longer needed. Not all logs are equal:
  - Error logs: keep about 90 days.
  - Debug logs: about 7 days is plenty.
  - Security audit logs: may need to stay for about a year.

## Key Concepts
- **Centralized logging**: All logs collected into one searchable store.
- **Correlation**: Connecting events across services to see cause and effect.
- **Retention policy**: The rules for how long each class of log is kept.
- **Cold storage**: Cheaper storage for logs that are accessed rarely.
- **Audit log**: A log class with legal or compliance value.

## Mental Models
- **One place to search**: Debugging is a query, not a server tour.
- **Events connect into stories**: The chain of services shows the real cause of a failure.
- **Tiers match value**: Hot storage for recent logs, cold storage for old logs, deletion for the rest.
- **Set the policy before the bill**: The best time to define retention is before the first cloud bill gives you a heart attack.

## Anti-patterns
- **Logs scattered across servers**: SSHing from box to box to debug one issue.
- **Keeping everything forever**: Paying hot-storage prices for logs nobody reads.
- **Treating all logs equally**: Giving debug logs the same retention as audit logs.
- **Centralizing too late**: Building the pipeline only when the need is already urgent.

## Worked Example
A user reports they could not check out. With centralized logging, the engineer searches one store and sees the payment service was slow, which timed out the cart service, which made the front end show an error. All connected, all in one place. Without centralization, the engineer would repeat the same search on each service's logs.

## Key Takeaways
1. Centralize logs from every service into one store.
2. Search across everything at once.
3. Correlate events across services to find root causes.
4. Use tiered retention: hot, cold, then delete.
5. Match retention to log class: errors about 90 days, debug about 7 days, audit about a year.
6. Set the policy before the storage bill arrives.

## Connects To
- **Section 2, Structure and Context**: Shared structure makes central search possible.
- **Section 3, Volume Control**: Sampling controls how much reaches the store.
- **Section 5, Security**: The central store concentrates the security risk.
- **Section 6, Performance and Monitoring**: Aggregated logs feed debugging, not alerting.
