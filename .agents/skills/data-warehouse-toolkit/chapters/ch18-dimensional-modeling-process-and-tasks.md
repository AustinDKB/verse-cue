# Chapter 18: Dimensional Modeling Process and Tasks

## Core Idea
Dimensional modeling is a collaborative, iterative process that moves from business requirements and a bus matrix to a tested model. The team first declares the grain and scope, then defines dimensions, facts, source rules, data quality concerns, and transformations through repeated review.

The process must include business representatives, source-system experts, and data stewards. Its main goals are to meet business requirements, confirm that usable data exists, and give the ETL team a strong source-to-target starting point.

## Frameworks Introduced
- **Dimensional modeling process flow**: Use when a team starts a model for one business process. Prepare the team, create a high-level dimensional model, develop the detailed model, review and validate it, iterate and test, then finalize the design documentation. Treat the flow as iterative, not linear.
- **Four key decisions**: Use when translating a prioritized bus matrix row into a dimensional model. Identify the business process, declare the grain, identify the dimensions, and identify the facts. Revisit the grain when a proposed dimension does not match it.
- **High-level model diagram (bubble chart)**: Use before detailed table design to establish scope and granularity with technical and non-technical participants. Draw the fact table and its associated dimensions, state the grain clearly, and reach team consensus before examining columns.
- **Detailed dimensional design worksheets**: Use when the team must communicate table and column decisions to stakeholders and ETL developers. Document attributes, facts, descriptions, sample values, sources, source fields, data types, ETL rules, and slowly changing dimension type indicators.
- **Issues tracking log**: Use throughout design when the team finds unresolved definitions, transformation rules, or data quality challenges. Assign each issue, review new entries at the end of every session, and track resolution between sessions.
- **Conformed dimension strategy**: Use across an enterprise to keep business rules, names, definitions, and values consistent across business processes. Involve data stewards and business groups to build organizational consensus.

## Key Concepts
- **Grain**: The exact business event represented by one fact-table row.
- **Fact table**: A table whose metrics and foreign keys all remain true at the declared grain.
- **Dimension**: A table that supplies descriptive context for a fact-table event.
- **Conformed dimension**: An enterprise dimension with shared definitions, names, and values across business processes.
- **Bus matrix**: A communication and planning tool that identifies business processes, dimensions, and, during detailed design, fact-table granularity and metrics.
- **Bubble chart**: An entity-level diagram that shows a business process, its fact table, associated dimensions, and declared grain.
- **Data profiling**: Query-based examination of source data content, structure, relationships, and derivation rules.
- **Slowly changing dimension technique**: A rule for representing source-system changes for each dimension attribute.
- **Design worksheet**: A table-specific record of attributes, metrics, sources, rules, data types, and related design details.
- **Issues tracking log**: A maintained list of design issues, assignments, and progress toward resolution.

## Mental Models
- Use the grain as the model’s test. If a dimension or metric does not fit the grain, change the design, omit the item, or consider a multivalued design solution.
- Think of the bubble chart as a shared contract. Secure agreement on scope and granularity before the team spends time on column details.
- Use business requirements and source data together. Requirements prevent a source-driven model, while profiling prevents a design that the sources cannot populate.
- Treat names and definitions as business decisions. Technical agreement alone does not create a usable conformed dimension.

## Anti-patterns
- **Modeling alone**: A single modeler lacks the full business and source-system knowledge needed for a complete design. Collaboration adds richer requirements and exposes source realities.
- **Skipping the requirements review**: A design that starts with source data usually supports existing data rather than the business value required for analysis.
- **Applying third normal form rules to the dimensional model**: This shifts dimensional complexity into the BI layer or creates a presentation layer that lacks simplicity and predictability.
- **Deferring complexity to BI applications**: The design should trade ETL processing complexity for a simpler and more predictable BI presentation layer.
- **Using an outside expert as a disappearing designer**: A completed design returned after several weeks prevents team learning and hides trade-offs. The expert should facilitate the team process.
- **Treating the process as linear**: New source findings and business decisions can add, split, or combine fact tables and dimensions. Failing to revisit the bus matrix leaves the plan inaccurate.
- **Using vague labels**: Names such as “Description” communicate little in reports. Agree on descriptive, consistent, business-friendly names and definitions.

## Worked Example
A team selects an orders row from the bus matrix and begins a high-level model. The team declares the grain as **one row per order line**. This decision makes the sales fact table represent line-level measurements rather than one row for an entire order.

The team then attaches dimensions that describe each order-line event: Order Date, Due Date, Sold To Customer, Ship To Customer, Bill To Customer, Currency, Promotion, Channel, Product, Order Profile, and Sales Person. The grain clarifies why these dimensions belong in the model and exposes any dimension that does not describe an order line.

During detailed design, the team defines Order Profile as a junk dimension for miscellaneous order information. It records Order Method, Order Source, and Commission Indicator, with source fields, example values, ETL rules, and slowly changing dimension type indicators. The team documents the Orders fact table separately, confirms that each metric is true at order-line grain, identifies foreign keys and any degenerate dimensions, and classifies facts as additive, semi-additive, or non-additive.

The team profiles the source, records unresolved data-quality and definition issues, updates the bus matrix if new facts appear, and reviews the model with IT and business representatives before finalization.

## Key Takeaways
- Involve business representatives, source experts, ETL staff, DBAs, and data stewards before modeling starts.
- Review business requirements before examining source details.
- Translate the selected bus matrix row into a bubble chart and declare the grain explicitly.
- Define dimensions before facts, then make every metric conform to the declared grain.
- Use data profiling to test data availability, relationships, derivations, and manageable defects.
- Record sources, definitions, ETL rules, slowly changing dimension techniques, and open issues in design worksheets.
- Review the bus matrix and model repeatedly, then compile the final diagram, worksheets, and open issues.

## Connects To
- **Chapter 3: Retail Sales**: Supplies the four key dimensional-modeling decisions and the grain-centered design approach.
- **Chapter 16: Insurance**: Shows how a detailed bus matrix can capture fact-table granularity and metrics.
- **Chapter 17: Kimball DW/BI Lifecycle Overview**: Provides the requirements and prioritization inputs for modeling.
- **Chapter 19: ETL Subsystems and Techniques**: Extends the source-to-target and ETL concerns identified during detailed modeling.
- **Conformed dimensions**: Links individual business-process models into an integrated enterprise DW/BI environment.
