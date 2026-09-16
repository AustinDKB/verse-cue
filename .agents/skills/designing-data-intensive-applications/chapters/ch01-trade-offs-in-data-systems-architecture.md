# Chapter 1: Trade-Offs in Data Systems Architecture

## Core Idea
Data-intensive architecture has no universally best technology: the right design is the best trade-off for a workload, organization, failure model, and legal context. Start by identifying how data is created, read, transformed, and retained; then compose specialized systems only where their different guarantees are worth the added operational complexity.

## Frameworks Introduced
- **Operational systems (OLTP) vs. analytical systems (OLAP)**: Separate systems when low-latency point reads/writes and large historical scans compete for resources.
  - **When to use**: OLTP serves application users and current state; OLAP serves analysts, data scientists, and exploratory aggregates.
  - **How**: Replicate or stream operational data through ETL/ELT into a warehouse or lake. Do not let arbitrary analytical queries endanger the transactional workload.
- **System of record vs. derived data system**: Keep each fact authoritative in one canonical place; treat caches, indexes, materialized views, denormalized copies, models, and analytical datasets as reproducible derivatives.
  - **When to use**: Whenever multiple stores contain related representations of the same facts.
  - **How**: Document the source-to-derived dependency and provide a reliable update/rebuild path.
- **Cloud vs. self-hosting**: Outsource routine infrastructure when elasticity or missing operational expertise outweighs vendor lock-in, loss of control, and usage cost.
  - **When to use**: Compare predictable versus bursty load, in-house expertise, compliance, required customization, and exit options.
  - **How**: Treat cloud adoption as a workload and business decision, not as an automatic cost or reliability win.
- **Single-node vs. distributed/shared-nothing**: Distribute only for a concrete need—fault tolerance, geographic latency, elasticity, specialized hardware, legal residency, or capacity beyond one machine.
  - **When to use**: After measuring the bottleneck and its growth direction.
  - **How**: Prefer independent components and accept the network, consistency, observability, and deployment costs explicitly.
- **Data minimization**: Store personal data only for a specified purpose and only as long as necessary; storage cost includes privacy, security, liability, and reputational risk.

## Key Concepts
- **Data-intensive application** — an application whose primary engineering challenge is managing data volume, change, consistency, availability, or processing.
- **OLTP** — high-volume, low-latency operational reads and writes, usually point queries and current state.
- **OLAP** — analytical queries that scan and aggregate large historical datasets.
- **Data warehouse** — a queryable, usually relational analytical copy assembled from operational systems.
- **Data lake** — a flexible repository of raw files and varied data types without a single imposed schema.
- **ETL/ELT** — extract, transform, load; or load first and transform inside the destination.
- **Derived data** — data computed from another dataset and therefore rebuildable in principle.
- **Disaggregation** — separating storage from compute so each can scale or specialize independently.
- **Multitenancy** — serving multiple customers on shared infrastructure while isolating performance and security.
- **Reverse ETL** — sending analytical outputs, such as model predictions, back into operational systems.

## Mental Models
- **Workload before product**: classify read/write shape, latency, volume, retention, and failure requirements before naming a database.
- **Canonical fact plus projections**: ask “which store is authoritative?” and “how do I rebuild this copy?” for every duplicate representation.
- **Abstraction has a price**: a managed service hides machines and routine operations, but also hides internals and reduces control.
- **Distribution tax**: every network boundary adds failure modes, latency, coordination, consistency work, and observability requirements.

## Anti-patterns
- **One size fits all**: forcing transactions, search, streaming, and analytics into one general-purpose system creates conflicting optimization goals.
- **Running analytics on OLTP**: expensive scans can consume resources needed for user-facing writes and point reads.
- **Premature distribution**: adding microservices or sharding before a measured need increases failure and operations surface area.
- **Cloud means no operations**: cloud shifts operations toward service selection, integration, cost, security, quotas, and migration; it does not remove them.
- **Store everything “just in case”**: indefinite retention expands breach, compliance, deletion, and misuse risk.

## Reference Tables

| Decision | Prefer the first option when… | Prefer the second option when… |
|---|---|---|
| OLTP / OLAP | Interactive current-state reads and writes dominate | Historical scans and ad-hoc aggregates dominate |
| Warehouse / lake | Consumers need governed relational models and SQL | Consumers need raw, heterogeneous files or custom ML processing |
| Cloud / self-hosted | Load is bursty, expertise is scarce, elasticity matters | Load is predictable, customization/control matters, or exit risk is high |
| Single node / distributed | The dataset and workload fit comfortably on one machine | Availability, geography, elasticity, or capacity require multiple nodes |
| System of record / derived store | Authoritative facts must be validated and retained | A representation exists to accelerate or specialize reads |

## Worked Example
For a social application, the operational database owns users, posts, and follow relationships. A warehouse receives a read-only history through ETL for revenue and engagement analysis; a lake may retain raw events, images, or feature data for data science. A home timeline is a derived materialized view: it can be regenerated from posts and follows, while the post and follow records remain authoritative. A search index and recommendation model are also derived systems, each optimized for a different access pattern. This design accepts extra pipelines and eventual propagation in exchange for protecting OLTP latency and allowing each consumer to use a suitable representation.

## Key Takeaways
1. Name the workload and its nonfunctional requirements before selecting infrastructure.
2. Separate transactional and analytical concerns when their access patterns interfere.
3. Identify one system of record and make every derived copy rebuildable.
4. Use distribution and managed services deliberately; both trade control for capabilities.
5. Include privacy, deletion, residency, and retention in the architecture—not as afterthoughts.

## Connects To
- **Ch 2**: Turns workload goals into measurable performance, reliability, scalability, and maintainability requirements.
- **Ch 3**: Chooses data models according to relationships and query shapes.
- **Ch 4**: Explains the storage engines and indexes behind OLTP and OLAP trade-offs.
- **Ch 5**: Makes data movement and independent system evolution safe through compatible encodings.
