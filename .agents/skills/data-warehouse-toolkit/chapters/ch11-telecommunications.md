# Chapter 11: Telecommunications

## Core Idea
A dimensional model needs a design review against both business requirements and operational source realities. Start with the business process, declare one precise grain, and then test every fact, dimension, key, hierarchy, and date against that grain. A process-centric model remains useful when reports and analytic questions change.

## Frameworks Introduced
- **Telecommunications bus matrix**: Use it to select a high-value business process and its shared dimensions. Start with customer billing, identify the common dimensions, and defer call-detail traffic when its cost exceeds its short-term business value.
- **Design review**: Use it when a draft schema needs a systematic search for design flaws. Invite a small group with modeling, BI, and business knowledge. Agree on scope, prepare sample rows, start at the bus matrix, declare the fact-table grain, peel back the layers of the onion through dimensions, record decisions, assign open issues, and schedule follow-up.
- **Process-centric dimensional modeling**: Use it instead of designing for one report or one question. Model the underlying business process event so several departments can analyze it and later report changes do not break the model.
- **Lowest level of granularity possible**: Use it when selecting the fact-table grain. Choose the most granular data available for the selected business process, not merely the most granular data available in the enterprise.
- **Single granularity for facts**: Use it after grain declaration. Keep all additive facts at the same grain, and move textual facts, cryptic indicators, and flags into dimensions with descriptive rollup attributes.
- **Peeling back the layers of the onion**: Use this review tactic to move from the bus matrix to one priority process, then to its fact table and dimensions. Sketch sample rows with data values while testing each design choice.
- **Conformity commitment**: Use shared conformed dimensions across process-centric models. Reuse dimensions to support consistent and integrated analysis instead of incompatible stovepipe views.
- **Retrofitting existing data structures**: Use a cost-and-benefit decision when a physical model needs correction. Compare remodeling, decommissioning, or leaving the structure unchanged. Account for fact reprocessing, historical recasting, and effects on BI applications.
- **Abstract geographic location dimension**: Keep location standardization in the ETL back room when useful, but expose geographic attributes within the dimensions that use them. Avoid a generic location dimension or outrigger in the presentation area unless its benefits justify its performance and usability costs.

## Key Concepts
- **Grain**: The exact business event represented by one fact-table row.
- **Fact table**: A process-centered table whose rows hold measurements at one declared grain.
- **Dimension**: A descriptive table whose attributes support filtering, grouping, and reporting.
- **Conformed dimension**: A shared dimension reused across fact tables so measurements remain comparable.
- **Degenerate dimension**: A transaction identifier, such as a bill number, stored in the fact table without a separate dimension table.
- **Surrogate key**: A warehouse-generated dimension primary key used instead of an operational identifier.
- **Textual fact**: A code, indicator, flag, or other text value incorrectly placed among fact measures.
- **Dimension hierarchy**: A many-to-one relationship represented as attributes within one denormalized dimension when possible.
- **Slowly changing dimension**: A dimension whose attribute-change strategy determines whether new rows, overwrites, or historical recasting are needed.
- **Date dimension**: An explicit dimension that gives a fact-table date a business meaning and supplies calendar rollup and filter attributes.

## Mental Models
- Ask, “What is the grain of the fact table?” before judging any other part of a design.
- Treat every fact as guilty of double counting until its additive behavior matches the declared grain.
- Treat a dimension with nearly as many rows as its fact table as a warning sign for a degenerate dimension.
- Treat a shared dimension as an integration contract across business processes, not as a local convenience.

## Anti-patterns
- **Designing for one report**: A report-specific schema breaks when users change filters, groupings, or report formats.
- **Requirements-only or source-only modeling**: Requirements-only designs include data that sources cannot provide. Source-only designs omit business-critical analytics.
- **Mixed-grain fact rows**: Year-to-date totals beside monthly facts invite double counting when queries include more than one date.
- **Text in fact tables**: Codes and flags consume space and give users poor query and reporting access. Store their descriptions in dimensions.
- **Snowflaked hierarchies and centipede fact tables**: Separate tables for simple rollups increase joins, reduce understandability, and can impair query performance. More than about 20 foreign keys signals a need to combine or collapse dimensions.
- **Fixed time series buckets**: Repeated month columns are inflexible, hide calendar attributes, and create null columns. Store recurring periods as separate fact rows with a date dimension.
- **Transaction-number dimensions**: A dimension with nearly as many rows as the fact table often misplaces a degenerate dimension. Keep the transaction number in the fact table and place transaction date and customer there as foreign keys.
- **Operational keys as dimension primary keys**: Source identifiers do not provide the warehouse’s required key stability. Use surrogate keys, except for the predictable date dimension.
- **Generic location dimensions**: A consolidated location table in the presentation area can reduce query performance and ease of use because addresses from different entities overlap little.

## Worked Example
The draft billing model declared one row per bill each month, but each service line carried separate minutes, messages, data, and charges. The review changed the grain to one row per service line per bill and moved the service line key into the billing fact table.

The team removed the bill dimension because it would nearly duplicate the fact table. It stored bill number as a degenerate dimension and linked bill date to a robust date dimension through bill date key. It collapsed sales channel into sales organization attributes, moved rate plan type code and its description into the rate plan dimension, and removed the redundant sales channel foreign key.

The revised billing fact used surrogate foreign keys for bill date, customer, service line, sales organization, and rate plan. It retained bill number, call counts, usage, and charges at the declared grain. It removed year-to-date service charge because users could calculate it with a year constraint on the date dimension. The review kept customer, sales organization, and rate plan as separate mini-dimensions of service line because collapsing them would leave only bill date and a rapidly growing service line dimension.

## Key Takeaways
- Declare the fact-table grain in one concise sentence before selecting facts or dimensions.
- Profile source data and compare it with business requirements before finalizing the model.
- Store each additive measure at one uniform grain and calculate year-to-date values from the date dimension.
- Use surrogate keys, descriptive decodes, degenerate dimensions, and explicit date roles.
- Collapse simple hierarchies into dimensions, and use snowflakes or outriggers only as exceptions.
- Review existing structures against cost, benefit, historical correctness, and BI application impact.
- Keep geographic standardization in ETL, but place usable location attributes in relevant dimensions.

## Connects To
- **Chapter 2: Kimball Dimensional Modeling Techniques**: Grain, dimensions, surrogate keys, and conformed dimensions provide the review vocabulary.
- **Chapter 3: Retail Sales**: The rationale for surrogate keys applies directly to this billing model.
- **Chapter 4: Inventory**: Conformed-dimension adoption can require complete fact-table reprocessing.
- **Bus architecture**: The telecommunications bus matrix extends process-centric integration across billing, activation, sales, support, inventory, and traffic.
- **Slowly changing dimensions**: Retrofitting a type 2 attribute can add dimension rows and recast existing fact rows.
