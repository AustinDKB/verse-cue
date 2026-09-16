# DDIA Decision Cheatsheet

## Start with the workload

| If the main need is… | Start with… | Check before committing |
|---|---|---|
| Current point reads and writes | OLTP model | Write contention, indexes, durability |
| Historical scans and aggregates | OLAP or warehouse | Bytes scanned, freshness, governance |
| Bounded tree read as one unit | Document model | Collection growth and shared references |
| Shared many-to-many relationships | Relational or graph model | Join and traversal patterns |
| Several read shapes | System of record plus derived views | Replay and repair path |

## Pick the physical design

- If writes dominate and sequential I/O fits, use an **LSM-tree**. Budget for compaction and read amplification.
- If predictable point or range reads dominate, use a **B-tree**. Budget for random writes, WAL, and page maintenance.
- If scans use few columns, use **columnar storage**. Prune columns and blocks before optimizing CPU.
- If a query repeats, add an **index or materialized view** only after measuring its write and storage cost.

## Replication and sharding

- If ordered writes and simple reads matter, use **single-leader replication**.
- If local writes during inter-region outages matter, consider **multi-leader replication** and define conflict resolution first.
- If nodes must accept writes independently, use **leaderless replication** with repair and explicit stale-read tolerance.
- For `n` replicas, start by checking `w + r > n`. Do not call this linearizability.
- Shard only when one node cannot meet data or write-throughput needs.
- Choose a partition key from the most common query path. Test skew and hot keys.
- Use key ranges for efficient ranges. Use hashing for even distribution. Use fixed many-shard layouts when growth is predictable.
- A local secondary index makes writes local but reads fan out. A global index focuses reads but needs cross-shard updates.

## Transactions and coordination

- If one object holds the invariant, prefer an atomic write or compare-and-set.
- If concurrent reads and writes can break a multi-object rule, use serializable isolation or materialize a conflict.
- Use **2PC** only when atomic commit across participants is worth blocking and recovery cost.
- Use **linearizability** for hard uniqueness, leader election, locks, and cross-channel recency.
- Use **logical clocks** for order. Use **consensus** when nodes must agree on one decision.
- If a lease holder can pause, add a fencing token at the resource.

## Batch and stream choices

- Use batch for bounded input, replay, rebuilds, and large historical transforms.
- Use streams for unbounded input, low-latency updates, and event-driven views.
- Use event time for business metrics. Define late events, watermarks, and corrections.
- Use tumbling windows for disjoint intervals, hopping windows for overlap, sliding windows for time-distance, and session windows for inactivity gaps.
- Make external effects idempotent. Store the request ID with the effect when possible.

## Correctness and responsibility

- Ask what happens after a timeout. The remote operation may still have committed.
- Keep source events and derivation code versions when views must be rebuilt or audited.
- Separate freshness from correctness. A fast answer can be wrong, and a correct answer can arrive too late.
- For automated decisions, test unequal outcomes, feedback loops, privacy, consent, appeal, and accountable ownership.
