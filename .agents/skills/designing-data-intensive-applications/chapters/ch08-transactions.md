# Chapter 8: Transactions

## Core Idea
A transaction groups reads and writes so that the database preserves a defined set of invariants despite errors, concurrency, and crashes. The useful question is not whether a database supports ACID as a label, but which atomicity, consistency, isolation, and durability guarantees it provides.

Weak isolation can improve throughput, but application correctness must account for dirty reads, dirty writes, lost updates, write skew, and phantoms. Serializability gives the strongest general isolation. Distributed commit adds a second failure problem because participants can remain uncertain after a coordinator fails.

## Frameworks Introduced

- **ACID as four separate guarantees**
  - **Atomicity**: A transaction commits all its intended changes or none of them.
  - **Consistency**: Every committed transaction preserves application invariants. The database cannot define all business rules.
  - **Isolation**: Concurrent transactions behave according to the selected isolation model.
  - **Durability**: A committed transaction survives a crash, subject to the system's storage and replication guarantees.

- **Read committed**
  - **When to use**: Use it when dirty reads and dirty writes are unacceptable, but full serializability is not needed.
  - **How**: Hide uncommitted writes and prevent concurrent transactions from overwriting uncommitted data. It still permits nonrepeatable reads and write skew.

- **Snapshot isolation and MVCC**
  - **When to use**: Use it for consistent reads with good read/write concurrency.
  - **How**: Give each transaction a snapshot. Store multiple row versions. A transaction reads versions visible at its snapshot and writes a new version.
  - **Failure mode**: Snapshot isolation alone does not prevent write skew or all lost-update patterns.

- **Lost-update prevention**
  - **When to use**: Use it for read-modify-write operations on shared objects.
  - **How**: Use an atomic update, an explicit lock, automatic conflict detection, or a conditional write such as compare-and-set.

- **Serializable execution**
  - **When to use**: Use it when concurrent transactions must preserve invariants across multiple objects.
  - **How**: Run transactions one at a time, use two-phase locking, or detect conflicts with serializable snapshot isolation.
  - **Trade-off**: Stronger isolation increases blocking, aborts, coordination, or resource cost.

- **Two-phase commit (2PC)**
  - **When to use**: Use it when several resource managers must make one atomic commit decision.
  - **How**: The coordinator asks participants to prepare. If all promise to commit, the coordinator sends commit. A participant must retain locks and prepared state while it waits for the decision.
  - **Failure mode**: Coordinator failure can leave participants blocked. 2PC is a commit protocol, not two-phase locking.

## Key Concepts

- **Transaction**: A group of operations with a commit or abort outcome.
- **Dirty read**: A transaction reads data written by an uncommitted transaction.
- **Dirty write**: A transaction overwrites data written by an uncommitted transaction.
- **Lost update**: A later write silently replaces an earlier concurrent update.
- **Write skew**: Two transactions update different rows after reading a shared condition, breaking an invariant.
- **Phantom**: A newly inserted or removed row changes the result of a predicate query.
- **MVCC**: Multiversion concurrency control, which stores several versions for concurrent visibility.
- **Serializable**: An isolation property equivalent to some serial transaction order.
- **Predicate lock**: A lock on rows that match a condition, including future matching rows.
- **Two-phase commit**: A coordinator protocol that separates prepare from commit.

## Mental Models

- Treat an invariant as a proof obligation. Ask which reads and writes must conflict to protect it.
- Treat snapshot isolation as a stable view, not as a complete serializability guarantee.
- Treat a transaction boundary as a correctness boundary. If a state change crosses that boundary, partial failure becomes visible.
- Treat a prepared participant as uncertain. It cannot safely release locks until the coordinator resolves the outcome.
- Prefer single-object atomic operations when they express the invariant. They need less coordination than multi-object transactions.

## Anti-patterns

- **Call ACID a complete design**: The words do not state which isolation, durability, or business constraints the system provides.
- **Use read-modify-write without protection**: Concurrent updates can overwrite each other.
- **Assume snapshot isolation prevents write skew**: Transactions can read the same premise and write separate rows.
- **Use application checks without a transaction**: A check and a write can interleave with another request.
- **Treat 2PC as a speed optimization**: A failed coordinator can block participants and hold locks.
- **Claim exactly-once from a retrying client**: A committed operation can produce a lost response and then run again.

## Code Examples

```sql
BEGIN TRANSACTION;
SELECT * FROM figures
  WHERE name = 'robot' AND game_id = 222
  FOR UPDATE;
-- Check whether move is valid, then update the position
UPDATE figures SET position = 'c4' WHERE id = 1234;
COMMIT;
```

- **What it demonstrates**: Explicit locking makes the read-modify-write sequence exclude conflicting moves.

```sql
ALTER TABLE requests ADD UNIQUE (request_id);
BEGIN TRANSACTION;
INSERT INTO requests (request_id, from_account, to_account, amount)
VALUES ('0286FDB8-D7E1-423F-B40B-792B3608036C', 4321, 1234, 11.00);
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;
UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;
COMMIT;
```

- **What it demonstrates**: A unique request record can suppress a duplicate retry while the transfer remains atomic.

## Reference Tables

| Isolation approach | Protects | Does not automatically protect |
|---|---|---|
| Read committed | Dirty reads and dirty writes | Nonrepeatable reads, lost updates, write skew |
| Snapshot isolation | Consistent snapshot and many read anomalies | Write skew, some lost updates |
| Two-phase locking | Serializable conflicts through locks | Blocking and deadlock cost |
| Serializable snapshot isolation | Serializable result with optimistic checks | Aborts and conflict-detection cost |
| Actual serial execution | All intertransaction concurrency anomalies | Throughput for long or blocking transactions |

## Worked Example

Two doctors must remain on call for a shift. Each transaction reads that two doctors are on call. Aaliyah turns herself off call, and Bryce does the same in a concurrent transaction. Each transaction updates a different row, so snapshot isolation sees no direct row conflict. The final state has no doctor on call.

To prevent this write skew, lock the rows that satisfy the condition, use a predicate or index-range lock, serialize the operation, or materialize the conflict in a row that every transaction must update.

## Key Takeaways

1. State the invariant before selecting an isolation level.
2. Use atomic operations or locks for read-modify-write sequences.
3. Use serializability when a correctness rule spans multiple objects.
4. Distinguish 2PC from 2PL and expect coordinator failure in 2PC designs.
5. Make retries idempotent with request identifiers or a durable deduplication record.
6. Treat distributed transactions as a cost and failure boundary.

## Connects To

- **Chapter 6**: Replication changes durability, conflict behavior, and transaction visibility.
- **Chapter 7**: Sharding turns cross-shard atomicity into a distributed transaction problem.
- **Chapter 9**: Partial failures and unbounded delays make distributed commit difficult.
- **Chapter 10**: Linearizability and consensus provide other coordination tools.
- **Chapter 13**: End-to-end idempotence can reduce the need for distributed transactions.
