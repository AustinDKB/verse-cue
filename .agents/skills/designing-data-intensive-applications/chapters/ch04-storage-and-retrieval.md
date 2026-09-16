# Chapter 4: Storage and Retrieval

## Core Idea
Storage engines are optimized around workload shape. OLTP needs fast point reads/writes and secondary indexes; analytics needs large scans and aggregates. Log-structured engines favor sequential writes and background compaction, B-trees favor predictable indexed reads and in-place updates, and column-oriented engines minimize the data read for analytical queries. Indexes are derived structures: every read-speed gain costs storage, write work, or maintenance complexity.

## Frameworks Introduced
- **Append-only log and index**: Appending is simple and fast, but a separate index is required to avoid scanning the entire log.
  - **When to use**: Write-heavy key-value workloads or as a durability/recovery primitive.
  - **How**: Maintain an index, reclaim overwritten data, persist/rebuild index state, and choose a structure that supports the needed queries.
- **LSM-tree**: Buffer writes in an ordered memtable, flush immutable sorted-string tables (SSTables), search newest-to-oldest, and merge/compact in the background.
  - **When to use**: High write throughput, sequential I/O, immutable/object-storage-friendly segments.
  - **How**: Protect the memtable with a write-ahead log, use tombstones for deletion, Bloom filters for negative lookups, and choose compaction for the read/write mix.
- **B-tree**: Maintain a balanced tree of fixed-size pages, update pages in place, split full pages, and use a write-ahead log for crash recovery.
  - **When to use**: Predictable point/range reads, mature transactional indexing, and workloads where read latency is dominant.
  - **How**: Tune page layout, WAL durability, clustering, and secondary indexes; account for random writes and fragmentation.
- **Column-oriented analytics**: Store columns together in blocks, read only referenced columns, compress repeated values, and sort rows by common filter/group keys.
  - **When to use**: Large scans and aggregates over wide fact tables.
  - **How**: Combine column pruning, block pruning, bitmap/run-length compression, vectorized or compiled execution, and batched writes.
- **Specialized indexes**: Use multidimensional indexes for simultaneous range predicates, inverted indexes for terms, and vector indexes for semantic nearest-neighbor search.

## Key Concepts
- **Index** — a derived structure that accelerates queries but adds write and storage overhead.
- **Memtable** — an in-memory ordered write buffer in an LSM-tree.
- **SSTable** — an immutable file sorted by key, usually with a sparse index.
- **Compaction** — merging segments, retaining the newest value, and removing obsolete data.
- **Tombstone** — a deletion marker propagated through compaction.
- **Bloom filter** — a probabilistic membership test with no false negatives but possible false positives.
- **B-tree page** — fixed-size disk block containing sorted keys and child references.
- **WAL** — write-ahead log flushed before in-place pages to support crash recovery.
- **Write amplification** — physical bytes or I/O written divided by the minimum logical write.
- **Columnar storage** — layout that stores values from a column together for scan efficiency.
- **Inverted index/vector index** — term-to-document postings or embedding-to-neighbor structures.

## Mental Models
- **Read/write budget**: An index is not free; ask whether its read savings justify extra write amplification, disk, compaction, and consistency work.
- **Immutable files simplify failure**: A partial SSTable can be discarded; a partially updated B-tree needs WAL recovery.
- **Compaction is background debt**: An LSM write benchmark is misleading until compaction catches up and shares disk bandwidth with new writes.
- **Prune before compute**: Analytical performance comes from reading fewer columns/blocks and then processing the remainder efficiently.
- **Accuracy versus speed**: Flat vector search is accurate but scans everything; IVF/HNSW reduce work with approximate results and tunable recall.

## Anti-patterns
- **Index everything**: Unused indexes slow every write and consume storage; index proven query patterns.
- **Choose LSM or B-tree from a slogan**: Benchmark the real key/value sizes, overwrite rate, range queries, read/write ratio, and latency goals.
- **Ignore compaction/WAL costs**: Short tests on an empty store hide write amplification, disk pressure, and recovery behavior.
- **Use row storage for wide scans**: Loading unused columns wastes I/O and CPU in analytical workloads.
- **Confuse wide-column with column-oriented**: Wide-column/column-family systems are generally row-oriented; the names describe different ideas.

## Code Examples
The simplest append-only key-value store shows the fundamental trade-off:

```bash
db_set () { echo "$1,$2" >> database; }
db_get () { grep "^$1," database | sed -e "s/^$1,//" | tail -n 1; }
```

An LSM write/read path is conceptually:

```text
write -> WAL -> memtable -> flush as SSTable
read  -> memtable -> newest SSTables -> older SSTables
background: merge/compact SSTables; discard overwritten values and tombstones
```

## Reference Tables

| Property | LSM-tree | B-tree |
|---|---|---|
| Write pattern | Sequential immutable segments | Random in-place page updates plus WAL |
| Read pattern | Check memtable/segments; Bloom filters help misses | Traverse a small balanced page tree |
| Range queries | Sorted segments must be merged | Natural ordered leaf scan |
| Typical strength | Write-heavy throughput and compression | Predictable reads and mature transactions |
| Main maintenance | Compaction, tombstones, backpressure | WAL, page splits, fragmentation/vacuum |

| Analytical technique | Effect |
|---|---|
| Column pruning | Read only columns referenced by the query |
| Block pruning/sort order | Skip blocks outside a time/key range |
| Bitmap/run-length encoding | Compress low-cardinality repeated values and combine predicates with bit operations |
| Vectorized execution | Apply an operator to batches rather than one row at a time |
| Query compilation | Generate tight machine code for a known query plan |

## Worked Example
For a write-heavy event store, an LSM design appends each event to a WAL, keeps recent keys in a memtable, flushes sorted immutable SSTables, and compacts them as they accumulate. A Bloom filter can avoid reading most SSTables for a missing key. If reads dominate, leveled compaction limits the number of files checked; if writes dominate, size-tiered compaction may reduce rewrite pressure. For an OLTP service needing predictable point and range reads, a B-tree with a WAL may be the better starting point. For a warehouse query over a 100-column fact table that uses only `date_key`, `product_sk`, and `quantity`, column blocks and compression avoid reading the other 97 columns. If the query asks for restaurants inside a latitude/longitude rectangle, use an R-tree or similar multidimensional index rather than a simple concatenated index.

## Key Takeaways
1. Select storage structures from access patterns and durability requirements.
2. LSM-trees trade read amplification and compaction for efficient sequential writes.
3. B-trees trade random page writes and WAL work for predictable indexed reads.
4. Treat indexes, materialized views, and vector structures as derived data with lifecycle costs.
5. For analytics, minimize bytes scanned before optimizing CPU execution.
6. Measure steady-state behavior after compaction, cache effects, and failures—not only the happy path.

## Connects To
- **Ch 1**: Implements the OLTP/OLAP and derived-data separation.
- **Ch 2**: Determines response-time distributions, throughput, and scaling limits.
- **Ch 3**: Provides the physical structures behind relational, document, graph, and event models.
- **Ch 5**: WALs, immutable files, and column formats depend on durable, evolvable encodings.
