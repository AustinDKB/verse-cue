# Chapter 1: Data Warehousing, Business Intelligence, and Dimensional Modeling Primer

## Core Idea

A DW/BI system starts with business needs, not technology. It must publish information that business users understand, trust, access quickly, and use for decisions. The design moves from business requirements through logical and physical models, then to technology and tools. The system succeeds only when the business community accepts and uses it.

Dimensional modeling addresses two linked needs: business understandability and fast query performance. It packages the same information found in normalized structures into simple, symmetric schemas. A fact table stores measurements from business process events at one defined grain. Dimension tables store the descriptive context that lets users filter, group, and label those measurements. Atomic data gives users flexibility for questions that the designer cannot predict.

## Frameworks Introduced

- **Business-driven goals of data warehousing and business intelligence**
  - **When to use:** Use these goals when defining requirements, judging architecture, or testing delivery.
  - **How:** Make information simple and fast, present consistent definitions, adapt to change, deliver timely information, protect sensitive data, support decisions, and earn business acceptance. Treat acceptance and decision value as the final tests, not technical elegance.

- **Publishing Metaphor for DW/BI Managers**
  - **When to use:** Use this model when setting team responsibilities and priorities.
  - **How:** Treat business users as readers. Understand their jobs and decisions, select relevant and accurate information, provide simple interfaces, monitor quality, publish regularly, adapt to new needs, and maintain user trust. Technology serves the readers rather than defining the product.

- **Kimball DW/BI Architecture**
  - **When to use:** Use it to separate data capture, preparation, presentation, and analysis.
  - **How:** Keep four components distinct: operational source systems, the extract, transformation, and load (ETL) system, the dimensional presentation area, and BI applications. Keep ETL off-limits to users. Publish dimensional, atomic, business-process-centric data through the presentation area.

- **Enterprise Data Warehouse Bus Architecture**
  - **When to use:** Use it to integrate multiple business processes and to guide iterative delivery.
  - **How:** Identify business processes and reusable conformed dimensions. Build dimensional models around measurement events, then share those dimensions across fact tables. Use the enterprise data warehouse bus matrix as the framework and master plan for incremental work.

- **Restaurant Metaphor for the Kimball Architecture**
  - **When to use:** Use it to explain why ETL and user-facing data must remain separate.
  - **How:** Treat ETL as a closed kitchen that transforms raw ingredients with throughput, quality, consistency, and integrity. Treat the presentation area as the dining room, where users receive safe, documented, timely, and usable data through reports and applications.

## Key Concepts

- **Operational system:** A system of record optimized for fast, repeated transaction processing, usually with limited history.
- **DW/BI system:** An analytical environment that searches many transactions, preserves historical context, and supports decision making.
- **Dimensional modeling:** A design technique that presents analytic data in simple structures for understandability and query performance.
- **Fact table:** A table that stores numeric performance measurements produced by business process events.
- **Grain:** The exact level of detail represented by one fact-table row. Every measurement row in one fact table must use the same grain.
- **Dimension:** A table that stores descriptive context about who, what, where, when, how, and why. Its attributes supply filters, groups, and report labels.
- **Conformed dimension:** A shared dimension with standardized labels, values, and definitions that links dimensional models across business processes.
- **Star schema:** A relational implementation of a dimensional model, with a fact table joined to surrounding dimension tables.
- **Atomic data:** The most detailed, unaggregated data available from a measurement event. It supports unexpected questions and later aggregation.
- **Surrogate key:** A key assigned during ETL processing for dimension-table rows, separate from operational identifiers, so the presentation model can manage dimensional data.

## Mental Models

- Use **grain first**. Define what one fact row means before selecting facts or dimensions, because mixed detail causes double-counting.
- Think of **dimensions as entry points** and **facts as measured results**. Attributes constrain and label a report, while facts supply its numeric values.
- Think of **atomic data as insurance against unknown questions**. Summary data can improve performance, but it cannot replace the detail needed for later analysis.
- Think of **business processes as the unit of work**. Do not let departments or current reports define the enterprise model.

## Anti-patterns

- **Copying operational systems into a separate platform:** This separates workloads but preserves poor analytical usability, limited history, and unsuitable query structures.
- **Putting normalized structures in the user-facing presentation area:** Complex 3NF schemas make business queries difficult to understand and can produce poor performance.
- **Publishing only summary data:** Users cannot drill into details, add new dimensions, or answer questions that the designer did not predict.
- **Snowflaking dimensions by default:** Normalizing small dimension hierarchies trades away simplicity and accessibility for little overall storage benefit.
- **Independent data marts:** Departmental silos apply different labels and rules, duplicate extracts, and produce conflicting numbers.
- **Designing for a fixed report list:** Reports change, but measurement processes remain more stable. Report-specific designs become moving targets.
- **Using agile work to create isolated stovepipes:** Fast delivery without the bus matrix can produce data that other teams cannot reuse or reconcile.

## Worked Example

Model retail sales as one business process. Define the grain as **one row per product sold on a sales transaction**. Each row records the event’s sales units and sales dollars. It carries foreign keys to the Date, Product, Store, Promotion, Customer, and Clerk dimensions, plus the transaction number.

The fact table contains only true sales activity. Do not add zero rows for products with no sale. Sales units and sales dollars are additive, so a BI application can sum them across any valid combination of date, product, store, or other dimensions. The dimensions provide readable attributes such as month, year, brand, category, district, and region.

For a report of sales by district and brand for a selected month and year, constrain the Date dimension, group by Store district and Product brand, and sum Sales Dollars from the fact table. The same atomic model can answer a later question about package type, customer state, or another combination without a new report-specific schema.

## Key Takeaways

- Start with business decisions and user needs before choosing tools.
- Define one grain for every fact table and keep every row at that grain.
- Store atomic measurements in the dimensional presentation area.
- Use verbose business attributes for filters, groups, and labels.
- Build by business process and reuse conformed dimensions.
- Keep ETL work centralized, quality-controlled, and separate from user queries.

## Connects To

- **Chapter 3: Retail Sales** develops transaction fact tables and the retail example.
- **Chapter 4: Inventory** develops periodic snapshot and accumulating snapshot fact tables and the enterprise data warehouse bus architecture.
- **Chapter 5: Procurement** discusses slowly changing dimension techniques and OLAP handling of Type 2 changes.
- **Chapter 17: Kimball DW/BI Lifecycle Overview** and **Chapter 18: Dimensional Modeling Process and Tasks** extend business-process planning and design work.
- **Chapter 19: ETL Subsystems and Techniques** expands the ETL system introduced here.
