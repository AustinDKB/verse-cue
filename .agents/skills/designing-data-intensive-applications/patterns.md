# Patterns and Techniques

## System of Record and Derived Views
**When to use**: Several consumers need different representations of the same facts.
**How**: Keep one authoritative source, publish changes, and rebuild caches, indexes, warehouses, and projections from it.
**Trade-offs**: Read performance and specialization improve, but propagation lag and rebuild operations become part of the system.

## Materialized View and Fan-Out
**When to use**: A read is frequent and expensive to derive, while extra write work is acceptable.
**How**: Update a read-optimized view when source data changes. Handle high-degree keys with a separate read-time merge or bounded fan-out.
**Trade-offs**: Reads become predictable, but writes consume storage, queue, and repair capacity.

## LSM-Tree Storage
**When to use**: The workload favors sequential writes and immutable files.
**How**: Write to a WAL and memtable, flush SSTables, use Bloom filters, and compact segments.
**Trade-offs**: Write throughput and compression improve, but reads, compaction, tombstones, and write amplification need monitoring.

## B-Tree Storage
**When to use**: Point and range reads need predictable indexed access and transactional updates.
**How**: Maintain balanced pages, split full pages, update pages in place, and protect recovery with a WAL.
**Trade-offs**: Reads are direct, but random writes, page splits, fragmentation, and WAL traffic cost resources.

## Compatible Schema Evolution
**When to use**: Old and new processes or records coexist.
**How**: Add optional fields, use stable field tags, supply defaults, preserve unknown fields, and test both compatibility directions.
**Trade-offs**: Compatibility rules limit schema changes, but they prevent synchronized deployments and broken consumers.

## Single-Leader Replication
**When to use**: Ordered writes and a simple consistency model matter.
**How**: Send writes to a leader, append a log, apply changes on followers, and fence stale leaders during failover.
**Trade-offs**: The model is simple, but the leader can bottleneck writes and failover can lose asynchronous writes.

## Quorum Replication
**When to use**: The system must continue during some node failures.
**How**: Use `n` replicas, require `w` write acknowledgements, and read from `r` replicas. Start with `w + r > n`, then validate edge cases.
**Trade-offs**: Availability and latency improve, but stale reads, concurrent conflicts, repair, and non-linearizable behavior remain possible.

## Key-Range Sharding
**When to use**: Ordered range scans are important.
**How**: Assign contiguous key ranges to shards and split hot or large ranges.
**Trade-offs**: Range scans are efficient, but increasing or nearby keys can form hot shards.

## Hash Sharding with Fixed Shards
**When to use**: Even distribution matters and expected scale is known.
**How**: Create many fixed shards from the start and move whole shards between nodes.
**Trade-offs**: Node movement is simple, but a wrong initial count causes expensive resharding.

## Local and Global Secondary Indexes
**When to use**: A sharded dataset needs searches beyond its partition key.
**How**: Keep local indexes with primary records for simple writes, or shard a global index by search term for focused reads.
**Trade-offs**: Local reads fan out. Global writes cross shards and can be asynchronous or transactional.

## Serializable Isolation
**When to use**: A business invariant spans concurrent reads and writes.
**How**: Use actual serial execution, two-phase locking, or serializable snapshot isolation. Materialize conflicts when a predicate cannot lock efficiently.
**Trade-offs**: Correctness improves, but blocking, aborts, coordination, and throughput cost increase.

## Two-Phase Commit
**When to use**: Several participants must commit or abort as one operation.
**How**: Prepare all participants, then commit only after every participant promises. Recover decisions from durable coordinator state.
**Trade-offs**: Atomic commit is possible, but prepared participants can block while the coordinator is unavailable.

## Fencing Token
**When to use**: A paused or disconnected process can retain stale authority.
**How**: Give each lease holder an increasing token and make the resource reject lower tokens.
**Trade-offs**: It adds a resource-side check, but it prevents delayed stale writes.

## Change Data Capture and Outbox
**When to use**: A database must publish changes without exposing its internal schema.
**How**: Write domain data and an outbox record in one local transaction. CDC streams the outbox schema.
**Trade-offs**: The outbox avoids a cross-system dual write, but it adds storage and transformation maintenance.

## Event-Time Windowing
**When to use**: Results describe when events occurred rather than when they arrived.
**How**: Assign event timestamps, define lateness and watermarks, choose a window, and emit corrections or track drops.
**Trade-offs**: Business accuracy improves, but state retention and late-event handling become necessary.

## Idempotent Consumer
**When to use**: A broker or stream processor can redeliver messages.
**How**: Use a request or event ID, record it with the effect, and treat repeated IDs as no-ops.
**Trade-offs**: Duplicate effects stop, but the deduplication store needs retention and atomicity.

## End-to-End Auditability
**When to use**: The system must explain, verify, or correct derived decisions.
**How**: Retain inputs, code or model versions, validation results, decisions, outputs, and reconciliation evidence.
**Trade-offs**: Storage and governance cost increase, but debugging, appeal, and compliance become possible.
