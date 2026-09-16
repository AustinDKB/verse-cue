# Chapter 5: Encoding and Evolution

## Core Idea
Data outlives the code that wrote it, and old and new processes often coexist during rolling upgrades, client lag, or asynchronous delivery. Encoding is therefore an architectural boundary, not a serialization detail. Choose formats and schema rules that preserve backward compatibility (new code reads old data) and forward compatibility (old code reads new data), then apply those rules consistently across databases, APIs, workflows, and messages.

## Frameworks Introduced
- **Backward and forward compatibility**:
  - **Backward** — newer readers understand data written by older writers.
  - **Forward** — older readers tolerate data written by newer writers, usually by ignoring unknown additions.
  - **When to use**: Any persistent or networked boundary where versions cannot change atomically.
  - **How**: Add optional fields, preserve unknown data when rewriting, reserve removed identifiers, and test reader/writer pairs before deployment.
- **Protocol Buffers schema evolution**: Field tags, not names, identify encoded fields.
  - **When to use**: Compact cross-language RPC or records with a deliberately managed schema.
  - **How**: Never reuse a tag; add fields with new tags; let old readers skip unknown fields; use defaults for missing fields; be cautious when changing types.
- **Avro writer/reader schemas**: The writer’s schema describes the bytes; the reader’s schema describes the expected view. Schema resolution matches fields by name and applies defaults.
  - **When to use**: Large files, dynamic schemas, data pipelines, and systems with a schema registry.
  - **How**: Give added/removed fields defaults, store a schema version or schema with the data, and check compatibility centrally.
- **Modes of dataflow**: Databases send data to future or concurrent readers; services exchange requests/responses; brokers deliver asynchronous messages; workflows coordinate durable tasks.
- **Durable execution**: Record workflow calls and state changes so failed tasks can replay without repeating successful effects.
  - **When to use**: Multi-service workflows such as payment processing where a database transaction cannot span external services.
  - **How**: Keep workflow code deterministic, version long-lived workflows, and require idempotent external APIs.

## Key Concepts
- **Encoding/decoding** — converting in-memory structures to/from self-contained bytes.
- **Schema evolution** — changing a data schema while retaining compatibility with existing data and code.
- **Rolling upgrade** — replacing service instances gradually, allowing old and new versions to run together.
- **Field tag** — stable numeric identifier for a Protocol Buffers field.
- **Writer’s schema** — schema used to encode a record.
- **Reader’s schema** — schema used to interpret a record, potentially different from the writer’s.
- **Schema registry** — versioned schema store that documents and validates compatibility.
- **REST/RPC** — request/response service styles; RPC should not pretend network calls are local functions.
- **Idempotence** — repeating an operation has the same intended effect as performing it once.
- **Message broker** — intermediary that buffers, redelivers, and distributes asynchronous byte messages.
- **Deterministic replay** — re-executing workflow code with the same inputs produces the same recorded effects.

## Mental Models
- **Database as a message to your future self**: Persistent data must remain readable after deployment and across years of historical formats.
- **Unknown fields are cargo**: A proxy or old reader should preserve fields it cannot interpret when it writes data back.
- **Network calls are not function calls**: They can time out after the server acted, vary wildly in latency, and require deduplication on retry.
- **Compatibility is directional**: Decide which side upgrades first and test the required direction; databases and brokers commonly need both.
- **Log intent, derive state**: Durable workflows and event-driven systems record enough history to recover, retry, or rebuild safely.

## Anti-patterns
- **Language-native serialization across boundaries**: It couples data to one language, may permit dangerous class instantiation, and often lacks evolution guarantees.
- **Reuse a Protocol Buffers tag**: Old data can be decoded as the wrong field; reserve removed tags permanently.
- **Add a required Avro field without a default**: Readers using the new schema cannot decode records written before the field existed.
- **Treat RPC as local invocation**: A timeout does not reveal whether the server acted; retries can duplicate side effects.
- **Change durable workflow code in place**: Replays can diverge when call order or nondeterministic behavior changes; version existing executions.

## Code Examples
Protocol Buffers uses stable numeric tags:

```protobuf
syntax = "proto3";
message Person {
  string user_name = 1;
  int64 favorite_number = 2;
  repeated string interests = 3;
}
```

An Avro schema identifies fields by name and supplies a default for an optional value:

```json
{
  "type": "record",
  "name": "Person",
  "fields": [
    {"name": "userName", "type": "string"},
    {"name": "favoriteNumber", "type": ["null", "long"], "default": null},
    {"name": "interests", "type": {"type": "array", "items": "string"}}
  ]
}
```

## Reference Tables

| Format | Compatibility mechanism | Strength | Main caution |
|---|---|---|---|
| JSON/XML/CSV | Convention or optional schema | Human-readable, broadly interoperable | Ambiguous types, verbose data, manual evolution |
| Protocol Buffers | Stable field tags; unknown fields skipped | Compact, code generation, explicit rules | Tags cannot be reused; type changes need care |
| Avro | Writer/reader schema resolution by field name | Compact, dynamic schema generation, file-friendly | Reader needs writer schema; defaults govern compatibility |
| Language-native format | Runtime object metadata | Convenient inside one transient process | Language lock-in, security risk, weak evolution |

| Dataflow | Sender/reader relationship | Compatibility concern |
|---|---|---|
| Database | Writer to current/future readers; mixed versions | Usually both backward and forward |
| REST/RPC | Client request and server response | Commonly old clients must keep working; IDLs help |
| Message broker | Asynchronous producer to consumers | Consumers may lag for a long time; preserve unknown fields |
| Durable workflow | Recorded calls replayed after failure | Deterministic code, versioning, idempotent external effects |

## Worked Example
During a rolling upgrade, old and new service instances read and write the same database. A new version adds `favorite_number`: new readers use a default when reading old records, while old readers skip the unknown field and must not discard it when rewriting a record. Protocol Buffers makes this safe if the new field receives a never-before-used tag. Avro makes it safe if the reader has a default and can obtain the writer’s schema. The same principle applies to a payment workflow: a durable engine may replay a failed activity, so the credit-card gateway must accept an idempotency key. Existing workflow executions should continue using their old deterministic call sequence while new executions use a versioned implementation.

## Key Takeaways
1. Design encodings for coexistence, not only for the current process version.
2. Add optional fields; preserve unknown fields; never reuse stable identifiers.
3. Maintain a schema registry or equivalent compatibility check for shared data.
4. Make external side effects idempotent because timeouts make duplicate execution possible.
5. Treat APIs, brokers, and workflow histories as long-lived data boundaries.
6. Prefer frequent, reversible, independently deployable changes over synchronized migrations.

## Connects To
- **Ch 1**: Encodings enable independent evolution of operational, analytical, and derived systems.
- **Ch 2**: Rolling upgrades and durable recovery support evolvability and reliability requirements.
- **Ch 3**: Data models need compatible representations as their schemas and projections change.
- **Ch 4**: WALs, SSTables, archival files, and column formats all depend on durable encoding choices.
