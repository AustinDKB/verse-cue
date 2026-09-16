# Chapter 8: Customer Relationship Management

## Core Idea

Customer relationship management (CRM) treats the customer as the central business subject. Its goal is to maximize valuable relationships over the customer lifetime by integrating marketing, sales, operations, and service. The data warehouse provides the historical, integrated foundation for a 360-degree customer view. Effective CRM therefore depends on a well-maintained conformed customer dimension, shared customer identifiers, and data collected at every customer touch point.

CRM has two linked roles. Operational CRM synchronizes customer-facing processes and shares current customer characteristics across touch points. Analytic CRM stores the resulting history, measures past decisions, finds opportunities, and returns scores or recommended actions to operational systems. This creates a closed loop analytic CRM: collect, integrate, store, analyze, model, and feed model results back to the point of customer contact.

## Frameworks Introduced

- **Closed loop analytic CRM:** Use when analysis must improve the next customer interaction. Collect touch-point data, integrate it through ETL, store history, analyze behavior, model recommendations, and return those results to a representative, call center, or website.
- **Parsed name and address design:** Use when customer text must support matching, segmentation, greetings, postal validation, or geographic analysis. Decompose general-purpose fields into elemental attributes, standardize values, verify combinations, and preserve international characters through Unicode across the full data pipeline.
- **Behavior Tag Time Series:** Use when customer behavior needs pattern queries across reporting periods. Calculate RFI or RFM measures, assign each customer a behavior tag, and store one positional attribute per period plus an optional concatenated tag string. Do not store these textual tags as regular facts.
- **Dimension outrigger:** Use as an exception when a large, low-cardinality attribute set has a different grain, load schedule, or analytic value. Link the customer dimension to the outrigger with a foreign key, as with county demographics or role-playing date dimensions. Avoid broad snowflaking.
- **Bridge table for multivalued dimensions:** Use when a transaction or customer can have an unpredictable number of values, such as hobbies, diagnoses, or contacts. Store only needed relationships in bridge rows, and hide the complex query from business users when possible. Choose a positional design instead when the bounded attribute set remains manageable.
- **Behavior Study Groups for Cohorts:** Use when a complex query identifies a reusable customer set. Capture the customers’ durable keys in a physical study group table, then constrain later fact analysis through the customer durable key. Add an occurrence date when the study tracks behavior after a qualifying event.
- **Step Dimension for Sequential Behavior:** Use when events must be analyzed within a session or another ordered process. Prebuild rows containing total number of steps, this step number, and steps until end, then attach roles such as overall session, successful purchase, and abandoned cart.
- **Timespan Fact Tables:** Use when analysts need a customer status at an arbitrary instant or across an interval. Store begin effective date/time and end effective date/time for each event, with the next transaction beginning exactly when the prior span ends.
- **Partial Conformity of Multiple Customer Dimensions:** Use when many customer sources differ in grain and quality, making one comprehensive dimension impossible. Administer a small set of shared attributes, such as customer category or geography, across separate dimensions, then expand conformity incrementally.

## Key Concepts

- **Conformed customer dimension:** A shared customer dimension with common names, values, and meanings across processes. It enables integrated analysis and drill-across reporting.
- **Customer durable key:** An identifier for the underlying customer that remains stable when Type 2 dimension rows change. Study groups use it to remain valid after later customer changes.
- **Aggregated facts as dimension attributes:** Frequently used measures, such as last year’s spending, stored in the customer dimension for filtering and labeling. They support constraints, not numeric calculations, and require ETL maintenance.
- **RFI/RFM measures:** Recency measures time since the last behavior, frequency counts behaviors over a period, and intensity or monetary measures amount spent. Quintile values can locate customers in an RFI cube.
- **Positional design:** A design that gives each known attribute or time position its own named column. It offers simple queries and good performance but scales poorly when values or columns become unpredictable.
- **Bridge table:** A sparse relationship table that represents multivalued membership without null-filled columns. It improves scalability but can exceed normal BI tool SQL capability.
- **Behavior study group dimension:** A physical table of customer durable keys that preserves a selected cohort for repeated analysis. Union, intersection, and set difference can combine study groups.
- **Timespan fact:** A fact row whose paired timestamps define the interval during which its customer status and demographics remain constant. Interval predicates can find overlap and calculate time in a status.

## Mental Models

- Treat the conformed customer dimension as CRM’s integration cornerstone, not as a passive list of names.
- Choose positional design for bounded, stable attributes. Choose a bridge table when the attribute set grows, stays sparse, or cannot be predicted.
- Move complex cohort logic into captured keys before analysis. Let later queries use the study group instead of repeating the original exception logic.
- Trade ETL complexity for query simplicity when the business benefit justifies it, as with twin timestamps and behavior study groups.

## Anti-patterns

- **General-purpose name and address columns:** They hide salutations, names, roles, address elements, and postal errors. They block useful matching and segmentation.
- **Uncontrolled dimension outriggers:** Many outriggers indicate that normalization has replaced a usable star design. Use an outrigger only for a justified, low-cardinality attribute cluster.
- **Regular fact storage for behavior tags:** Textual time-series tags cannot be averaged or computed as numeric facts, and pattern queries become difficult correlated-subquery chains.
- **Direct fact-to-fact joins through one dimension:** A many-to-one-to-many join between facts with different cardinalities multiplies rows and returns wrong measures. Query each fact separately and use drill-across, or build a governed consolidated fact table.
- **Generic hierarchy levels:** Names such as Level-1 and Level-2 do not express ragged customer hierarchy meaning. Use fixed depth, slightly variable, or ragged hierarchy techniques according to the actual structure.
- **Unqualified low latency promises:** Faster delivery can expose incomplete transactions, unresolved keys, fragments, and weaker data quality checks. Define the trade-off and consider intraday delivery with nightly batch correction.

## Worked Example

A retailer wants to identify customers whose behavior is deteriorating. Each period, a data miner assigns an RFI-based behavior tag: A means high-volume repeat customer with good credit and few returns, while B means high volume with many returns. John Doe’s ten-period sequence is `CCCDDAAABB`. Store these ten values as positional attributes in the customer dimension and also store the concatenated string `CCCDDAAABB`. Analysts can query for customers who held tag A in earlier periods and tag B in recent periods, without a cascade of correlated subqueries. A contemporary tag can also reside in a minidimension for analysis of fact rows by the tag active at load time.

## Key Takeaways

- Build and govern one conformed customer dimension where source integration permits.
- Parse, standardize, verify, and Unicode-enable name and address data end to end.
- Store only frequently used aggregated facts as dimension attributes, and keep them consistent with fact rows.
- Capture reusable cohorts as behavior study groups keyed by durable customer identifiers.
- Use step dimensions and timespan facts when sequence or exact historical status matters.
- Prevent fact-to-fact cardinality errors with drill-across or an explicitly governed consolidated fact.
- Match latency promises to transaction completeness and data quality capacity.

## Connects To

- **Chapter 1:** DW/BI architecture and the warehouse as the integrated historical foundation.
- **Chapter 4:** Conformed dimensions, drill-across, and integration across business processes.
- **Chapter 7:** Fixed, slightly variable, and ragged hierarchy techniques for commercial customers.
- **Chapter 19:** ETL administration for bridge tables, matching, cleansing, and twin timestamps.
- **Chapter 20:** ETL effects of low latency delivery and data quality trade-offs.
- **Chapter 21:** Big data analytics for external behavioral data and customer touch points.
