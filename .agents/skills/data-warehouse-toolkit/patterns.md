# Patterns

## Four-Step Dimensional Design Process
**When to use**: Use for every dimensional model.
**How**: Select the business process. Declare one atomic grain. Identify dimensions. Identify facts. Document names, domains, and rules with business stewards.
**Trade-offs**: Grain-first work prevents rework, but workshops need business and source experts.

## Enterprise Data Warehouse Bus Architecture
**When to use**: Use for incremental enterprise delivery across business processes.
**How**: Put processes in bus-matrix rows and shared conformed dimensions in columns. Build one process row at a time and reuse dimensions.
**Trade-offs**: Conformance needs governance effort, but it prevents isolated data marts and conflicting measures.

## Transaction, Periodic Snapshot, and Accumulating Snapshot
**When to use**: Use a transaction fact for events, a periodic snapshot for regular state, and an accumulating snapshot for finite workflows with milestones.
**How**: Keep each grain in a separate physical table. Add role-playing dates and lag measures where needed.
**Trade-offs**: Complementary tables preserve multiple views, but increase ETL and storage work.

## Slowly Changing Dimension Techniques
**When to use**: Use an attribute-level technique when descriptive values change.
**How**: Use Type 0 for original-only, Type 1 for correction or current-only, Type 2 for history, Type 3 for current-plus-prior, Type 4 for volatile groups, and Types 5–7 for combined current and historical paths.
**Trade-offs**: Type 2 protects history but adds rows. Hybrid techniques add analytic choice but increase keys, joins, and user confusion.

## Role-Playing Dimensions
**When to use**: Use when one fact contains several dates, people, places, or other roles from one dimension.
**How**: Store separate foreign keys and expose clear logical views with unique role names.
**Trade-offs**: Roles improve meaning without duplicating storage, but require careful naming and ETL lookup.

## Factless and Coverage Fact Tables
**When to use**: Use event facts for relationships without measures. Use coverage facts when absence must compare with every possible combination.
**How**: Set the event or coverage grain, store dimension keys, and count rows. Add an artificial count of one when SQL or OLAP clarity needs it.
**Trade-offs**: Sparse event facts are efficient. Coverage facts can grow rapidly and need a justified bounded domain.

## Bridge Tables with Weighting
**When to use**: Use for open-ended many-to-many relationships, such as account holders or diagnoses.
**How**: Store a group key and bridge rows. Add weights that sum to 1.00 when allocated totals are valid. Use unweighted impact reports only with an overcount warning.
**Trade-offs**: Bridges preserve grain and flexibility, but complicate BI queries and can overcount without weights.

## Mini-Dimensions
**When to use**: Use for correlated attributes that change too quickly for a large Type 2 dimension.
**How**: Group attributes into clumps, assign a mini-dimension key, and place the key in the fact at load time.
**Trade-offs**: Mini-dimensions control row growth, but add fact keys and separate lookup paths.

## Step Dimension and Timespan Fact
**When to use**: Use Step Dimension for ordered sessions or workflows. Use Timespan Fact Tables for arbitrary point-in-time or interval status.
**How**: Prebuild step numbers and remaining-step values. For timespans, store begin and end timestamps, with the next interval beginning when the prior one ends.
**Trade-offs**: ETL work makes queries simple. Intervals and sequence roles need strict boundary rules.

## Supertype and Subtype Schemas
**When to use**: Use when products or charges share core measures but have line-specific facts.
**How**: Put common measures in the supertype. Put special facts and attributes in subtype schemas with shared surrogate keys and shrunken conformed dimensions.
**Trade-offs**: The design avoids a sparse Swiss-cheese table, but users need clear navigation across schemas.

## Kimball Lifecycle
**When to use**: Use for planning and governing an iterative DW/BI program.
**How**: Assess readiness, scope and justify, define requirements, design architecture, select products, model data, build ETL and BI applications, deploy, maintain, and grow.
**Trade-offs**: Iterative delivery provides value sooner, but each process needs business sponsorship, feasibility checks, and deployment support.

## ETL Quality and Surrogate-Key Pipeline
**When to use**: Use for every production load.
**How**: Profile sources. Capture changes. Apply column, structure, and business-rule quality screens. Record error events. Load dimensions first, resolve historical keys, then load facts. Archive stages and lineage.
**Trade-offs**: Screens and archives consume time and storage, but they support recovery, diagnosis, and referential integrity.

## Real-Time Triage and Data Highway
**When to use**: Use when users request real-time or mixed-latency data.
**How**: Classify the need as instantaneous, intra-day, or daily. Select EII, micro-batch, or batch. Route data through Raw Source, Real Time, Business Activity, Top Line, and DW and Long Time Series caches as needed.
**Trade-offs**: Lower latency reduces time for cleansing and relationship checks. Slower paths improve quality and history.

## Extended RDBMS vs MapReduce/Hadoop
**When to use**: Use Extended RDBMS for relational semantics and indexed lookups. Use MapReduce/Hadoop for flexible structures, full scans, and complex branching.
**How**: Extract useful facts from raw data, dimensionalize early, replace natural keys with durable surrogate keys, and reimplement proven sandbox logic in supported platforms.
**Trade-offs**: RDBMS improves governed SQL access. Hadoop improves flexible distributed processing, but both need resource isolation, privacy controls, and governance.
