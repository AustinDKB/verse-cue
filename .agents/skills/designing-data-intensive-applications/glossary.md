# Glossary

**Asynchronous** — A sender does not wait for a receiver before it continues. (Ch 5–6, 12)

**Backpressure** — Feedback that slows input when downstream processing cannot keep up. (Ch 2, 12)

**Batch process** — A computation over a bounded collection of input. (Ch 11)

**B-tree** — A balanced page-oriented index suited to point and range access. (Ch 4)

**Byzantine fault** — A fault in which a node can lie, equivocate, or act maliciously. (Ch 9–10)

**CAP theorem** — A result about linearizability and availability during a network partition. (Ch 10)

**Causality** — A dependency relation in which one operation knows about or builds on another. (Ch 6, 9–10, 12–13)

**Change Data Capture (CDC)** — A stream of database changes emitted for downstream consumers. (Ch 6, 12–13)

**Compaction** — Merging storage segments while removing obsolete records and tombstones. (Ch 4, 12)

**Consensus** — Agreement among distributed nodes on one value, order, or decision. (Ch 10)

**Declarative query** — A query that states the desired result while the engine chooses execution steps. (Ch 3, 11)

**Denormalization** — Duplication or precomputation that makes a read faster at extra update cost. (Ch 1, 3–4)

**Derived data** — Data computed from an authoritative source and rebuilt when needed. (Ch 1, 11–13)

**Durability** — A committed result survives the failures covered by the storage design. (Ch 6, 8)

**Event time** — The time represented by an event, rather than the time a processor handles it. (Ch 12)

**Event sourcing** — Storing immutable domain events as the source from which state and views derive. (Ch 3, 12–13)

**Failover** — Moving leadership or service responsibility after a node failure. (Ch 6, 10)

**Fault tolerance** — Continued service within stated limits despite specified component faults. (Ch 2, 6, 9–10)

**Follower** — A replica that applies changes from a leader. (Ch 6)

**Graph model** — A model of vertices and edges that makes many-to-many traversal explicit. (Ch 3)

**Hash sharding** — Assigning a record using a hash of its partition key. (Ch 7)

**Idempotent** — An operation whose repeated application has the same intended effect as one application. (Ch 5, 8, 12–13)

**Index** — A derived structure that accelerates a query but adds write and storage work. (Ch 4, 7)

**Isolation** — The rule that defines which effects concurrent transactions can observe. (Ch 8)

**Join** — An operation that combines records using a shared relationship or key. (Ch 3, 11–12)

**Leader** — The replica that accepts and orders writes in leader-based replication. (Ch 6, 10)

**Linearizability** — A recency guarantee that makes operations appear atomic on one current copy. (Ch 6, 10)

**Logical clock** — An event-counting algorithm used to order operations without measuring wall time. (Ch 9–10)

**LSM-tree** — A storage design that writes immutable sorted files and merges them by compaction. (Ch 4)

**Materialized view** — A stored read-oriented result derived from source data. (Ch 2–4, 11–13)

**MVCC** — Multiversion concurrency control, which stores versions for transaction visibility. (Ch 8)

**OLAP** — Online analytical processing over large historical scans and aggregates. (Ch 1, 4, 11)

**OLTP** — Online transaction processing for low-latency operational reads and writes. (Ch 1, 4)

**Partition key** — The key used to select a shard. (Ch 7)

**Percentile** — A value below which a stated percentage of observations fall. (Ch 2)

**Primary key** — A record identifier that is unique within its table or collection. (Ch 3, 7–8)

**Quorum** — A required set or count of replica responses. (Ch 6, 10)

**Rebalancing** — Moving shard ownership to distribute data and request load. (Ch 7)

**Replication** — Keeping copies of data on multiple machines. (Ch 6–7)

**Schema evolution** — Changing data structure while old and new readers or writers coexist. (Ch 3, 5, 12–13)

**Secondary index** — An index that searches by a field other than the primary key. (Ch 4, 7)

**Serializable** — An isolation guarantee equivalent to some serial transaction order. (Ch 8, 10)

**Sharding** — Splitting a dataset into subsets stored on different nodes. (Ch 7)

**Shared-nothing** — An architecture in which nodes do not share storage or memory. (Ch 1–2, 7)

**Skew** — Uneven data or request distribution across workers or shards. (Ch 2, 7, 11)

**Split brain** — Two nodes believe that each has authority to lead or write. (Ch 6, 9–10)

**Stream** — An unbounded sequence of events processed over time. (Ch 11–13)

**Synchronous** — A sender waits for a receiver or condition before it continues. (Ch 5–6, 12)

**System of record** — The authoritative store from which other representations derive. (Ch 1, 11–13)

**Timeout** — A local deadline after which a caller stops waiting. It does not prove remote failure. (Ch 2, 5, 9)

**Transaction** — A group of reads and writes with a commit or abort result. (Ch 8, 13)

**Two-phase commit (2PC)** — A coordinator protocol with prepare and commit phases for atomic distributed commit. (Ch 8, 10)

**Two-phase locking (2PL)** — A serializability method that holds locks while a transaction runs. (Ch 8)

**Unbounded** — A dataset or stream with no known final size or end. (Ch 11–12)

**Version vector** — Per-replica causal metadata used to distinguish overwrites from concurrent writes. (Ch 6)

**Window** — A bounded time or session range used for stream aggregation or joins. (Ch 12)

**Write amplification** — Physical write work divided by the logical data written. (Ch 4)
