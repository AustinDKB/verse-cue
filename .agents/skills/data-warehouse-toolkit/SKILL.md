---
name: data-warehouse-toolkit
description: "Knowledge base from \"The Data Warehouse Toolkit\" by Ralph Kimball and Margy Ross. Use when applying dimensional modeling, DW/BI architecture, fact and dimension design, ETL, lifecycle planning, or big-data practices."
---
argument-hint: [topic, framework name, or chapter number]

# The Data Warehouse Toolkit
**Authors**: Ralph Kimball and Margy Ross | **Pages**: ~601 | **Chapters**: 21 | **Generated**: 2026-08-13

The book uses business case studies to show dimensional modeling techniques. Chapter 2 acts as a technique checklist for the rest of the book.

## How to Use This Skill

- Without a topic, load the core frameworks below.
- With a topic, find it in the Topic Index and read the linked chapter.
- With a framework name, read the matching section in `patterns.md` and the source chapter.
- With a chapter number, read its exact file in `chapters/`.
- For terms, use `glossary.md`. For decisions, use `cheatsheet.md`.

## Core Frameworks & Mental Models

### Design from business process and grain

- Use the **Four-Step Dimensional Design Process** for every model: select the business process, declare the grain, identify dimensions, then identify facts.
- Declare grain as the exact meaning of one fact row. Treat grain as a contract. Reject every dimension or fact that cannot describe that row.
- Prefer atomic data over premature summaries because atomic rows preserve dimensions and support questions that designers cannot predict.
- Use a **Transaction Fact Table** for point events, a **Periodic Snapshot Fact Table** for regular states, and an **Accumulating Snapshot Fact Table** for finite workflows with known milestones. Keep different grains in separate tables.
- Use **Factless Fact Tables** for events or relationships without measures. Use **Coverage Factless Fact Tables** when non-use must compare with every possible combination.
- Use **Semi-additive Facts** with special time rules. Never sum balances across dates. Calculate ratios from additive components, such as total dollars divided by total quantity.

### Integrate with conformed dimensions

- Use the **Enterprise Data Warehouse Bus Architecture** and **Enterprise Data Warehouse Bus Matrix** as the enterprise plan. Put processes in rows and reusable dimensions in columns.
- Prefer **Conformed Dimensions** and **Conformed Facts** over independent data marts because shared meaning enables **Drill Across** and prevents conflicting results.
- Use role-playing views when one dimension has several meanings, such as order date, ship date, and arrival date.
- Use surrogate keys for dimension rows. Use a **Durable Supernatural Key** when one business entity spans source-key changes or Type 2 profile rows.
- Use bridges for open-ended many-to-many relationships. Add weights only when allocated totals have a valid business rule.

### Manage history and complex dimensions

- Choose SCD treatment per attribute. Use **Type 0: Retain Original** for immutable history, **Type 1: Overwrite** for correction or current-only views, **Type 2: Add New Row** for point-in-time history, and **Type 3: Add New Attribute** for one prior value.
- Prefer **Type 4: Add Mini-Dimension** for large, volatile attribute groups. Use Types 5, 6, and 7 only when users need combined current and historical paths and governance accepts the complexity.
- Prefer flattened dimensions for fixed-depth hierarchies. Use a hierarchy bridge for ragged or variable-depth structures. Use an outrigger only for a justified low-cardinality cluster.
- Use **Junk Dimensions** for low-cardinality flags. Use **Degenerate Dimensions** for transaction identifiers without descriptive attributes.
- Use **Step Dimensions** for sequence analysis and **Timespan Fact Tables** for arbitrary historical status.
- Use **Supertype and Subtype Schemas** when shared measures coexist with line-of-business detail.

### Deliver through the Kimball Lifecycle and ETL

- Use the **Kimball Lifecycle** as an iterative roadmap: readiness, scope, requirements, architecture, modeling, ETL, BI applications, deployment, maintenance, and growth.
- Prefer high-impact, feasible processes in the **Prioritization Grid**. Protect the first iteration from the **Law of Too**.
- Use interviews plus facilitated sessions for requirements. Use the bus matrix, bubble chart, design worksheets, data profiling, and an issues tracking log in collaborative workshops.
- Use the 34 ETL subsystems as a checklist. Profile sources early, capture changes, screen quality, archive stages, preserve lineage, and load dimensions before facts.
- Use the **Surrogate Key Pipeline** to resolve every fact foreign key to the correct current or historical dimension row. Use a keyed dummy row for an accepted late-arriving dimension.
- Apply **Real-Time Triage** before promising latency. Choose instantaneous, intra-day, or daily delivery, then accept the related data-quality and administration trade-offs.

### Govern big data

- Prefer **Extended RDBMS Architecture** for relational semantics and indexed lookups. Prefer **MapReduce/Hadoop Architecture** for flexible structures, massive scans, and complex branching.
- Use the **Data Highway** to separate Raw Source, Real Time, Business Activity, Top Line, and DW and Long Time Series quality and latency levels.
- Use a **Fact Extractor from Big Data** to turn raw observations into trendable facts. Build from sandbox results, then reimplement and rehost proven logic in supported platforms.
- Dimensionalize early. Replace source natural keys with durable surrogate keys across caches. Apply privacy, security, compliance, metadata, master-data, and resource governance during exploration.

## Chapter Index

| # | Title | Key frameworks |
|---|---|---|
| [ch01](chapters/ch01-dw-bi-dimensional-modeling-primer.md) | Data Warehousing, Business Intelligence, and Dimensional Modeling Primer | Kimball DW/BI Architecture, Bus Architecture |
| [ch02](chapters/ch02-kimball-dimensional-modeling-techniques.md) | Kimball Dimensional Modeling Techniques Overview | Four-Step Process, SCD Types 0–7 |
| [ch03](chapters/ch03-retail-sales.md) | Retail Sales | Atomic Grain, Factless Fact Table |
| [ch04](chapters/ch04-inventory.md) | Inventory | Three Fact Table Types, Bus Matrix |
| [ch05](chapters/ch05-procurement.md) | Procurement | Procurement Pipeline, SCD Techniques |
| [ch06](chapters/ch06-order-management.md) | Order Management | Role Playing, Junk Dimensions |
| [ch07](chapters/ch07-accounting.md) | Accounting | GL Periodic Snapshot, Organization Map Bridge |
| [ch08](chapters/ch08-customer-relationship-management.md) | Customer Relationship Management | Closed Loop Analytic CRM, Behavior Study Groups |
| [ch09](chapters/ch09-human-resources-management.md) | Human Resources Management | Employee Type 2, HR Bus Matrix |
| [ch10](chapters/ch10-financial-services.md) | Financial Services | Bridge Weighting, Supertype and Subtype |
| [ch11](chapters/ch11-telecommunications.md) | Telecommunications | Design Review, Process-Centric Modeling |
| [ch12](chapters/ch12-transportation.md) | Transportation | Multiple Granularities, Local and Equivalized Time |
| [ch13](chapters/ch13-education.md) | Education | Accumulating Snapshot, Coverage Factless Fact |
| [ch14](chapters/ch14-healthcare.md) | Healthcare | Measurement Type Dimension, Diagnosis Group Bridge |
| [ch15](chapters/ch15-electronic-commerce.md) | Electronic Commerce | Clickstream Facts, Step Dimension |
| [ch16](chapters/ch16-insurance.md) | Insurance | Insurance Bus Matrix, Timespan Snapshot |
| [ch17](chapters/ch17-kimball-lifecycle-overview.md) | Kimball DW/BI Lifecycle Overview | Lifecycle, Product Evaluation Matrix |
| [ch18](chapters/ch18-dimensional-modeling-process-and-tasks.md) | Dimensional Modeling Process and Tasks | Bubble Chart, Design Worksheets |
| [ch19](chapters/ch19-etl-subsystems-and-techniques.md) | ETL Subsystems and Techniques | 34 Subsystems, Quality Screens |
| [ch20](chapters/ch20-etl-system-design-and-development-process-and-tasks.md) | ETL System Design and Development Process and Tasks | 10-Step ETL Plan, Real-Time Triage |
| [ch21](chapters/ch21-big-data-analytics.md) | Big Data Analytics | Data Highway, MapReduce/Hadoop |

## Topic Index

- **Accumulating Snapshot Fact Table** → ch02, ch04, ch06, ch13, ch14, ch16
- **Aggregate Navigation** → ch02, ch15
- **Big Data** → ch21
- **Bus Architecture and Bus Matrix** → ch01, ch02, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch14, ch15, ch16, ch17, ch18
- **Conformed Dimensions and Facts** → ch01, ch02, ch04, ch05, ch07, ch08, ch17, ch18, ch19, ch21
- **Data Highway** → ch21
- **Data Profiling** → ch18, ch19, ch20
- **Degenerate Dimensions** → ch02, ch03, ch06, ch11, ch12, ch15, ch16
- **Dimensional Modeling** → ch01, ch02, ch03, ch11, ch17, ch18
- **Factless Fact Tables** → ch02, ch03, ch06, ch07, ch09, ch13, ch16
- **Fact Table Grain** → ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch10, ch11, ch12, ch14, ch16, ch18, ch20
- **Kimball Lifecycle** → ch01, ch17, ch18
- **MapReduce/Hadoop Architecture** → ch21
- **Mini-Dimensions** → ch05, ch08, ch10, ch12, ch15, ch16
- **Periodic Snapshot Fact Tables** → ch02, ch04, ch07, ch09, ch10, ch16
- **Quality Screens and Error Event Schema** → ch19, ch20
- **Role-Playing Dimensions** → ch03, ch06, ch12, ch14, ch15, ch16
- **Slowly Changing Dimensions** → ch02, ch05, ch09, ch10, ch16, ch19, ch20, ch21
- **Step Dimensions** → ch08, ch15
- **Surrogate and Durable Keys** → ch01, ch02, ch03, ch05, ch08, ch09, ch11, ch19, ch20, ch21
- **Supertype and Subtype Schemas** → ch10, ch14, ch16
- **Timespan Fact Tables** → ch08, ch14, ch16
- **Transaction Fact Tables** → ch02, ch03, ch04, ch07, ch16

## Supporting Files

- [glossary.md](glossary.md) — significant terms in alphabetical order.
- [patterns.md](patterns.md) — dimensional modeling, ETL, lifecycle, and big-data techniques.
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, trade-offs, and fast smells.

## Scope & Limits

This skill covers frameworks and techniques from the generated chapter files for *The Data Warehouse Toolkit*. It does not replace source-system profiling, business governance, security review, or platform-specific documentation. Apply the patterns with current project constraints and validate all business definitions before implementation.
