# Glossary

**Accumulating Snapshot Fact Table** — One row follows a finite process through known milestones and updates as events occur (Ch 2, 4, 6, 13, 14, 16).
**Additive Fact** — A measure that can sum across every dimension at its grain (Ch 3).
**Aggregate Navigation** — BI-layer selection of aggregate facts to improve query speed without changing results (Ch 2).
**Atomic Data** — The most detailed, unaggregated measurement-event data (Ch 1, 2).
**Audit Dimension** — ETL metadata about runtime, quality, allocation, currency, or version context (Ch 6, 19).
**Behavior Study Group** — A stored cohort of durable entity keys for repeated analysis (Ch 8).
**Bus Matrix** — A matrix of business processes and shared dimensions that guides integration and delivery (Ch 1, 2, 4, 17, 18).
**Change Data Capture** — Isolation of source inserts, edits, and deletes since the prior load (Ch 19).
**Conformed Dimension** — A shared dimension with consistent names, definitions, keys, and values across processes (Ch 1, 2, 4).
**Conformed Fact** — A repeated measure with the same definition, unit, and dimensional context (Ch 4, 16).
**Consolidated Fact Table** — A combined fact table at a common grain and dimensionality for repeated comparisons (Ch 7, 16).
**Coverage Factless Fact Table** — Rows for every possible facility, time, and state combination, including non-use (Ch 13).
**Data Highway** — Physical caches arranged by latency and quality, from Raw Source to DW and Long Time Series (Ch 21).
**Data Profiling** — Query-based examination of source content, structure, relationships, and derivations (Ch 18, 19, 20).
**Data Virtualization** — A logical structure over physical data that defers computation to query time (Ch 21).
**Degenerate Dimension** — A transaction identifier kept in a fact table without a related dimension (Ch 2, 3, 6).
**Dimension** — Descriptive context used to filter, group, and label measurements (Ch 1, 2).
**Dimension Role Playing** — Separate logical views of one physical dimension used for different business roles (Ch 2, 3, 6, 12).
**Durable Supernatural Key** — A stable identifier for one business entity across changing source natural keys and Type 2 rows (Ch 2, 5, 8, 21).
**Fact Extractor from Big Data** — Processing that converts raw or unstructured observations into trendable facts (Ch 21).
**Fact Table** — Rows of measurement events, dimension keys, and optional degenerate dimensions at one grain (Ch 1, 2).
**Factless Fact Table** — A fact table that records events or relationships without variable numeric measures (Ch 2, 3, 13).
**Four-Step Dimensional Design Process** — Select business process, declare grain, identify dimensions, then identify facts (Ch 2, 3, 18).
**Grain** — The exact business meaning of one fact-table row (Ch 1, 2, 18).
**Junk Dimension** — A dimension that groups low-cardinality flags and indicators (Ch 6, 16).
**Kimball Lifecycle** — An iterative roadmap from readiness and requirements through architecture, delivery, maintenance, and growth (Ch 17).
**MapReduce/Hadoop Architecture** — Distributed processing for flexible structures, full scans, and complex branching (Ch 21).
**Measurement Type Dimension** — A dimension that gives sparse generic measurements their meaning, unit, and additivity rules (Ch 6, 14).
**Mini-Dimension** — A smaller dimension for volatile or frequently analyzed attribute groups (Ch 5, 8, 10, 12).
**Non-additive Fact** — A measure that cannot sum across one or more dimensions, such as unit price (Ch 3).
**Periodic Snapshot Fact Table** — A regular measurement of status or balance at a declared period grain (Ch 2, 4, 7, 9, 10).
**Real-Time Triage** — Classification of instantaneous, intra-day, or daily needs before selecting a delivery method (Ch 20).
**Role-Playing Dimension** — One physical dimension presented through several labeled roles (Ch 6, 12, 14, 16).
**Semi-additive Fact** — A measure that sums across some dimensions but needs special handling across time (Ch 4, 7, 9).
**Slowly Changing Dimension** — A dimension whose attribute changes follow an explicit history technique (Ch 2, 5, 19, 20).
**Star Schema** — A fact table joined to surrounding dimension tables (Ch 1).
**Step Dimension** — A dimension with sequence position and remaining-step attributes for ordered behavior (Ch 8, 15).
**Surrogate Key** — A warehouse-assigned dimension key separate from an operational identifier (Ch 1, 2, 19).
**Supertype and Subtype Schema** — Common facts in a supertype with line-of-business facts in subtype schemas (Ch 10, 14, 16).
**Timespan Fact Table** — Rows with effective and expiration times that describe a state interval (Ch 8, 14, 16).
**Transaction Fact Table** — Atomic event rows recorded at a point in space and time (Ch 2, 4, 7, 16).
**Type 0: Retain Original** — Keep the first attribute value and ignore later changes (Ch 5, 19).
**Type 1: Overwrite** — Replace an attribute value when history has no business value or the value needs correction (Ch 5, 19).
**Type 2: Add New Row** — Add a surrogate-keyed row with effective dates to preserve history (Ch 5, 19, 20).
**Type 3: Add New Attribute** — Store current and prior values in separate attributes (Ch 5, 19).
**Type 4: Add Mini-Dimension** — Move volatile attribute groups into a separate dimension (Ch 5, 19).
**Type 5: Mini-Dimension and Type 1 Outrigger** — Combine a mini-dimension with a current Type 1 reference (Ch 2, 5).
**Type 6: Add Type 1 Attributes to Type 2 Dimension** — Preserve Type 2 rows while overwriting current-value attributes across them (Ch 2, 5).
**Type 7: Dual Type 1 and Type 2 Dimensions** — Provide both current and historical access paths (Ch 2, 13).
