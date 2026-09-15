# Chapter 13: A Philosophy of Streaming Systems

## Core Idea
A data system can integrate specialized components by representing state changes as durable streams and deriving read models from them. This approach separates application code, stored state, and dataflow. It supports reprocessing, multiple projections, offline clients, and auditability, but it does not remove the need for coordination where a hard constraint spans concurrent writers.

The chapter applies end-to-end reasoning. A local component can make a promise only within its failure boundary. The complete system must validate identity, duplicates, ordering, constraints, timeliness, and integrity at the point where the result matters.

## Frameworks Introduced

- **Derived data and data integration**
  - **When to use**: Use derived data when several tools need different read or write shapes.
  - **How**: Keep a source log or database. Derive indexes, caches, warehouses, search stores, and client views through explicit dataflows. Rebuild a view when code or schema changes.
  - **Trade-off**: Multiple views increase operational work but reduce coupling between specialized systems.

- **Batch and stream unification**
  - **When to use**: Use one derivation model for historical rebuilds and live updates.
  - **How**: Treat batch as processing a bounded prefix and stream as processing an unbounded continuation. Use the same transformation where possible.
  - **Trade-off**: A unified model needs stable event schemas, replayable input, and deterministic or versioned logic.

- **Unbundled database**
  - **When to use**: Use separate storage technologies when workloads need different indexes, layouts, or latency profiles.
  - **How**: Connect components through durable logs and materialized views. Make ownership, replay, monitoring, and schema contracts explicit.
  - **Trade-off**: The application team owns integration and consistency behavior that an integrated database might provide.

- **Application as a derivation function**
  - **When to use**: Use this model when state can be derived from commands, events, or prior state.
  - **How**: Define application logic as a function that consumes input and emits state changes. Store state separately so the logic can be replaced and replayed.

- **End-to-end argument**
  - **When to use**: Use it when lower layers claim exactly-once delivery, durability, or integrity.
  - **How**: Trace the full operation from client intent to final effect. Add request identity, duplicate suppression, validation, and audit records at the endpoint that needs the guarantee.

- **Coordination avoidance**
  - **When to use**: Avoid coordination when constraints can tolerate temporary divergence or can be repaired later.
  - **How**: Partition work so each shard owns independent decisions. Use compensation, reconciliation, or a loosely interpreted constraint where business policy permits it.
  - **Boundary**: Hard uniqueness and mutually exclusive claims need consensus or an equivalent linearizable authority.

- **Auditable data systems**
  - **When to use**: Use auditability when software bugs, policy disputes, or regulatory review require an explanation of a result.
  - **How**: Preserve input events, code versions, validation results, decisions, and derived outputs. Add independent integrity checks and reconciliation.

## Key Concepts

- **Derived data**: Data produced from another dataset or event stream.
- **Dataflow**: A directed set of transformations that moves data between components.
- **Materialized view**: A stored result optimized for a read pattern.
- **Unbundled database**: A composition of specialized storage and processing components.
- **End-to-end argument**: A function is reliable only when the complete path enforces its required property.
- **Duplicate suppression**: Detecting repeated request identities before repeating an effect.
- **Idempotent effect**: An effect that remains correct when applied more than once.
- **Coordination avoidance**: Designing work so independent operations do not need synchronous agreement.
- **Timeliness**: Whether a result arrives before its business deadline.
- **Integrity**: Whether a result satisfies its correctness rules and can be trusted.
- **Auditability**: The ability to explain and verify how a result was produced.

## Mental Models

- Think of an event log as a durable interface between producers and many derived views.
- Think of application code as a versioned function over data, not as the only place where state exists.
- Separate freshness from correctness. A late result can be correct but useless, while a fast result can be wrong.
- Push guarantees to the end of the path. A transport guarantee does not prove an external side effect occurred once.
- Use consensus only where concurrent decisions must agree. Avoid global order for independent work.

## Anti-patterns

- **Replace one monolithic database with unowned components**: Unbundling without contracts moves hidden coupling into operations.
- **Trust exactly-once claims across system boundaries**: A database, broker, and client each have different failure and retry scopes.
- **Use a global total order for all events**: Global coordination creates a bottleneck and does not add causality for unrelated events.
- **Assume a unique request ID alone makes a transfer safe**: The ID must participate in the same durable transaction as the effect or a compensating design.
- **Drop source events after building a view**: Reprocessing and audit require durable source history.
- **Treat a model output as neutral truth**: Data and feedback loops can encode bias and cause unequal effects.

## Code Examples

```sql
ALTER TABLE requests ADD UNIQUE (request_id);
BEGIN TRANSACTION;
INSERT INTO requests (request_id, from_account, to_account, amount)
VALUES ('0286FDB8-D7E1-423F-B40B-792B3608036C', 4321, 1234, 11.00);
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;
UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;
COMMIT;
```

- **What it demonstrates**: Request identity and the effect share one transaction, so a retry cannot apply the transfer twice.

## Reference Tables

| Requirement | Local technique | System-level boundary |
|---|---|---|
| At-most-once effect | Idempotent operation | Durable request identity at the receiver |
| Rebuildable view | Replayable log | Retained input and versioned derivation code |
| Low coordination | Per-shard ownership | Compensation and reconciliation |
| Hard uniqueness | Local unique index | Linearizable authority or consensus |
| Fresh result | Incremental view | Timeliness monitor and late-result policy |
| Explainable result | Audit log | Integrity checks and code/data lineage |

## Worked Example

A client submits a money transfer and loses the response. It retries the same request. The service inserts the request ID into a table with a uniqueness constraint and updates both account balances in one transaction. The first attempt commits the request and balances. The retry fails or becomes a no-op when the request ID already exists.

If the broker, database, and client each claim exactly-once behavior but the request ID is not stored with the balances, a crash between those operations can still duplicate or omit the transfer. The end-to-end design places duplicate suppression beside the final state change.

## Key Takeaways

1. Use durable streams to connect specialized stores and derive views.
2. Reuse transformations for historical batch rebuilds and live stream updates.
3. Keep source events, derivation code versions, and output lineage for replay and audit.
4. Define exactly-once at the final effect, not at an intermediate transport.
5. Avoid coordination for independent work, but use consensus for hard uniqueness.
6. Measure timeliness and integrity as separate correctness dimensions.

## Connects To

- **Chapter 5**: Dataflow requires compatible schemas and safe evolution.
- **Chapter 8**: Transactions implement duplicate suppression and atomic effects.
- **Chapter 10**: Linearizability and consensus enforce uniqueness and shared order.
- **Chapter 11**: Batch rebuilds provide a recovery path for derived state.
- **Chapter 12**: Event logs, stream joins, and materialized views implement the dataflows.
- **Chapter 14**: Auditability and data governance address social effects of derived systems.
