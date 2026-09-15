# Chapter 11: Batch Processing

## Core Idea
Batch processing reads a bounded collection of durable input and writes derived output. Its strengths come from replayable immutable input, explicit dataflow, parallel execution, and the ability to rerun a failed task. Distributed batch systems extend simple Unix pipelines with storage, scheduling, resource allocation, shuffles, joins, and fault recovery.

A useful batch system separates computation from storage and treats output as derived data. MapReduce and dataflow engines expose different levels of abstraction, but both divide work, move records by key, and combine partial results.

## Frameworks Introduced

- **Unix pipeline as dataflow**
  - **When to use**: Use it for small or local transformations that can stream through standard input and output.
  - **How**: Compose simple programs. Use sorting when grouping by key is needed. Keep input immutable so the pipeline can run again.
  - **Trade-off**: Process startup, parsing, and text formats limit scale and type safety.

- **Distributed filesystem and object store**
  - **When to use**: Use durable shared storage for large input and output collections.
  - **How**: Store immutable files or objects. Replicate or erasure-code data. Let compute tasks read local or nearby blocks when possible.
  - **Trade-off**: Object stores offer durability and low cost but add request latency and usually do not support in-place random writes.

- **MapReduce**
  - **When to use**: Use it for large parallel transformations with a clear map, shuffle, and reduce shape.
  - **How**: Map input records to key-value pairs. Partition and sort by key. Reduce each key group. Materialize output for the next job.
  - **Trade-off**: Job boundaries and materialized files add overhead but make recovery and debugging clear.

- **Dataflow engines**
  - **When to use**: Use them for multi-stage pipelines that need fused operators, better scheduling, and less intermediate materialization.
  - **How**: Represent computation as a directed graph. Partition operators by key. Shuffle only when data must move between partitions. Track lineage and rerun failed tasks.

- **Joins and grouping**
  - **When to use**: Use a sort-merge join for large inputs with compatible keys. Use a broadcast hash join when one input fits in memory on each worker.
  - **How**: Partition both inputs by join key or broadcast the small side. Group records by key. Produce joined or aggregated output.

- **Serving derived data**
  - **When to use**: Use batch output to build indexes, caches, search stores, recommendation features, and reports.
  - **How**: Write output to a new version. Validate it. Atomically switch readers to the new version or use an append-and-merge process.

## Key Concepts

- **Batch process**: A computation over bounded input.
- **Dataflow**: A graph of transformations and data movement.
- **Map**: A transformation that emits records from input records.
- **Reduce**: A transformation that combines records by key.
- **Shuffle**: Network redistribution that groups records with the same key.
- **Sort-merge join**: A join that sorts or receives both inputs by key and merges matching groups.
- **Broadcast hash join**: A join that copies a small input to every worker.
- **Lineage**: The record of how output depends on input and prior stages.
- **ETL**: Extract, transform, and load processing for derived data.
- **Data warehouse**: A query system optimized for large analytical scans and aggregates.

## Mental Models

- Treat immutable input as an experiment surface. Rerun a new program without changing the source.
- Treat a shuffle as a boundary that costs network, disk, and coordination.
- Prefer local aggregation before a shuffle to reduce network volume.
- Treat output as a materialized view that can be rebuilt from source data.
- Use the smallest computation model that exposes the needed parallelism and recovery.

## Anti-patterns

- **Mutate input files in place**: A failed job can destroy the data needed for recovery or comparison.
- **Use an in-memory aggregate for unbounded data**: Memory grows with key count and cannot survive a worker failure.
- **Shuffle without a key need**: Network redistribution becomes the main cost.
- **Send a large table through every worker for a join**: Broadcast only when the small side fits safely in memory.
- **Publish partial derived output as final**: Readers can observe an incomplete index or report.
- **Recompute expensive work without lineage or checkpoints**: One failed task can repeat the full pipeline.

## Code Examples

```bash
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
```

- **What it demonstrates**: A log record has fields that can feed a batch parser.

```python
from collections import defaultdict

counts = defaultdict(int)
with open('/var/log/nginx/access.log', 'r') as file:
    for line in file:
        url = line.split()[6]
        counts[url] += 1

top5 = sorted(((count, url) for url, count in counts.items()), reverse=True)[:5]
for count, url in top5:
    print(f"{count} {url}")
```

- **What it demonstrates**: A custom program can aggregate keys in memory, but a distributed version must partition or sort the key space.

## Reference Tables

| Model | Intermediate data | Recovery | Best fit |
|---|---|---|---|
| Unix pipeline | Stream between processes | Rerun command | Local bounded data |
| MapReduce | Materialized stage output | Rerun failed task | Large, clear batch stages |
| Dataflow engine | Fused or managed graph stages | Lineage and checkpoints | Multi-stage pipelines |
| SQL warehouse | Managed tables and query plan | Engine-specific | Interactive analytics |

| Join strategy | Requirement | Network cost | Risk |
|---|---|---|---|
| Sort-merge | Both inputs partitioned or sorted by key | Shuffle both sides | Disk and sort cost |
| Broadcast hash | One side fits on every worker | Copy small side | Memory pressure |
| Partitioned hash | Hash-partition both inputs | Shuffle both sides | Skewed keys |

## Worked Example

To find the most visited URLs in a web log, parse each line, emit `(url, 1)`, group by URL, sum each group, and select the top five. A local script stores every count in memory. A distributed job first performs local counts, shuffles partial counts by URL, sums them, and performs a final top-five selection. If one task fails, the engine reruns that task from immutable input.

## Key Takeaways

1. Keep batch input immutable and output reproducible.
2. Reduce locally before shuffling by key.
3. Choose join strategy from input size, key distribution, and memory limits.
4. Treat intermediate data and task retries as operational costs.
5. Publish derived data through a controlled version or atomic switch.
6. Use batch processing to rebuild state and validate stream-derived systems.

## Connects To

- **Chapter 4**: LSM storage, column storage, and indexes determine batch I/O cost.
- **Chapter 7**: Sharding supplies partitioning for distributed batch work.
- **Chapter 12**: Stream processing handles unbounded input and continuous updates.
- **Chapter 13**: Batch and stream processing can share dataflow and derivation principles.
