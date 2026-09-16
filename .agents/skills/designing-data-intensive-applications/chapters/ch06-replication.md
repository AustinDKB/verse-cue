# Chapter 6: Replication

## Core Idea
Replication keeps copies of the same data on several machines. It improves availability, durability, read capacity, geographic locality, and disconnected operation, but it introduces lag, conflicts, and failure modes.

Choose a replication model by the guarantees the application needs. Single-leader replication orders writes through one leader. Multi-leader replication accepts writes at several leaders. Leaderless replication uses quorum reads and writes plus conflict repair.

## Frameworks Introduced

- **Single-leader replication**
  - **When to use**: Use it when one ordered write stream and a simple consistency model matter.
  - **How**: Send writes to the leader. Append changes to a replication log. Apply the log in order on followers. Route reads to the leader or to followers when stale results are permitted.
  - **Failure mode**: Failover must prevent split brain. Asynchronous failover can lose acknowledged writes.

- **Synchronous, asynchronous, and semisynchronous replication**
  - **When to use**: Select synchronous replication for a durability bound. Select asynchronous replication for write availability and lower latency. Use semisynchronous replication when at least one follower must confirm each write.
  - **How**: Define which replicas must acknowledge before the leader reports success. Monitor lag and replace a slow synchronous follower.

- **Session guarantees**
  - **When to use**: Use read-after-write consistency when users must see their own updates. Use monotonic reads when a user must not see time move backward. Use consistent prefix reads when causal order must remain visible.
  - **How**: Route a user's reads to a suitable replica, track a log position, or wait until a replica reaches the required position.

- **Multi-leader replication**
  - **When to use**: Use it for multi-region writes, offline operation, or local writes during an inter-region outage.
  - **How**: Let each leader accept writes and asynchronously exchange changes. Define conflict detection and resolution before deployment.

- **Leaderless replication and quorums**
  - **When to use**: Use it when the system must keep accepting requests despite node or network faults.
  - **How**: Write to `w` of `n` replicas and read from `r` replicas. The usual quorum condition is `w + r > n`. Treat this as a likelihood of a fresh read, not a complete linearizability guarantee.

- **Causal versioning**
  - **When to use**: Use version numbers or version vectors when concurrent writes need explicit detection.
  - **How**: Record the state on which each write depends. Overwrite causally older values. Retain concurrent values as siblings until a merge function resolves them.

## Key Concepts

- **Replica**: A node that stores a copy of a dataset or shard.
- **Leader**: The replica that accepts ordered writes in a single-leader model.
- **Follower**: A read replica that applies changes from a leader.
- **Replication log**: An ordered stream of data changes used to update replicas.
- **Replication lag**: The delay between a write on the leader and its application on a follower.
- **Read-after-write consistency**: A user sees updates that the user submitted.
- **Monotonic reads**: A user never reads an older state after reading a newer state.
- **Consistent prefix reads**: Readers observe causally ordered writes in the same order.
- **Quorum**: A required number of successful replica responses for a read or write.
- **Version vector**: A per-replica version set that records causal dependencies.

## Mental Models

- Think of replication as a choice between **order**, **availability**, and **conflict work**.
- Treat a follower as a delayed view unless the system proves a stronger read guarantee.
- Treat a backup as historical recovery. Replication mirrors deletes, but a backup can restore an earlier state.
- Treat failover as a correctness operation, not only an availability operation. The old leader must lose authority before it can accept writes again.
- Treat asynchronous replication as a queue with unbounded delay. Design the application behavior for minutes or hours of lag.

## Anti-patterns

- **Use replicas as backups**: Replication copies accidental deletes and corrupt writes. Keep independent historical backups.
- **Read from random followers without session rules**: A user can see an update disappear or see a reply before its question.
- **Assume `w + r > n` proves linearizability**: Concurrent quorum operations and read repair can still return stale values.
- **Promote any reachable follower**: An old follower can lose recent writes and reuse identifiers.
- **Use last-write-wins without a conflict policy**: Clock skew can discard a valid write, and the lost write cannot be reconstructed.
- **Replicate statements without checking determinism**: Time, random values, triggers, and order-sensitive updates can diverge across replicas.

## Reference Tables

| Model | Writes | Read behavior | Main strength | Main cost |
|---|---|---|---|---|
| Single leader | One leader | Leader or possibly stale followers | Simple ordering | Failover and leader bottleneck |
| Multi leader | Several leaders | Local reads can be fast | Multi-region and offline writes | Conflict resolution |
| Leaderless | Several replicas | Quorum or best responses | Fault and latency tolerance | Stale reads, repair, conflicts |

| Guarantee | Application promise | Typical implementation |
|---|---|---|
| Read-after-write | See your own update | Leader read, session position, or wait for replica catch-up |
| Monotonic reads | Do not move backward | Sticky user-to-replica routing or replica position tracking |
| Consistent prefix reads | Preserve causal order | Same shard for causal writes or causal metadata |

## Worked Example

A three-replica leaderless store uses `n = 3`, `w = 2`, and `r = 2`. A write succeeds after two replicas acknowledge. A read queries two replicas and chooses the value with the highest version. If one replica is down, reads and writes can continue. When it returns, read repair, hinted handoff, and anti-entropy copy missed data to it.

This design still needs conflict handling. If two clients write the same key without seeing each other, the replicas can observe the writes in different orders. A version vector marks the writes as concurrent. A merge function, manual review, or a CRDT creates the final value.

## Key Takeaways

1. Pick replication for explicit availability, durability, latency, and read-scale goals.
2. Define the user-visible consistency guarantee before routing reads to asynchronous replicas.
3. Keep backups independent from replicas.
4. Make failover fence the old leader and select the most current candidate.
5. Treat quorum math as an availability and freshness tool, not a substitute for consensus.
6. Design conflict detection and repair before choosing multi-leader or leaderless replication.

## Connects To

- **Chapter 7**: Sharding applies replication choices separately to each shard.
- **Chapter 8**: Transactions define atomicity and isolation within and across replicas.
- **Chapter 9**: Network faults, clocks, and process pauses explain replication failures.
- **Chapter 10**: Consensus provides safe leader election and linearizable coordination.
- **Chapter 12**: Change streams and event logs carry replication and data-integration updates.
