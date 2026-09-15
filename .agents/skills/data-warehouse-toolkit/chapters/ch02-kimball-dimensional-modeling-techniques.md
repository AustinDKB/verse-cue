# Chapter 2: Kimball Dimensional Modeling Techniques Overview

## Core Idea
Dimensional modeling starts with a business process and its measurement events, then declares grain, dimensions, and facts in that order. The design stays useful when it uses atomic data, reusable conformed dimensions, and structures that match business questions without being shaped by individual reports.

## Frameworks Introduced
- **Four-Step Dimensional Design Process**: Use for every dimensional design. Select the business process, declare the grain, identify the dimensions, and identify the facts. Then document names, domains, and business rules with business data governance representatives.
- **Collaborative Dimensional Modeling Workshops**: Use when requirements and data realities must become one design. Bring business subject matter experts, source-system experts, data modelers, and data governance representatives together. Let the model unfold through interactive sessions rather than designing it in isolation.
- **Enterprise Data Warehouse Bus Architecture** and **Enterprise Data Warehouse Bus Matrix**: Use to build an enterprise DW/BI system incrementally. Put business processes in matrix rows and dimensions in columns. Use shaded cells to show associations, test dimension definitions, identify conformance opportunities, and prioritize one process row at a time.
- **Integration via Conformed Dimensions**: Use when separate business processes must appear together in one analysis. Define shared dimensions with identical column names and domain contents, reuse them across fact tables, and align separate results with **Drilling Across**.
- **Three Basic Fact Table Grains**: Use a **Transaction Fact Table** for events at a point in space and time, a **Periodic Snapshot Fact Table** for a standard period, and an **Accumulating Snapshot Fact Table** for predictable process milestones. Keep each grain in a separate physical table.
- **Slowly Changing Dimension (SCD) Techniques, Types 0–7**: Use the type that matches the required history. Type 0 retains the original, type 1 overwrites, type 2 adds a row, type 3 adds an attribute, type 4 adds a mini-dimension, type 5 adds a mini-dimension and type 1 outrigger, type 6 adds type 1 attributes to a type 2 dimension, and type 7 provides dual type 1 and type 2 dimensions.
- **Hierarchy Techniques**: Use fixed depth positional attributes for stable named levels. Use force-fit positional attributes for slightly ragged hierarchies. Use a hierarchy bridge table or a pathstring attribute for ragged or variable-depth hierarchies, based on the needed flexibility.

## Key Concepts
- **Grain**: The exact meaning of one fact table row. It is a binding contract that every dimension and fact must obey.
- **Business Process**: An operational activity that generates or captures performance metrics and corresponds to a row in the enterprise data warehouse bus matrix.
- **Dimension**: A descriptive context that supplies who, what, where, when, why, and how for a process event.
- **Fact**: A measurement from a business process event, usually numeric, that remains consistent with the declared grain.
- **Fact Table**: A table of measurement-event rows, dimension foreign keys, and optional degenerate dimensions or timestamps.
- **Conformed Dimension**: A dimension reused across processes with matching attribute names and domain contents, enabling consistent drill-across analysis.
- **Surrogate Key**: An anonymous integer key controlled by the DW/BI system, rather than by an operational natural key.
- **Durable Supernatural Key**: A persistent key for one business entity that does not change when source-system natural keys change.
- **Aggregate Navigation**: Open BI-layer selection of aggregate fact tables so they accelerate queries like database indexes without changing results.
- **Factless Fact Table**: A fact table that records dimensional entities coming together without a numeric measurement, and can support coverage-versus-activity analysis.

## Mental Models
- Use **grain as a contract**: reject every candidate dimension or fact that cannot describe one row at that exact level.
- Think of atomic fact tables as the durable foundation and aggregates as performance structures. Atomic data supports unpredictable queries, while aggregates anticipate common query levels.
- Use the bus matrix as both a design test and a delivery plan. Scan rows for process fit, columns for conformance, and implement manageable process rows.
- Treat dimensions as the user experience. Invest in descriptive, governed attributes because filters, groups, and report labels come from them.

## Anti-patterns
- **Mixed grains in one fact table**: Different grains make facts and dimensions ambiguous, producing unreliable analysis. Create separate physical tables.
- **Fact-to-fact table joins across foreign keys**: Relational cardinality cannot control the result. Use separate queries and **Drilling Across** with common conformed row headers.
- **Snowflaked dimensions**: Normalized hierarchies make navigation harder and can reduce query performance. Prefer a denormalized flattened dimension for fixed-depth hierarchies.
- **Centipede fact tables**: Many hierarchically related foreign keys or separate low-cardinality dimensions create needless complexity. Collapse fixed-depth hierarchies and consider a junk dimension.
- **Abstract generic dimensions**: Combining unrelated locations, people, or products enlarges tables and harms query legibility and performance. Keep distinct dimension types with clear attributes.
- **Stored year-to-date facts**: YTD requests expand into varied fiscal-period requirements. Calculate these metrics in BI applications or an OLAP cube.
- **Uncontrolled natural keys as dimension primary keys**: Source changes and multiple source systems make them unsafe. Use dimension surrogate keys, with a special meaningful key allowed for the calendar date dimension.

## Worked Example
For a retail sales process, declare the grain as one row per product line in one sales transaction. Attach the date, product, store, and other dimensions that describe that line, and place quantity sold and extended price in the fact table. These facts measure the transaction event, while a store manager salary does not match the grain and stays out. If the invoice has no remaining descriptive content at line grain, retain its invoice number as a **Degenerate Dimension** in the fact table. This atomic transaction design supports slicing by any attached dimension. If later reporting needs daily rollups, create an aggregate fact table with shrunken conformed dimensions instead of changing the atomic table.

## Key Takeaways
- Select the business process before designing tables.
- Declare atomic grain before selecting dimensions or facts.
- Keep each fact table at one grain and tie every fact to a physical measurement event.
- Build wide, descriptive dimensions with controlled surrogate keys and explicit unknown values.
- Reuse conformed dimensions across processes and use drill-across instead of fact-to-fact joins.
- Choose SCD treatment per attribute, not necessarily per dimension.
- Add aggregates for performance, but keep atomic facts available to the BI layer.

## Connects To
- **Chapter 1, DW/BI and Dimensional Modeling Primer**: Defines the dimensional foundations used here.
- **Chapter 3, Retail Sales**: Applies the techniques to the retail sales case study.
- **Chapter 4, Inventory**: Extends conformed dimensions, bus architecture, and periodic snapshots.
- **Chapter 18, Dimensional Modeling Process and Tasks**: Expands the design process and workshop work.
- **Chapter 19, ETL Subsystems and Techniques**: Describes surrogate keys, SCD processing, aggregates, and late-arriving data.
