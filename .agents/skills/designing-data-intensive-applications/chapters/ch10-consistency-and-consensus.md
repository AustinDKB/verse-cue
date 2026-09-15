# Chapter 10: Consistency and Consensus

## Core Idea
Strong consistency becomes useful when a replicated service should look like one current copy of the data. Linearizability gives that recency guarantee for individual objects. Consensus lets distributed nodes agree on a value, an order, or a commit decision despite failures.

Linearizability has a cost. When nodes cannot communicate, a linearizable system must reject or delay operations that require agreement. Logical clocks can order events but cannot make a value current. Consensus combines ordering, leader election, and fault tolerance, but it needs a quorum and remains sensitive to network delay.

## Frameworks Introduced

- **Linearizability**
  - **When to use**: Use it for locks, leader election, uniqueness, cross-channel timing, and hard constraints.
  - **How**: Treat each operation as taking effect at one point between request and response. If one operation completes before another starts, the later operation must observe a state at least as new.

- **Serializability versus linearizability**
  - **When to use**: Use serializability to reason about transaction interleavings. Use linearizability to reason about the recency of individual reads and writes.
  - **How**: A system can be serializable but return stale data. Strict serializability combines serializable transactions with linearizable recency.

- **CAP trade-off**
  - **When to use**: Use the theorem as a narrow statement about linearizability during a network partition.
  - **How**: When a partition separates replicas, choose whether to reject or delay operations that require consistency or to accept operations with weaker consistency.
  - **Correction**: Do not describe CAP as choosing two of three normal features. Partitions are faults, and consistency and availability can coexist when the network works.

- **Logical clocks**
  - **When to use**: Use Lamport timestamps for a compact total order consistent with causality. Use hybrid logical clocks when physical-time locality and causal order both matter. Use version vectors when concurrent histories must remain distinguishable.
  - **How**: Increment a local counter, incorporate observed remote timestamps, and compare `(counter, node_id)` pairs for Lamport order.

- **Consensus**
  - **When to use**: Use it when nodes must decide one value, commit one transaction outcome, or maintain one replicated log.
  - **How**: Require uniform agreement, integrity, and termination. Use a leader and a quorum to order proposals, and use terms or epochs to reject stale leaders.

- **Coordination services**
  - **When to use**: Use ZooKeeper, etcd, or a similar service for small authoritative state such as leases, configuration, work allocation, and service discovery.
  - **How**: Keep the coordination state small. Use linearizable operations and watch for changes. Do not use the service as a general data store.

## Key Concepts

- **Linearizability**: A recency guarantee that makes operations appear atomic on one copy.
- **Strict serializability**: Serializable transactions plus linearizable recency.
- **CAP theorem**: A result about linearizability and availability during network partitions.
- **Logical clock**: An event-counting algorithm that orders events without measuring wall time.
- **Lamport timestamp**: A causality-consistent total-order timestamp.
- **Hybrid logical clock**: A timestamp that combines physical-time information with logical advancement.
- **Consensus**: Agreement among nodes on one result despite failures.
- **Term or epoch**: A monotonically increasing leadership period that fences old leaders.
- **Quorum**: A set of votes sufficient to intersect another required set.
- **Coordination service**: A fault-tolerant service for small shared control state.

## Mental Models

- Ask whether the application needs a current value or only a causally valid value.
- Treat linearizability as a communication cost paid on every operation, not only during a fault.
- Treat logical clocks as order labels. They do not provide a fresh read or a unique physical time.
- Treat consensus as a replicated decision log. A log gives each participant the same sequence of decisions.
- Treat a coordination service as a small safety kernel. Keep large, high-throughput data outside it.

## Anti-patterns

- **Say “strong consistency” without naming a guarantee**: The phrase can mean linearizability, serializability, session guarantees, or another model.
- **Use quorum reads as a universal linearizability proof**: Delays and concurrent operations can produce a stale response.
- **Use a wall-clock timestamp as a consensus order**: Clock skew can reverse event order.
- **Read from a follower without checking leadership**: A new leader may have committed a newer value.
- **Use CAP as a product scorecard**: It ignores most faults, latency choices, and weaker consistency models.
- **Run a large workload through a coordination service**: Consensus and durable watches are expensive control mechanisms.

## Reference Tables

| Guarantee | Scope | Main promise | Does not provide |
|---|---|---|---|
| Read-after-write | Session or user | See own writes | Global recency |
| Serializability | Transactions | Equivalent to some serial order | Fresh reads |
| Linearizability | Individual objects | Fresh order by real-time completion | Multi-object transaction isolation |
| Strict serializability | Transactions and recency | Both properties | Low coordination cost |

| Tool | Orders events | Detects concurrency | Makes state current |
|---|---:|---:|---:|
| Lamport timestamp | Yes | No | No |
| Hybrid logical clock | Yes, with physical hint | No | No |
| Version vector | Partial causal order | Yes | No |
| Consensus log | Yes | Not by itself | Yes, when reads use the committed log |

## Worked Example

A chat service uses a single-node counter to assign message IDs. The counter gives unique, increasing IDs and preserves real-time order, but it is a bottleneck and a single point of failure. Sharding the counter or allocating blocks improves scale but weakens global ordering. UUIDs remove coordination but give no useful order. A Lamport timestamp gives a causal total order, but it still does not prove that a read sees the latest message.

If the service needs a globally current sequence, it needs a linearizable fetch-and-add operation, usually backed by consensus. If it needs only a causal display order, a logical clock or application-defined conversation sequence may be sufficient.

## Key Takeaways

1. Name the exact consistency and isolation guarantees that the application needs.
2. Use linearizability for hard uniqueness, leader authority, and cross-channel recency.
3. Use logical clocks to order events, not to replace consensus.
4. Expect a consistency and availability trade-off during partitions.
5. Use consensus for a small authoritative log or decision, not for every data path.
6. Measure latency because linearizability costs communication even when no fault occurs.

## Connects To

- **Chapter 6**: Replication models differ in their ability to provide linearizability.
- **Chapter 7**: Shard ownership and request routing need coordination.
- **Chapter 8**: Serializable transactions and linearizable operations solve different problems.
- **Chapter 9**: Consensus assumptions depend on network, clock, and process fault models.
- **Chapter 13**: Uniqueness and end-to-end correctness determine where consensus remains necessary.
