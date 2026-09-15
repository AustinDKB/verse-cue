# Chapter 20: ETL System Design and Development Process and Tasks

## Core Idea

ETL development exposes the hidden complexity of a data warehouse. Source-system limits, data quality, historical reconstruction, key assignment, job dependencies, recovery, and load performance determine more effort than the target tables alone suggest. Kimball presents a 10-step plan that separates one-time historic loads from ongoing incremental loads. Begin only after the dimensional model, high-level architecture plan, and source-to-target mappings exist. Create a technology-independent plan, choose an ETL tool before detailed design, document decisions, stage and archive data, and automate predictable errors. Treat real-time delivery as a business trade-off between latency, data quality, and administration, not as a single technical feature.

## Frameworks Introduced

- **10-step ETL system design and development plan:** Use when building a warehouse ETL system from an initial design through operation. Draw the high-level plan, choose an ETL tool, develop default strategies, drill down by target table, develop the ETL specification document, develop a sandbox source system, perform the one-time historic load, develop incremental ETL processing, load aggregate tables and OLAP, and automate operation.
- **High-level plan schematic:** Use at project start to show sources, targets, major transformations, unresolved issues, and processing burdens. Maintain a simple communication version and a detailed internal version, then update and release the schematic as design knowledge changes.
- **ETL specification document:** Use before implementation to combine source-to-target mappings, data profiling, physical design decisions, historic and incremental strategies, dependencies, preconditions, cleanup, and implementation difficulty. Describe each target table in enough detail to guide development and future maintenance.
- **Surrogate key pipeline:** Use as the final fact transformation to exchange source natural keys for dimension surrogate keys and resolve referential integrity errors. Process all dimension tables, including type 2 changes, before the fact rows enter this pipeline.
- **Real-Time Triage:** Use when business users request “real-time” delivery. Classify the need as **instantaneous**, **intra-day**, or **daily**, then select EII, micro-batch ETL, or conventional batch ETL according to the required latency and accepted data quality.
- **Real-time partition:** Use to extend a static historical warehouse to the current time. Keep the hot partition aligned with the static fact table’s grain, load it continuously, and merge or reconcile it with the static table during regular processing.

## Key Concepts

- **Default strategies:** Reusable decisions for extraction, archiving, data quality policing, dimension changes, availability, auditing, and staging. Apply them broadly, then modify them for individual tables when needed.
- **Data staging:** Writing extracted or transformed data to disk for later ETL steps, recovery, auditability, and archiving. Archive extracted and staged data for at least one month.
- **Historic load:** A one-time process that reconstructs past dimension and fact data. It can pause for manual investigation and can tolerate a load that takes several days.
- **Incremental load:** A fully automated process that identifies new, changed, and deleted source rows, then applies established transformations to the changed set.
- **Type 1 dimension change:** An attribute update that overwrites existing values, usually across all existing rows for that entity.
- **Type 2 dimension change:** An attribute update that closes the current dimension row and inserts a new row with a new surrogate key, effective dates, and current-row status.
- **Audit statistics:** Counts, sums, and other quality measures that tie source reports to extracted data and warehouse load results. Explain differences when exact tie-back cannot occur.
- **Grain alignment:** The rule that every fact in a fact table row must represent the same grain. Remove totals at another grain or move them to the correct aggregate table.
- **Late arriving fact:** A fact received after its event date. With type 2 dimensions, find the dimension row effective when the fact occurred by using row begin and end dates.

## Mental Models

- **Design dependencies before speed:** Load dimensions before fact-table surrogate key lookups because available keys and type 2 versions define valid fact references.
- **Separate correctness checkpoints from transformation:** Archive raw extracts and calculate quality measures before transformation so recovery and diagnosis start from known data.
- **Latency spends a quality budget:** As delivery moves from daily to intra-day to instantaneous, remove staging and structure or business-rule screens only with explicit acceptance of provisional data.

## Anti-patterns

- **Using a hand-coded script library as the default platform:** This hides process logic, metadata, version control, recovery, and performance behavior. Kimball recommends a commercial ETL tool despite its learning curve.
- **Trusting an informal hierarchy as clean:** A hierarchy from a desktop spreadsheet can violate many-to-one relationships. Pre-verify it or normalize it in staging before loading the dimension.
- **Loading facts before dimension processing finishes:** This creates missing surrogate keys or referential integrity violations. Complete dimension inserts and type 2 changes first.
- **Mapping every unknown natural key to one shared unknown member:** This loses the identity of each error and prevents later correction. Create a dummy dimension row for the specific unknown key when appropriate.
- **Parallelizing jobs without resource analysis:** Concurrent jobs can compete for network bandwidth, I/O, and memory, making processing slower than a sequential design.
- **Building aggregates without synchronization:** Type 1 dimension changes and current-period facts can make aggregates disagree with detail facts unless the ETL process backs out and rebuilds affected results.

## Worked Example

A utility warehouse receives a 2,000-field COBOL Detailed Master Record (DMR), one row per customer meter, with 13 monthly usage buckets. The design first extracts only the needed fields into `Fact_stage1`, while dimension processing creates customer, geography, meter, and date surrogate keys. The ETL unbucketizes the monthly columns into as many as 13 rows per source row and stops before the customer’s subscription date. It then performs customer-key lookup on the customer-sorted stream, sorts by geography for the geography-key lookup, sorts by meter type for the meter-key lookup, and looks up the read-date key. Only after these dependencies complete does it bulk-load `Electric_Usage_Fact`. The schematic also records estimated bills, missed meter reads, old meter types, and unresolved maintenance questions, so the team treats these as design and data-quality decisions rather than hidden defects.

## Key Takeaways

- Draw and maintain the high-level plan before detailed ETL design.
- Choose the ETL tool before detailed planning to reduce redesign and rework.
- Archive raw extracts and stage data before transformation and quality review.
- Profile each target table, validate hierarchies, and document dependencies and preconditions.
- Separate historic and incremental processes when their automation and volume needs differ.
- Preserve fact grain, enforce referential integrity, and complete the surrogate key pipeline before loading.
- Classify real-time needs with Real-Time Triage before selecting an architecture.

## Connects To

- **Chapter 19, ETL Subsystems and Techniques:** Supplies the 34 ETL subsystems for extraction, cleaning and conforming, presentation delivery, and environment management.
- **Chapter 5, Procurement:** Defines slowly changing dimension methods, including type 1, type 2, type 3, and hybrid techniques used during dimension processing.
- **Dimensional modeling:** Provides grain, fact table, dimension, conformed dimension, and surrogate key decisions that the ETL system must physically enforce.
- **Aggregate tables and OLAP:** Depend on synchronized fact loads and dimension history so precomputed results match detail data.
