# Chapter 12: Stream Processing

## Core Idea
A stream is an unbounded sequence of events. Stream processing applies operators as events arrive, keeps state when needed, and emits derived data or external effects. Unlike batch processing, a stream does not end, so time, ordering, backpressure, replay, and recovery need explicit design.

Streams can come from user actions, sensors, messages, database changes, or event logs. A durable log can serve many consumers, retain history, and support replay. The central choices are delivery semantics, event-time behavior, state management, and fault recovery.

## Frameworks Introduced

- **Direct messaging, message brokers, and log-based brokers**
  - **When to use**: Use direct messaging for simple one-producer-to-one-consumer flows. Use a broker for routing, buffering, and consumer management. Use a durable log for replay and multiple independent consumers.
  - **How**: Define delivery, acknowledgement, redelivery, ordering, retention, and consumer-offset behavior.
  - **Trade-off**: A queue often removes a message after delivery. A log retains messages and lets each consumer track its position.

- **Change Data Capture (CDC)**
  - **When to use**: Use CDC to publish database changes to indexes, caches, warehouses, or services.
  - **How**: Capture a logical change log, take an initial snapshot, then stream changes after the snapshot position. Use an outbox table when the public event schema must differ from the internal schema.
  - **Trade-off**: The database schema becomes a downstream API unless the outbox decouples it.

- **Event sourcing**
  - **When to use**: Use it when immutable application events are the system of record and multiple states must derive from them.
  - **How**: Append domain events. Rebuild current state or materialized views by replaying events. Keep snapshots as a performance aid, not as the only history.
  - **Trade-off**: Event schemas, retention, privacy deletion, and log growth need long-term policy.

- **Materialized view maintenance and incremental view maintenance**
  - **When to use**: Use a stream to keep a read-optimized view current.
  - **How**: Apply each change to the view. Use incremental computation to update only affected results instead of recomputing all source data.

- **Event time and processing time**
  - **When to use**: Use event time for business-time metrics. Use processing time only when arrival time is the intended meaning.
  - **How**: Assign timestamps, define lateness, track watermarks or producer thresholds, and choose whether to ignore stragglers or emit corrections.

- **Windowing**
  - **When to use**: Choose a window from the question being measured.
  - **How**: Tumbling windows do not overlap. Hopping windows overlap at fixed intervals. Sliding windows contain events within a moving interval. Session windows group activity separated by inactivity gaps.

- **Stream joins**
  - **When to use**: Use a stream-stream join for correlated events, a stream-table join for enrichment, and a table-table join for materialized view maintenance.
  - **How**: Store enough state to match events within a window or to represent the current table. Evict state only when the time and correctness policy permits it.

- **Fault tolerance and delivery semantics**
  - **When to use**: Choose at-least-once, at-most-once, or exactly-once effects from business risk.
  - **How**: Use replay, checkpoints, microbatches, transactional output, idempotence, or state rebuilds. Exactly-once usually means exactly-once effect under defined boundaries, not that a message is physically processed once.

## Key Concepts

- **Event stream**: An unbounded sequence of records ordered by some stream position.
- **Consumer offset**: A consumer's position in a durable log.
- **Backpressure**: Feedback that slows input when a consumer cannot keep up.
- **Change Data Capture**: A stream of database changes.
- **Event sourcing**: Storing application events as the durable source of truth.
- **Materialized view**: A stored read-oriented result derived from source data.
- **Event time**: The time an event represents.
- **Processing time**: The time a processor handles an event.
- **Straggler**: A late event that arrives after a window appears complete.
- **Watermark**: A progress signal about the minimum future event timestamp.
- **Window**: A bounded time or session range used for aggregation or joining.
- **Idempotence**: Repeating an operation produces the same effect as one application.

## Mental Models

- Treat a durable log as a database for events and a coordination boundary for consumers.
- Treat state as an integral of events. A changelog is the derivative of state.
- Treat event time as the subject of the metric and processing time as the speed of the measurement.
- Treat every window close as a policy decision under uncertainty.
- Treat a stream processor as a state machine that must recover its state and output position together.

## Anti-patterns

- **Use processing time for event-time business metrics**: Backlogs look like traffic spikes.
- **Close a window without a lateness policy**: Late events silently create wrong results.
- **Use an unbounded state store without retention or compaction**: Memory and disk grow without limit.
- **Assume a broker acknowledgement means the external effect happened once**: Retries can duplicate effects after lost responses.
- **Expose internal database schemas through CDC without a contract**: A column change can break production consumers.
- **Refresh a full materialized view for every event**: Most source data remains unchanged, so freshness and efficiency suffer.

## Code Examples

```sql
SELECT follows.follower_id AS timeline_id,
       array_agg(posts.* ORDER BY posts.timestamp DESC)
FROM posts
JOIN follows ON follows.followee_id = posts.sender_id
GROUP BY follows.follower_id;
```

- **What it demonstrates**: A table-table stream process can maintain a per-user timeline as a materialized join.

## Reference Tables

| Time basis | Meaning | Main risk |
|---|---|---|
| Event time | When the event occurred | Late or incorrect device timestamps |
| Processing time | When the processor handled it | Backlog and restart artifacts |
| Ingestion time | When the system accepted it | Network and buffering delay hides event time |

| Window | Boundary | Common use |
|---|---|---|
| Tumbling | Fixed, nonoverlapping | Counts per minute |
| Hopping | Fixed, overlapping | Smoothed rolling metrics |
| Sliding | Event-to-event interval | Correlation within a duration |
| Session | Inactivity gap | User activity sessions |

## Worked Example

A request-rate processor groups events into one-minute event-time windows. A network outage delays some events from minute 37 until minute 39. The processor can ignore late events and report a drop metric, or emit a correction and retract the earlier value. A watermark can state that no producer expects timestamps before a boundary, but several producers require per-producer progress tracking.

For a mobile client, record the interaction time, send time, and server receive time. The difference between device send time and server receive time estimates clock offset when network delay is small. This estimate can correct the event timestamp while retaining the original values for audit.

## Key Takeaways

1. Define retention, replay, acknowledgement, and redelivery before selecting a messaging system.
2. Use CDC or event sourcing with explicit schema and privacy policies.
3. Use event time when the event's business time matters.
4. Define late-event corrections, watermarks, and state retention.
5. Make external effects idempotent or commit them with the consumed position.
6. Rebuild state from durable input when checkpoints do not cover every failure.

## Connects To

- **Chapter 4**: Log-structured storage and compaction support durable event histories.
- **Chapter 5**: Schema evolution is required for long-lived events and RPC dataflow.
- **Chapter 8**: Exactly-once effects and transactional output need transaction semantics.
- **Chapter 11**: Batch processing supplies replay, rebuilding, and historical recomputation.
- **Chapter 13**: Streaming systems are applications of dataflow, derived state, and end-to-end correctness.
