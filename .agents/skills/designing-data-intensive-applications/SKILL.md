---
name: designing-data-intensive-applications
description: "Knowledge base from \"Designing Data-Intensive Applications\" by Martin Kleppmann and Chris Riccomini. Use when applying its frameworks for reliable, scalable, maintainable data systems, distributed systems, databases, replication, transactions, batch processing, streams, or data ethics."
---
argument-hint: [topic, framework name, or chapter number]

# Designing Data-Intensive Applications
**Authors**: Martin Kleppmann and Chris Riccomini | **Pages**: ~673 | **Chapters**: 14 | **Generated**: 2026-08-13

## How to Use This Skill

- **Without arguments** — load the core frameworks below.
- **With a topic** — find the topic in the index and read the linked chapter.
- **With a framework** — read the matching pattern in `patterns.md` and then the source chapter.
- **With a chapter** — read the exact file in `chapters/`, such as `ch08-transactions.md`.
- **For terms** — use `glossary.md`. For decisions — use `cheatsheet.md`.

## Core Frameworks and Mental Models

### 1. Start with workload and requirements

- Classify data by read shape, write shape, volume, latency, retention, consistency, and failure behavior before choosing a product.
- Separate OLTP from OLAP when analytical scans can harm user-facing transactions.
- Define performance with response-time distributions and tail percentiles. Define reliability with explicit fault classes, recovery targets, and data-loss limits.
- Treat operability, simplicity, and evolvability as system requirements, not later polish.

### 2. Keep one source of truth and derive other views

- Identify the **system of record** for each fact.
- Treat caches, indexes, search stores, warehouses, models, and timelines as derived data.
- Make each derived view rebuildable from retained source data and versioned transformation logic.
- Use materialized views when repeated reads cost more than extra write and propagation work.

### 3. Match the data model to relationships

- Embed bounded tree-shaped data when the aggregate is read and changed together.
- Use normalized references for shared entities, many-to-many relationships, and independently changing records.
- Use relational or graph models when joins or variable-depth traversal are core queries.
- Use event sourcing and CQRS when immutable domain events, audit history, or many read models justify replay and projection operations.
- Prefer declarative query languages because they state intent and allow the engine to optimize execution.

### 4. Match storage to access patterns

- Use LSM-trees for write-heavy workloads that benefit from sequential writes and immutable files.
- Use B-trees for predictable point and range reads with transactional page updates.
- Use column-oriented layouts, compression, pruning, and vectorized execution for analytical scans.
- Treat every index and materialized view as derived data with write amplification, storage, compaction, and repair costs.

### 5. Evolve data through compatibility boundaries

- Support backward compatibility when new readers consume old data and forward compatibility when old readers consume new data.
- Add optional fields, preserve unknown fields, use stable Protocol Buffers tags, and use Avro writer/reader schema resolution with defaults.
- Treat databases, APIs, brokers, and workflow histories as long-lived dataflows.
- Make external effects idempotent because a timeout does not show whether the server acted.

### 6. Choose replication and sharding separately

- Single-leader replication simplifies ordering. Multi-leader replication supports local writes across regions. Leaderless replication tolerates some faults through quorum and repair.
- Define read-after-write, monotonic-read, and consistent-prefix guarantees before routing reads to asynchronous followers.
- Backups restore historical state. Replicas do not replace backups.
- Shard only when one node cannot meet data or write-throughput needs. Choose a partition key that serves common queries without skew.
- Use key ranges for locality and range scans. Use hash schemes for distribution. Plan rebalancing, hot keys, routing, and secondary indexes before scale-up.

### 7. Protect invariants with the right coordination

- ACID names four dimensions. Select the actual isolation and durability behavior that the invariant needs.
- Use atomic writes for single-object rules. Use serializable isolation when a rule spans concurrent reads and writes.
- Distinguish serializability from linearizability. Serializability orders transactions. Linearizability supplies real-time recency for individual objects.
- Use linearizability for hard uniqueness, leader election, locks, and cross-channel timing. Use consensus when nodes must agree on one value or log.
- Use leases with fencing tokens. A paused process can outlive its local lease knowledge.
- Use 2PC only when atomic commit across participants outweighs blocking and recovery costs.

### 8. Treat networks, clocks, and processes as unreliable

- A timeout stops local waiting but does not prove that remote work failed.
- Use monotonic clocks for durations, time-of-day clocks for calendar values, and logical clocks for causality.
- Separate safety, which prevents bad outcomes, from liveness, which guarantees progress.
- Test message delay, duplication, reordering, partition, process pause, and recovery with fault injection or deterministic simulation.

### 9. Use batch and stream processing as dataflow

- Batch processes bounded immutable input and can rebuild state. Stream processes unbounded input and must define offsets, retention, backpressure, time, windows, and late events.
- Use event time for business-time metrics. Use watermarks or explicit lateness policies to handle stragglers.
- Use stream-stream joins for correlated events, stream-table joins for enrichment, and table-table joins for materialized view maintenance.
- Define delivery and effect semantics. Exactly-once usually means one final effect within a stated boundary, supported by idempotence or transactional output.

### 10. Apply end-to-end and ethical reasoning

- A lower layer cannot guarantee a property that the complete path does not enforce. Trace request identity, retries, duplicate suppression, validation, and final effects end to end.
- Avoid coordination for independent work, but use consensus for hard uniqueness and mutually exclusive claims.
- Preserve source events, code versions, inputs, outputs, and integrity checks when auditability matters.
- Treat predictive systems as interventions. Test bias, feedback loops, privacy, consent, recourse, accountability, and power effects.

## Chapter Index

| # | Title | Key frameworks |
|---|---|---|
| [ch01](chapters/ch01-trade-offs-in-data-systems-architecture.md) | Trade-Offs in Data Systems Architecture | OLTP/OLAP, system of record, cloud, distribution |
| [ch02](chapters/ch02-defining-nonfunctional-requirements.md) | Defining Nonfunctional Requirements | latency, percentiles, fault tolerance, scalability, maintainability |
| [ch03](chapters/ch03-data-models-and-query-languages.md) | Data Models and Query Languages | relational/document, graphs, declarative queries, CQRS |
| [ch04](chapters/ch04-storage-and-retrieval.md) | Storage and Retrieval | LSM-trees, B-trees, column storage, indexes |
| [ch05](chapters/ch05-encoding-and-evolution.md) | Encoding and Evolution | compatibility, Protocol Buffers, Avro, durable workflows |
| [ch06](chapters/ch06-replication.md) | Replication | leader models, session guarantees, quorums, version vectors |
| [ch07](chapters/ch07-sharding.md) | Sharding | partition keys, rebalancing, hot spots, secondary indexes |
| [ch08](chapters/ch08-transactions.md) | Transactions | ACID, isolation, serializability, 2PC |
| [ch09](chapters/ch09-trouble-with-distributed-systems.md) | The Trouble with Distributed Systems | partial failure, clocks, leases, fencing, testing |
| [ch10](chapters/ch10-consistency-and-consensus.md) | Consistency and Consensus | linearizability, CAP, logical clocks, consensus |
| [ch11](chapters/ch11-batch-processing.md) | Batch Processing | MapReduce, dataflow, shuffles, joins, ETL |
| [ch12](chapters/ch12-stream-processing.md) | Stream Processing | CDC, event sourcing, time, windows, stream joins |
| [ch13](chapters/ch13-philosophy-of-streaming-systems.md) | A Philosophy of Streaming Systems | derived data, unbundling, end-to-end correctness, auditability |
| [ch14](chapters/ch14-doing-the-right-thing.md) | Doing the Right Thing | bias, privacy, consent, feedback, accountability |

## Topic Index

- **ACID and transactions** → ch08, ch13
- **Batch processing and MapReduce** → ch11, ch13
- **B-trees and LSM-trees** → ch04
- **CAP and partitions** → ch09, ch10
- **Change Data Capture** → ch05, ch06, ch12, ch13
- **Cloud and self-hosting** → ch01
- **Consensus and coordination services** → ch09, ch10, ch13
- **CQRS and event sourcing** → ch03, ch12, ch13
- **Data ethics and privacy** → ch01, ch13, ch14
- **Data models and query languages** → ch03
- **Derived data and materialized views** → ch01–04, ch11–13
- **Distributed transactions and 2PC** → ch08, ch09, ch10
- **Encoding and schema evolution** → ch03, ch05, ch12, ch13
- **Fault tolerance and testing** → ch02, ch06, ch09, ch10, ch11, ch12
- **Graph data** → ch03
- **Indexes and search** → ch03, ch04, ch07, ch11–12
- **Isolation and serializability** → ch08, ch10
- **Logical clocks and causality** → ch06, ch09, ch10, ch12–13
- **OLTP and OLAP** → ch01, ch02, ch04, ch11
- **Replication and consistency** → ch06, ch09, ch10
- **Request routing and sharding** → ch07, ch10
- **Response time and percentiles** → ch02, ch09
- **Safety and liveness** → ch09, ch10, ch13
- **Secondary indexes** → ch04, ch07
- **Storage engines** → ch04
- **Stream processing and windows** → ch11–13
- **System of record** → ch01, ch11–13
- **Unbundled databases** → ch01, ch13
- **Workflow execution and idempotence** → ch05, ch08, ch12–13

## Supporting Files

- [glossary.md](glossary.md) — significant terms with chapter references.
- [patterns.md](patterns.md) — design patterns, algorithms, and techniques.
- [cheatsheet.md](cheatsheet.md) — decision rules, trade-offs, and fast checks.

## Scope and Limits

This skill captures frameworks and technical concepts from the second edition of *Designing Data-Intensive Applications*. It does not replace current database, cloud, security, legal, or project documentation. Validate all choices against the application's workload, failure model, data policy, and operational evidence.
