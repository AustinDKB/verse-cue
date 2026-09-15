# Chapter 2: Defining Nonfunctional Requirements

## Core Idea
Functional requirements say what a system does; nonfunctional requirements define whether it remains useful under load, failure, and change. Make performance, reliability, scalability, and maintainability explicit and measurable. Optimize the end-to-end experience and the tail of the distribution, not an average that hides the users who suffer most.

## Frameworks Introduced
- **Materialized view and fan-out**: Precompute a read result to make reads cheap, accepting extra work and propagation delay on writes.
  - **When to use**: A read is frequent and expensive to derive, while the derived result can tolerate asynchronous maintenance.
  - **How**: Write the source event, enqueue/update affected projections, serve reads from the projection, and handle high-degree outliers separately.
- **Response-time distribution**: Measure client-visible response time as a distribution; use median and high percentiles rather than only the mean.
  - **When to use**: Any user-facing or service-to-service latency SLO.
  - **How**: Track p50 for typical experience and p95/p99/p999 for tail behavior. Aggregate histograms, not averages of percentiles.
- **Overload controls**: Exponential backoff with jitter, circuit breakers, token buckets, load shedding, and backpressure prevent a retry storm or metastable failure.
  - **When to use**: A dependency approaches capacity, times out, or returns errors under load.
  - **How**: Bound concurrency and retries, reject work deliberately, and communicate pressure upstream.
- **Fault tolerance**: A system is reliable when it continues to meet its SLO despite specified faults; remove single points of failure with redundancy and recovery.
  - **When to use**: Decide what happens when disks, nodes, zones, dependencies, software, or operators fail.
  - **How**: Define tolerated fault classes and limits, exercise them with fault injection, and learn through blameless postmortems.
- **Scalability as a load relationship**: Scalability is not a product label; describe how resource needs and performance change as a particular load dimension grows.
- **Maintainability triad**: **Operability** keeps the system running, **simplicity** keeps it understandable, and **evolvability** keeps change affordable.

## Key Concepts
- **Response time** — elapsed time visible to the client, including service, network, and queueing delays.
- **Service time** — time the service actively processes a request.
- **Latency** — time a request is not actively being processed; network delay is one form.
- **Throughput** — requests, records, or bytes processed per unit time.
- **Queueing delay** — waiting time caused by limited processing capacity.
- **Tail latency** — high-percentile response time, such as p99.
- **SLO/SLA** — an operational performance/availability target and the contract governing consequences when it is missed.
- **Fault/failure** — a faulty component versus a system-level violation of the required service.
- **SPOF** — a single point of failure whose fault takes down the system.
- **Linear scalability** — doubling resources permits roughly twice the load at unchanged performance.

## Mental Models
- **Capacity cliff**: As throughput approaches capacity, queueing grows sharply; a small load increase can cause a large latency increase.
- **The slowest child wins**: A request that waits for several parallel backend calls inherits the slowest call; tail latency amplifies across dependencies.
- **Scale the bottleneck, not the slogan**: Record read/write ratios, payload sizes, concurrency, skew, cache hit rate, and peak behavior before planning capacity.
- **Reliability is bounded**: State which faults and how many simultaneous failures the system tolerates; “highly reliable” without a fault model is not a requirement.
- **Make irreversible actions rare**: Simple, loosely coupled, reversible changes improve evolvability.

## Anti-patterns
- **Optimize the mean**: A good average can coexist with unacceptable p99 latency and a poor user experience.
- **Retry without limits or jitter**: Timeouts can trigger a retry storm that increases load and prevents recovery.
- **Treat every fault as a failure**: Redundancy should allow component faults without escalating them to user-visible failure.
- **Plan hypothetical scale indefinitely**: Premature distributed architecture can reduce simplicity and flexibility before the product’s real bottleneck is known.
- **Blame the operator**: Incidents often expose weak testing, interfaces, rollout, observability, or organizational incentives; a blameless investigation should improve the system.

## Code Examples
A naive home-timeline query illustrates why a read-heavy workload may need a derived view:

```sql
SELECT posts.*, users.*
FROM posts
JOIN follows ON posts.sender_id = follows.followee_id
JOIN users ON posts.sender_id = users.id
WHERE follows.follower_id = current_user
ORDER BY posts.timestamp DESC
LIMIT 1000;
```

## Reference Tables

| Requirement | Useful measure or design response |
|---|---|
| Performance | Client-side response-time distribution; p50 plus tail percentiles |
| Capacity | Throughput and peak concurrency; resource cost at target load |
| Reliability | SLO, fault classes, redundancy, recovery time, data-loss tolerance |
| Scalability | Load dimensions and resource growth needed to preserve the SLO |
| Operability | Monitoring, observability, automation, safe defaults, documented actions |
| Simplicity | Small number of understandable components and explicit abstractions |
| Evolvability | Loose coupling, compatibility, reversible migrations, easy change |

## Worked Example
Suppose a network handles 500 million posts per day—about 5,800 posts per second on average—with spikes to 150,000 posts per second. If 10 million users poll every five seconds, the timeline query runs about 2 million times per second. With 200 followed accounts per user, that implies roughly 400 million sender lookups per second. Instead, materialize each follower’s timeline when a post arrives: 5,800 posts/second × 200 followers is about 1.16 million timeline writes per second, a much cheaper read path. Queueing can absorb spikes. A celebrity with millions of followers is a skewed outlier, so store celebrity posts separately and merge them at read time rather than fan out millions of writes synchronously.

## Key Takeaways
1. State nonfunctional requirements as measurable SLOs tied to user-visible behavior.
2. Measure distributions and tail latency; never average percentiles.
3. Use materialization to trade write work and freshness for predictable reads.
4. Design overload behavior before overload happens: backoff, budgets, shedding, and backpressure.
5. Scale according to observed load shape and bottlenecks, not generic claims about technology.
6. Treat operability, simplicity, and evolvability as first-class requirements.

## Connects To
- **Ch 1**: Applies the workload and architecture trade-offs to measurable requirements.
- **Ch 4**: Storage engines, indexes, and columnar layouts determine the observed performance curve.
- **Ch 5**: Compatible encodings and APIs support rolling upgrades and evolvability.
- **Ch 6–9**: Later chapters develop replication, partitioning, transactions, and distributed-system fault models.
