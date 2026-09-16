# Chapter 4: Inventory

## Core Idea

Model inventory as complementary views of a value-chain process, then integrate those models through the enterprise data warehouse bus architecture. Choose a fact table type from the business process: a periodic snapshot for recurring balances, a transaction fact table for individual inventory events, or an accumulating snapshot for a finite workflow with known milestones. Shared conformed dimensions and facts make separate process models usable as one DW/BI environment.

## Frameworks Introduced

- **Value chain dimensional modeling** — Use when an organization has a sequence of primary activities, such as purchase orders, warehouse receipts, warehouse inventory, store deliveries, store inventory, and retail sales. Model each process at its own natural grain and dimensionality, then integrate the process models through shared dimensions.
- **Three fact table types** — Use the transaction fact table for an instantaneous event, the periodic snapshot for recurring measurements at regular intervals, and the accumulating snapshot for a pipeline with a definite beginning, definite end, and standard intermediate milestones. Select one or more complementary types when one view cannot answer all business questions.
- **Enterprise data warehouse bus architecture** — Use when the enterprise needs incremental construction without isolated data marts. Define a standard interface of conformed dimensions and facts, and let independent process-centric dimensional models connect to that interface.
- **Enterprise data warehouse bus matrix** — Use for architecture planning, database design, data governance coordination, project estimating, and communication. Put business processes in rows, common dimensions in columns, and mark each process-dimension relationship. Start implementation with one process row to limit ETL risk.
- **Opportunity/stakeholder matrix** — Use the same business-process rows with business functions in place of dimension columns. Mark each group interested in each process so the project team can invite the correct participants for requirements, dimensional modeling, and BI specifications.
- **Drill across** — Use when a report must combine measures from separate fact tables. Query each dimensional model separately, then join results through identical conformed dimension attributes.

## Key Concepts

- **Grain** is the declared level of detail for a fact table. A store inventory periodic snapshot has one row per product, store, and day.
- **Periodic snapshot** stores a row for each product and location at each regular measurement period. Its rows form a time series and are often predictably dense.
- **Inventory transaction fact** stores one row per inventory transaction. Its facts record the quantity impact and often a dollar amount, with date, product, warehouse, vendor, and transaction type dimensions.
- **Accumulating snapshot** stores one row per pipeline occurrence and updates that row as the occurrence reaches milestones. Multiple date foreign keys represent events such as receipt, inspection, bin placement, and shipment.
- **Semi-additive fact** can be added across some dimensions but not across dates. Quantity on hand can aggregate across products or stores, but time aggregation needs an average or another valid balance rule.
- **Conformed dimension** means that a dimension has consistent keys, names, definitions, and values across the fact tables that use it. It can be identical, a shrunken rollup with an attribute subset, or a row subset at the same granularity.
- **Conformed fact** uses the same definition, dimensional context, and unit of measure wherever the fact name appears. If definitions differ, use unique names.
- **Surrogate date key** represents an undefined milestone date in a new accumulating snapshot row until the event occurs. A role-playing date dimension handles each milestone date.
- **Bus matrix** exposes common dimensions and business-process relationships. Its rows represent processes, not departments or reports, and its columns represent dimensions at their most granular common level.

## Mental Models

- A transaction fact tells what happened at an event. A periodic snapshot tells the state at regular times. An accumulating snapshot tells how a workflow progresses.
- Use a snapshot to answer broad balance questions. Do not reconstruct every historical position by rolling transactions forward unless the question needs transaction detail.
- Treat conformed dimensions as integration glue. Treat conformed facts as shared measurement contracts.
- Build process rows as independent pieces, but design them against one bus so independent delivery does not create independent definitions.

## Anti-patterns

- **Transaction-only inventory analysis:** Rolling every inventory transaction forward to reconstruct positions is cumbersome and impractical for broad analysis. Add a snapshot view when cumulative performance matters.
- **One fact table for different grains or dimensionality:** Combining events with different natural detail or dimensions obscures meaning. Model separate processes as separate fact tables.
- **Summing balances across dates:** Inventory levels and account balances are not additive over time. Use the correct time aggregation, such as averaging by the number of periods, rather than a row-weighted `AVG`.
- **Departmental, report-centric, or overly broad matrix rows:** Departments and requested reports do not define business processes. Use primary activities and events as rows.
- **Generic or hierarchy-level matrix columns:** A generic “person” dimension can combine unrelated populations, while separate columns for every hierarchy level make the matrix unruly. Use granular common dimensions and document rollup grain in the cell.
- **Isolated stovepipe models:** Models without conformed dimensions produce irreconcilable views and can block enterprise integration. Map and reprocess sound models, or rebuild models whose grain and dimensionality cannot support the bus.
- **IT-only data governance:** IT can facilitate conformance but seldom has enough authority to drive enterprise agreement alone. Business subject matter experts must lead governance and enforce common definitions.
- **Unmarked incompatible facts:** Identical labels with different definitions or units invite invalid calculations. Rename incompatible facts or carry measures in both required units.

## Worked Example

A grocery retailer needs daily quantity-on-hand analysis by product and store. Declare the grain as one row per product, store, and day, then use date, product, and store dimensions. Store quantity on hand as a semi-additive fact, and add quantity sold plus inventory dollar value at cost and latest selling price for movement and valuation measures. The snapshot is dense: 60,000 products across 100 stores create about 6 million rows per nightly load. If three years of daily history creates too much volume, retain 60 daily days and store older history as weekly snapshots in a separate fact table because the periodicity differs. Do not sum quantity on hand across dates. For a yearly turns calculation, divide total quantity sold by the daily average quantity on hand.

## Key Takeaways

- Declare grain before choosing dimensions or facts.
- Use periodic, transaction, and accumulating snapshots as complementary views, not competing universal answers.
- Document the enterprise data warehouse bus matrix before scaling process delivery.
- Build conformed dimensions once and reuse them across process models.
- Govern names, definitions, values, quality, security, and access through business-led stewardship.
- Carry comparable conformed facts in compatible units, and rename facts that cannot conform.

## Connects To

- **Chapter 3: Retail Sales** supplies the shared date, product, and store dimensional context used by inventory models.
- **Chapter 5: Procurement** continues the discussion of handling content changes in dimensions.
- **Chapter 6: Order Management** develops role-playing date dimensions and multiple units of measure further.
- **Chapter 10: Financial Services** extends the discussion of dimension subsets and supertype/subtype dimensions.
- **Enterprise data warehouse concepts** connect value-chain process models, conformed dimensions, conformed facts, data governance, and agile development.
