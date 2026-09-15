# Section 6: Performance and Monitoring

## Core Idea
Logging consumes CPU and memory, and logs are the wrong tool for real-time monitoring. Choose libraries and paths that keep the cost low, and use metrics to know when you have a problem.

## Frameworks Introduced
- **Mind the performance cost**: Writing logs takes CPU cycles and memory. The video's benchmark on a basic Go web server:
  - No logging: about 192,000 requests per second.
  - Basic logging with `logrus`: a 20 percent performance drop.
  - Go's newer `slog` package: a 3 percent drop.
  Four mitigations keep logs without destroying performance:
  1. Choose an efficient logging library.
  2. Use log sampling in high-traffic paths.
  3. Log to a separate disk partition, not the one the application runs on.
  4. Run load tests to catch logging bottlenecks early.
- **Use metrics for monitoring, logs for debugging**: Logs and metrics answer different questions. Logs tell you what happened. Metrics tell you how often things are happening. To answer "is my service healthy right now", do not grep through logs to count errors and calculate rates. That is tedious and slow. Use metrics for trends, alerts, and catching problems before they become disasters. Use logs to debug the problems that metrics and alerts point at.

## Key Concepts
- **Throughput**: Requests handled per second, such as 192,000.
- **Performance drop**: The throughput lost to logging, for example 20 percent with `logrus`, 3 percent with `slog`.
- **Load test**: A test that measures the application under expected traffic.
- **Metric**: A count or measurement of how often something happens.
- **Alert**: A notification triggered by a metric threshold.

## Mental Models
- **Logging is a tax on the request path**: Every log statement costs cycles and memory.
- **The library choice is the first lever**: A 3 percent drop beats a 20 percent drop.
- **Logs for the what, metrics for the how often**: Choose the tool by the question.
- **Grep is not monitoring**: Counting errors through logs does not scale and does not alert.

## Anti-patterns
- **Logging in the hot path without sampling**: Paying full cost on every request.
- **Logs and app on one disk**: A full log disk stalls the application.
- **Using logs for real-time monitoring**: Grepping logs to answer a health question.
- **Skipping load tests**: Discovering the logging bottleneck during an incident.

## Worked Example
A team adds verbose request logging to a Go service. The load test shows throughput drops 20 percent. The team switches from `logrus` to `slog`, adds sampling on the high-traffic path, and moves the log files to a separate partition. The drop shrinks to a few percent, and the service keeps its SLO. Separately, the team stops grepping logs for error counts and sets a metric with an alert on the error rate.

## Key Takeaways
1. Choose an efficient logging library such as Go's `slog`.
2. Sample high-traffic paths.
3. Write logs to a separate disk partition.
4. Run load tests to find logging bottlenecks early.
5. Use metrics for trends and alerts.
6. Use logs to debug, not to monitor in real time.

## Connects To
- **Section 1, Objectives and Levels**: The level filter shapes how much the hot path pays.
- **Section 3, Volume Control**: Sampling is both a cost control and a performance mitigation.
- **Section 4, Aggregation and Retention**: Aggregated logs serve debugging; metrics serve alerting.
- **Section 5, Security**: Pipeline filters such as redaction also cost cycles.
