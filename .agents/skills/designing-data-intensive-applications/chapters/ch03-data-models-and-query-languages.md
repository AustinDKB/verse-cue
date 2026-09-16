# Chapter 3: Data Models and Query Languages

## Core Idea
A data model is not just storage syntax: it shapes the concepts the application can express and the queries it can perform. Choose the model whose relationship structure, locality, update pattern, and evolution needs match the domain. Declarative query languages preserve that choice as an abstraction, allowing the engine to optimize execution without changing application intent.

## Frameworks Introduced
- **Layered data models**: Model the domain in application objects and APIs, map it to a general-purpose model (relational, document, graph, or event log), then let the storage engine map that model to bytes.
  - **When to use**: Evaluate whether an abstraction hides useful complexity without hiding necessary trade-offs.
  - **How**: Keep boundaries explicit; avoid leaking storage representation into every application decision.
- **Relational vs. document models**: Relational tables and joins suit shared, many-to-many data; documents suit tree-shaped one-to-many data commonly loaded as a unit.
  - **When to use**: Use embedding for bounded, document-like data with read locality; use references/joins for shared entities, large collections, and relationships queried in multiple directions.
  - **How**: Decide from access patterns and update frequency, not from “SQL versus NoSQL” identity.
- **Normalization vs. denormalization**: Normalize authoritative facts to avoid update anomalies; denormalize selectively as derived data when read performance justifies write and consistency work.
- **Star, snowflake, and one-big-table schemas**: Model analytical facts as events with dimension references; normalize dimensions for structure or flatten them for simpler/faster reads.
- **Graph models**: Property graphs and triple stores make arbitrary many-to-many paths first-class; Cypher, SPARQL, SQL recursion, and Datalog express traversals at different levels of convenience.
- **Event sourcing and CQRS**: Append immutable domain events as the write-side source of truth and derive multiple read-optimized projections.
  - **When to use**: A domain has complex state transitions, audit requirements, or many competing read representations.
  - **How**: Validate commands first, append past-tense facts, replay events to rebuild projections, and keep side effects idempotent.

## Key Concepts
- **Declarative query** — states the result pattern, leaving indexes, joins, and execution order to the optimizer.
- **Relational model** — unordered tables of rows with explicit relationships and joins.
- **Document model** — self-contained JSON-like records, often with nested one-to-many data.
- **Object-relational impedance mismatch** — translation friction between in-memory objects and relational tables.
- **Normalization** — store each meaningful fact once and refer to it by an identifier.
- **Denormalization** — duplicate or precompute data to reduce joins and accelerate reads.
- **Data locality** — placing data fetched together physically or logically close together.
- **Star schema** — a fact table surrounded by denormalized dimension tables.
- **Property graph/triple store** — vertices and labeled edges/properties, or subject-predicate-object facts.
- **Materialized view/projection** — a stored result derived from source data for a read pattern.

## Mental Models
- **Relationship shape decides the model**: trees favor embedding; shared entities and many-to-many paths favor references or graphs.
- **Read/write asymmetry**: normalization makes authoritative writes safer; denormalization makes repeated reads cheaper but creates synchronization work.
- **Schema-on-read is not no schema**: if the database does not enforce a schema, the application still carries an implicit one.
- **Events explain intent**: “booking canceled” communicates more than a collection of row mutations; projections can be rebuilt from the intent-bearing log.
- **Query language fit matters**: a concise traversal language can prevent an awkward, error-prone collection of recursive joins.

## Anti-patterns
- **Embed unbounded collections**: A document containing thousands or millions of child records becomes expensive to read and update.
- **Normalize or denormalize by ideology**: Both are trade-offs; choose per field according to change frequency, read shape, skew, and consistency needs.
- **Assume an ORM hides the database**: ORMs can create N+1 queries, inefficient schemas, and leaky abstractions; inspect generated queries and retain SQL fluency.
- **Call JSON “schemaless”**: Old and new shapes still require compatibility logic, validation, and migration discipline.
- **Use event sourcing without replay discipline**: Projections, event ordering, schema evolution, log growth, and external side effects require deliberate operations.

## Code Examples
A property graph can be represented with indexed relational tables:

```sql
CREATE TABLE vertices (
  vertex_id integer PRIMARY KEY,
  label text,
  properties jsonb
);
CREATE TABLE edges (
  edge_id integer PRIMARY KEY,
  tail_vertex integer REFERENCES vertices (vertex_id),
  head_vertex integer REFERENCES vertices (vertex_id),
  label text,
  properties jsonb
);
CREATE INDEX edges_tails ON edges (tail_vertex);
CREATE INDEX edges_heads ON edges (head_vertex);
```

A graph traversal is concise in Cypher because variable-length paths are first-class:

```cypher
MATCH (person)-[:BORN_IN]->()-[:WITHIN*0..]->(:Location {name:'United States'}),
      (person)-[:LIVES_IN]->()-[:WITHIN*0..]->(:Location {name:'Europe'})
RETURN person.name
```

## Reference Tables

| Model | Strong fit | Main cost or risk |
|---|---|---|
| Relational | Shared entities, joins, many-to-many relationships, integrity | Joins and schema migrations can be cumbersome at extreme scale |
| Document | Bounded tree, whole-record reads, locality, heterogeneous records | Unbounded nesting, duplicated references, weak joins |
| Star schema | BI aggregates over historical facts and dimensions | Large fact tables; ETL/modeling discipline required |
| Property graph / triples | Variable-depth traversal and rich many-to-many relationships | Specialized query/indexing and operational tooling |
| Event log + projections | Auditing, complex state transitions, multiple read models | Replay, ordering, projection lag, event/schema management |

## Worked Example
A résumé can be a single document when a profile, its few positions, education entries, and contact information are normally read together. A region should usually be referenced by `region_id`: the name, localization, and geography are shared facts that should change once. A social post’s timeline projection should store post and sender IDs rather than copying mutable text, likes, and profile data; the read path hydrates those IDs. Conversely, a warehouse can use a star schema: `fact_sales` records each purchase while dimensions describe product, store, date, promotion, and customer. The same domain therefore uses embedding, references, and analytical denormalization at different boundaries.

## Key Takeaways
1. Treat the data model as a domain language, not a persistence afterthought.
2. Embed bounded one-to-many data when locality and aggregate ownership matter.
3. Use normalized references for shared or frequently changing facts; derive denormalized views for specific reads.
4. Choose graphs when variable-depth, many-to-many traversal is central to the product.
5. Use event sourcing/CQRS when immutable intent and rebuildable projections outweigh operational complexity.
6. Prefer declarative queries that state intent and let the engine optimize execution.

## Connects To
- **Ch 1**: Maps operational, analytical, and derived-data roles to concrete models.
- **Ch 4**: Storage engines and indexes implement the access patterns selected here.
- **Ch 5**: Data models must evolve while old and new encodings coexist.
- **Ch 11–12**: Data integration, logs, streams, and materialized views maintain derived representations.
