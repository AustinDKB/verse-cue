# Chapter 19: ETL Subsystems and Techniques

## Core Idea

A dimensional data warehouse needs a structured ETL architecture, not an improvised collection of tables, scripts, triggers, alerts, and schedules. Kimball identifies 34 subsystems grouped into extracting, cleaning and conforming, delivering, and managing. Design starts with requirements and constraints, then selects the needed techniques for reliable, available, and manageable data delivery.

## Frameworks Introduced

- **Requirements roundup**: Use before ETL design and development, when business, source, compliance, and operating constraints remain unclear. List business needs, compliance, data quality, security, data integration, data latency, archiving and lineage, BI delivery interfaces, available skills, and legacy licenses. Record KPIs, drill targets, source and transformation custody, retention, exposed fact and dimension tables, skills, and mandated licenses.
- **The 34 Subsystems of ETL**: Use as an architecture checklist for a dimensional warehouse back room. Group the subsystems into extracting, cleaning and conforming, delivering, and managing. Select the techniques that fit the requirements, but do not omit a needed capability because the initial load appears simple.
- **Quality screens**: Use as diagnostic filters in data-flow pipelines. Apply column screens to one-column null, range, or format tests. Apply structure screens to relationships across columns or tables. Apply business rule screens to complex, time-dependent, or aggregate-threshold tests. Record each failure in the error event schema, then halt, suspend, or tag the data according to severity.
- **Slowly changing dimension (SCD) techniques**: Use when a dimension attribute changes. Choose type 1 overwrite when history has no business value or data needs correction. Choose type 2 add new row when history must remain accurate. Choose type 3 add new attribute when users need old and new values. Use type 4 add mini-dimension for rapidly changing attribute groups, and types 5, 6, and 7 when current and historical perspectives need combined structures.
- **Surrogate key pipeline**: Use before fact loading to replace operational natural keys with dimension surrogate keys. Update dimensions first, resolve each lookup to the correct historical or current key, route failures to the responsible process, and load only rows with referential integrity or an approved default.

## Key Concepts

- **Data profiling**: Technical analysis of data content, consistency, and structure for early source suitability decisions and later cleansing specifications.
- **Change data capture (CDC)**: Isolation of source deletions, edits, and insertions since the last load, with reason codes and compliance metadata when needed.
- **Conformed dimension**: A dimension whose shared attributes have the same names and contents across business processes, enabling drill-across queries.
- **Survivorship**: Combination of matched records into one conformed row by applying business rules that select the best source value for each column.
- **Error event schema**: Centralized dimensional schema with one error event fact row for each quality-screen error and a lower-grain error event detail fact for affected fields.
- **Audit dimension**: ETL-created dimension that attaches runtime metadata, quality ratings, flags, and version numbers to fact rows.
- **Transaction grain**: Measurement event at a particular instant, such as an invoice line item.
- **Periodic snapshot grain**: Repeating measurement for a defined period, such as a monthly account balance.
- **Accumulating snapshot grain**: Evolving status of a finite process with a defined beginning and end, such as order processing.
- **Fact table surrogate key**: Sequential integer key that supports restart, rollback, row identification, insert-plus-delete updates, and parent-child designs.

## Mental Models

- Use the **bus matrix** to prioritize conformed dimensions. Start with an executive-backed business process and one shared attribute, then expand attributes and participating processes incrementally.
- Treat every staged dataset as archived unless the team consciously decides that recovery will never be needed. Preserve metadata that records origins and processing steps.
- Prefer tagging a quality failure and passing the row onward when business risk permits. Halting or suspending data creates manual work, missing rows, and uncertain database integrity.
- Keep relational dimensional schemas as the foundation for OLAP cubes. Complete referential integrity, hierarchy enforcement, and conventional ETL before cube loading.

## Anti-patterns

- **“It depends” without structure**: This permits an unplanned ETL spaghetti-mess. Use the 34-subsystem checklist and document the constraints that drive each decision.
- **Timed extracts based only on dates**: Restarts create duplicate rows, and missed runs can lose data. Use a CDC strategy that handles restart and deletion behavior.
- **Late data profiling**: Dirty or incomplete source data can divert the project after major milestones. Profile candidate sources early and use results to set realistic expectations.
- **Technical fixes without process change**: Input constraints can force clerks to enter artificial values. Treat recurring quality defects as indications of broken business processes and improve the quality culture.
- **Uncontrolled type 1 updates**: Overwrites restate history and invalidate affected aggregates. Use type 1 only when history has no business value, and notify fact providers when aggregates need rebuilding.
- **Operational keys combined with timestamps**: Concatenated keys do not scale reliably. Generate independent surrogate keys for each dimension.
- **Suspense as the default error response**: Suspended records may never return, so reports remain incomplete. Tag minor errors whenever possible.

## Worked Example

A late customer dimension feed arrives after sales facts must become visible. Waiting would violate the latency requirement, but pointing facts to a generic default row would require destructive foreign-key repairs later. The ETL system creates a customer dimension row with a new surrogate key and dummy attributes, then loads the facts against that key. When complete customer data arrives, the dimension manager performs type 1 overwrites on the dummy row. The fact keys remain stable. If the late feed instead represents a type 2 historical change, the ETL system adds a new dimension row, resets effective dates, and revises affected subsequent fact keys to preserve the customer context at the activity date.

## Key Takeaways

- Round up requirements before selecting ETL tools, schedules, latency patterns, or cleansing depth.
- Profile every candidate source early, then use the findings to drive source repair and quality-screen design.
- Maintain CDC that captures inserts, edits, deletions, nonstandard changes, reason codes, and compliance metadata.
- Update dimensions before facts, and make every fact foreign key resolve to a valid surrogate key.
- Match the fact loader to transaction, periodic snapshot, or accumulating snapshot grain.
- Stage and archive data with lineage metadata, version the ETL context, and design restart points before production.

## Connects To

- **Chapter 3: Retail Sales**: surrogate keys and dimension-key design.
- **Chapter 4: Inventory**: conformed dimensions and conformed facts.
- **Chapter 5: Procurement**: slowly changing dimension techniques.
- **Chapter 6: Order Management**: audit dimensions.
- **Chapters 8 and 10**: multivalued dimensions, bridge tables, and financial-services dimensional structures.
- **Chapter 20: ETL System Design and Development Process and Tasks**: implementation processes, tasks, and latency-related data quality trade-offs.
