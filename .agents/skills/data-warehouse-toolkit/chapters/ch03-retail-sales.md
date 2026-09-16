# Chapter 3: Retail Sales

## Core Idea

Dimensional modeling starts with the business process and its measurable events, not with source tables. The design must state the grain in business terms before it selects dimensions or facts. For retail sales, the strongest foundation is atomic POS detail: one row per individual product line on a customer transaction. Atomic grain preserves the dimensions known at the event and lets users summarize or filter the data in many ways. Premature aggregation creates an analytic wall because a summary cannot recreate detail.

## Frameworks Introduced

- **Four-Step Dimensional Design Process** — Use this for every dimensional model. Select the business process, declare the grain, identify the dimensions, then identify the facts. Revisit step two when later decisions show that the grain does not fit.
- **Atomic-grain design** — Use this when the source captures detailed events and users need flexible analysis. State the lowest practical business grain, then attach dimensions and facts that hold one value at that grain.
- **Fact-table dimensionality test** — Use this when evaluating an additional dimension. Add it only when it has one value for each measurement at the declared grain. If it creates extra fact rows, reject the dimension or restate the grain.
- **Additive-fact method** — Use this when selecting measures. Store quantities and extended dollar amounts that can sum across every dimension. Store numerators and denominators for ratios, then calculate the ratio of sums.
- **Dimension role playing** — Use this when one date dimension describes different dates, such as a store opening date and a sales date. Expose distinct logical views with unique names and meanings.
- **Factless fact table technique** — Use this to analyze an event or relationship, including what did not happen. Record the eligible keys at their own grain, with no measures or an optional constant count of one.

## Key Concepts

- **Business process:** A low-level organizational activity that generates or captures performance measurements, such as POS retail sales transactions.
- **Grain:** The exact business meaning of one fact table row. It determines the detail level, primary dimensionality, and valid facts.
- **Transaction fact table:** A sparse, highly dimensional table that records atomic events. It can become very large, while its extended measures remain additive.
- **Additive fact:** A measure that can sum correctly across all dimensions, such as sales quantity or extended sales dollar amount.
- **Non-additive fact:** A measure that cannot be summed across dimensions, such as unit price or gross margin. Calculate weighted prices from total dollars divided by total quantity.
- **Derived fact:** A calculated measure stored consistently when its source values exist at the same row, such as extended gross profit from extended sales less extended cost.
- **Causal dimension:** A promotion dimension that describes conditions believed to affect sales, including price reductions, ads, displays, and coupons.
- **Degenerate dimension:** A transaction control number kept in the fact table without a related dimension table, such as a POS transaction number.
- **Conformed dimension:** A shared descriptive dimension that supports consistent analysis across business processes. The chapter applies the broader rule that data should publish once rather than duplicate across departments.
- **Surrogate key:** A meaningless integer key assigned by the warehouse for dimension joins. A natural key remains an attribute, while a durable supernatural key preserves entity identity across natural-key changes.

## Mental Models

- **Grain is the contract.** Every dimension and fact must describe the event at that exact level. A fact from another grain belongs in another fact table.
- **Dimensions describe; facts measure.** Use dimensions for who, what, where, when, why, and how. Use facts for measurements that users analyze.
- **Detail creates options.** Atomic rows support later rollups, but summary rows cannot restore missing detail.
- **Wide dimensions beat wide facts.** Flatten fixed-depth hierarchies in dimensions, and combine correlated dimensions instead of building a centipede fact table.

## Anti-patterns

- **Skipping grain declaration:** This allows rogue facts and incompatible dimensions into one table. The team must state and agree on the row meaning first.
- **Modeling departments instead of processes:** Departmental models duplicate labels and values. Model the underlying processes and publish shared information once.
- **Using null foreign keys:** Null keys break referential integrity and confuse joins. Add dimension rows such as No Promotion, Unknown, or Not Applicable.
- **Summing ratios or unit prices:** These results have no valid meaning. Sum the relevant additive measures first, then calculate the ratio or weighted value.
- **Snowflaking fixed-depth hierarchies:** Snowflaked dimensions increase joins, reduce browsing simplicity, and usually save insignificant space. Flatten repeated low-cardinality attributes.
- **Building centipede fact tables:** Separate keys for every hierarchy level inflate the largest table and make joins and indexing difficult. Combine correlated attributes in dimensions.
- **Changing the grain to fit payment methods:** Multiple payment methods per transaction need a separate payment fact table, not an unnatural product-by-payment grain.

## Worked Example

A grocery chain models POS sales at one row per product line on a transaction. The row links date, product, store, promotion, cashier, and payment method, and keeps the POS transaction number as a degenerate dimension. It stores quantity, regular and discount prices, extended discount, extended sales, extended cost, and extended gross profit. Sales, quantity, discount, and cost amounts sum across dimensions. Gross margin does not. For a widget example, one unit at $1.00 and four units at $0.50 produce $3.00 sales and five units. The valid average unit price is $0.60, calculated as $3.00 divided by five, not the sum or simple average of line prices.

## Key Takeaways

- Select a critical and feasible business process.
- Declare one precise, atomic grain before listing columns.
- Add dimensions only when they hold one value at that grain.
- Store additive measures and the components needed for non-additive calculations.
- Use explicit date dimensions with calendar, fiscal, holiday, and weekday attributes.
- Use surrogate keys for dimension joins and descriptive default rows for unknown states.
- Add a factless fact table when the business must analyze eligible events without sales.

## Connects To

- **Chapter 4: Inventory** — Extends the retail case to another business process and reinforces shared dimensional design.
- **Chapter 5: Procurement** — Continues product attributes and introduces slowly changing dimension handling.
- **Chapter 6: Order Management** — Develops dimension role playing and related date views.
- **Chapter 19: ETL Subsystems and Techniques** — Covers surrogate-key administration and durable identifier processing.
- **Bus matrix and conformed dimensions** — The process-first design supports consistent dimensions across the enterprise.
