# Chapter 7: Sharding

## Core Idea
Sharding splits a dataset across machines so that one node does not need to hold or process everything. Replication can protect each shard, but sharding itself adds routing, rebalancing, cross-shard transaction, and secondary-index complexity.

The central design question is whether the partition key spreads data and work evenly while keeping important queries local. A poor key creates skew and hot spots that defeat horizontal scaling.

## Frameworks Introduced

- **Key-range sharding**
  - **When to use**: Use it when ordered range scans are important.
  - **How**: Assign each shard a contiguous range of keys. Split a range when it grows or becomes hot. Keep records sorted within the shard.
  - **Trade-off**: Sequential or nearby keys can concentrate writes in one hot shard.

- **Hash sharding**
  - **When to use**: Use it when even distribution matters more than range scans.
  - **How**: Hash the partition key and assign hash ranges or fixed shard numbers. Keep a mapping from shard to node.
  - **Trade-off**: Hashing scatters nearby keys and makes partition-key range queries inefficient.

- **Fixed-number shard rebalancing**
  - **When to use**: Use it when you can estimate the future scale and want cheap node movement.
  - **How**: Create many shards at the start. Move whole shards between nodes as nodes join or leave.
  - **Trade-off**: Resharding becomes expensive when the initial shard count is too small or shard sizes become too large.

- **Consistent hashing**
  - **When to use**: Use a consistent hashing scheme when node membership changes and key movement must stay small.
  - **How**: Map keys and shard ranges into a hash space. Split or move only affected ranges, or use rendezvous or jump consistent hashing.

- **Cell-based multitenancy**
  - **When to use**: Use cells when tenant isolation, data residence, per-tenant recovery, or fault containment matters.
  - **How**: Group service and storage resources into self-contained cells. Assign tenants to cells and move them as size or policy changes.
  - **Trade-off**: Cross-tenant queries and large-tenant growth need extra design.

- **Local and global secondary indexes**
  - **When to use**: Use a local index when writes must stay on the primary-key shard. Use a global index when searches must find records in one index shard.
  - **How**: A local index stores entries with the record. A global index shards entries by the indexed term and updates several shards when a record changes.
  - **Trade-off**: Local reads fan out. Global writes need coordination and may expose stale entries.

## Key Concepts

- **Shard**: A subset of records managed as a small database.
- **Partition key**: The key used to choose a shard.
- **Skew**: Uneven data or request distribution across shards.
- **Hot shard**: A shard with disproportionate load.
- **Hot key**: A key that receives disproportionate requests or writes.
- **Rebalancing**: Moving shard ownership to distribute load.
- **Request routing**: Sending a request to a node that owns the target shard.
- **Local secondary index**: An index that covers only records in one primary-key shard.
- **Global secondary index**: An index that covers records from all primary-key shards.
- **Cell**: An isolated group of services and storage for a tenant set.

## Mental Models

- Treat the partition key as a query contract. A query without that key may become a cluster-wide operation.
- Treat sharding and replication as separate axes. A shard owns a record, while replicas copy that shard.
- Prefer locality for frequent queries, but measure whether locality creates a hot spot.
- Treat rebalancing as a production workload. It consumes disk, network, CPU, and write capacity while normal traffic continues.
- Treat a secondary index as another distributed dataset. Its update path needs the same correctness analysis as the primary data.

## Anti-patterns

- **Shard by an increasing timestamp**: New writes land in one range and create a hot shard.
- **Use `hash(key) % node_count`**: Adding one node remaps most keys and causes excessive movement.
- **Choose the shard count without growth estimates**: Too few shards force expensive resharding. Too many small shards add overhead.
- **Fan out every secondary-index query without measuring tail latency**: More shards amplify the slowest response.
- **Hide cross-shard writes inside application code**: Partial success can leave related records inconsistent.
- **Automate failure detection and rebalancing without limits**: A slow node can trigger a cascading overload.

## Reference Tables

| Scheme | Data layout | Range query | Hot-spot risk | Rebalance method |
|---|---|---|---|---|
| Key range | Sorted key intervals | Efficient | High for nearby writes | Split or merge ranges |
| Hash range | Sorted hash intervals | Poor by original key | Lower for uniform keys | Split or merge hash ranges |
| Fixed hash shards | `hash(key) % shard_count` | Poor | Low if keys are uniform | Move whole fixed shards |
| Rendezvous or jump hash | Hash-based node choice | Poor | Depends on workload | Reassign affected keys |

| Index type | Write path | Read path without partition key | Main concern |
|---|---|---|---|
| Local | One primary shard | Query all shards | Fan-out and tail latency |
| Global | Primary plus index shards | Query the index shard | Cross-shard consistency and stale index entries |

## Worked Example

A sensor service stores measurements with a timestamp. Key-range sharding by timestamp gives efficient monthly scans, but all current writes go to the shard for the current month. Prefixing the key with a sensor ID spreads writes across sensors, but a query for all sensors in a month must issue one range query per sensor.

A social service has a different problem. One celebrity key receives millions of requests. Adding random suffixes spreads writes across many keys. Reads must then gather all suffixes, so the service applies this technique only to tracked hot keys and maintains metadata for their split state.

## Key Takeaways

1. Shard only after one node cannot meet data or write-throughput needs.
2. Choose a partition key from access patterns, not only from schema shape.
3. Separate even distribution from query locality and measure both.
4. Plan shard movement, ownership metadata, and cutover behavior before scale-up.
5. Select local or global secondary indexes from read fan-out and write coordination needs.
6. Keep cross-shard operations rare, explicit, and observable.

## Connects To

- **Chapter 6**: Replicate each shard for availability and durability.
- **Chapter 8**: Cross-shard transactions need distributed transaction protocols.
- **Chapter 10**: Coordination services provide authoritative shard ownership and routing data.
- **Chapter 11**: Analytical queries often aggregate data from many shards in parallel.
