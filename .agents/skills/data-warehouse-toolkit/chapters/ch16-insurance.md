# Chapter 16: Insurance

## Core Idea

Design the insurance DW/BI system from business requirements and measurement processes, not from reports or operational silos. Start with the insurance value chain, identify the grain of each process, and place each measurement in a dimensional model that preserves its required context. Policy transactions, premium revenue, claim events, and claim workflow need complementary schemas because they answer different questions. Conformed dimensions and facts then connect these models for enterprise analysis.

The insurance case uses a requirements-driven approach to dimensional design. The initial enterprise data warehouse bus matrix focuses on reusable dimensions, not every possible dimension. The policy transaction and premium snapshot rows later expand when claim requirements appear. During implementation, the team can refine a high-level process row into separate fact tables or OLAP cubes with explicit grain and metrics.

## Frameworks Introduced

- **Insurance value chain and enterprise data warehouse bus matrix** — Use this during requirements analysis to organize core policy and claim processes against shared dimensions. Begin with policy transactions and a monthly premium snapshot. Add claim transactions and claim-related dimensions when interviews expose that need. Keep the planning matrix high-level, then create a detailed implementation matrix with each resulting fact table, grain, and metric.
- **Complementary transaction, periodic snapshot, and accumulating snapshot schemas** — Use a transaction fact table for every atomic event, a periodic snapshot for status or activity at regular intervals, and an accumulating snapshot for a predictable workflow with milestone dates. Use the schemas together when users need both event detail and current or period-based measures.
- **Dimension role playing** — Use one physical date dimension through separate logical views when a fact table contains distinct dates, such as policy transaction date and policy effective date. Give each foreign key a unique role name.
- **Heterogeneous supertype and subtype technique** — Use a shared enterprise supertype when metrics remain common across lines of business, then add subtype dimensions or snapshots for attributes and facts that apply only to automobile, homeowner, or another coverage type. Use views to present line-specific data without duplicating the shared fact design.
- **Timespan accumulating snapshot** — Use this when a workflow has a definite start and end but users must reconstruct its state at any past date. Insert a new row for each state span, with snapshot start date, snapshot end date, and snapshot current flag.
- **Consolidated fact table** — Use this after delivering separate atomic policy and claim models, when users frequently drill across premium revenue and claim loss. Combine metrics at the lowest common grain and retain a reduced, conformed dimension set.

## Key Concepts

- **Policy transaction fact table**: One row records one individual policy transaction, such as creation, alteration, cancellation, rating, or underwriting.
- **Premium periodic snapshot**: One row records each coverage and covered item on a policy for each month. It stores written and earned premium separately.
- **Claim transaction fact table**: One row records one claim task transaction, such as opening, reserving, inspection, payment, lawsuit activity, or closing.
- **Claim accumulating snapshot**: One row represents one claim. The row begins at claim opening and updates through closure, while milestone dates, lags, and to-date amounts show workflow progress.
- **Grain**: The declared business level of one fact row. Each measurement grain requires its own fact table.
- **Conformed dimension**: A dimension that remains identical, or a carefully chosen shrunken subset, across fact tables. It enables matching filters, row labels, and drill-across analysis.
- **Conformed fact**: A repeated metric with the same definition and label across fact tables. Different definitions require different names.
- **Mini-dimension**: A type 4 dimension that stores closely monitored, rapidly changing attributes separately from a large dimension. A separate surrogate key in the fact row tracks the attribute combination over time.
- **Junk dimension**: A dimension for low-cardinality indicators and coded descriptions. The claim profile dimension groups unique combinations such as loss-report method and catastrophe status.
- **Factless fact table**: A table that records key combinations at a point in space and time. An accident involvement table can include a count fact valued at one to support aggregation.

## Mental Models

- Model the event stream and the business state separately. Transactions preserve detail, while snapshots make status, revenue, and workflow measures directly available.
- Let grain control every key and measure. If a fact does not match the declared grain, place it in another fact table.
- Share meaning before sharing storage. Conformed dimensions and conformed facts make separate processes analytically compatible.
- Use the simplest structure that preserves required history. Choose SCD type 1 for corrections, type 2 for accurate change history, type 3 for a limited old-versus-new classification view, and a mini-dimension for large, rapidly changing attributes.

## Anti-patterns

- **Place text attributes in a fact table**. Text used for filtering, grouping, or labels belongs in a dimension.
- **Limit verbose descriptors to save space**. Dimension tables are usually much smaller than fact tables, and readable descriptions support browsing and reports.
- **Split fixed-depth hierarchies into multiple dimensions**. Keep a hierarchy in one flat dimension unless data volume or change velocity gives a clear reason to separate it.
- **Ignore dimension changes**. Type 1 alone cannot provide historical analysis, and rapidly changing attributes need a mini-dimension when appropriate.
- **Use operational keys to join dimensions and facts**. Use sequential integer surrogate keys, except for the date dimension.
- **Neglect the fact grain**. Extra totals at another time or geographic grain cause automatic aggregations to overcount.
- **Use a report to design the model**. Design around measurement processes, then use aggregates for report performance.
- **Expect users to query normalized atomic data**. Use normalized models in the ETL kitchen, not as the business-facing dimensional model.
- **Fail to conform facts and dimensions**. Unmatched definitions create isolated data repositories and prevent reliable drill-across analysis.

## Worked Example

An annual coverage costs $600 and starts January 1. The monthly premium snapshot has one row for the coverage and covered item in each month. January stores $600 as written premium and $50 as earned premium. February stores zero written premium and $50 earned premium. If cancellation occurs March 31, March stores negative $450 written premium and $50 earned premium. Later months stop the earned revenue stream. The transaction fact table still retains the policy creation and cancellation events. The two fact tables together answer both transaction-timing questions and earned-income questions without forcing users to replay complex revenue-recognition rules.

## Key Takeaways

- Declare the grain before selecting facts, dimensions, or keys.
- Build transaction and snapshot fact tables when event detail and business-state analysis conflict.
- Reuse conformed dimensions, and define repeated facts consistently.
- Use role-playing date views for distinct business dates.
- Apply SCD techniques deliberately, and use mini-dimensions for large, volatile attribute groups.
- Add accumulating snapshots for workflow milestones and timespan snapshots for historical state reconstruction.
- Deliver consolidated fact tables only after separate atomic models establish trustworthy base metrics.

## Connects To

- **Chapter 4: Inventory** — Accumulating snapshots represent predictable pipeline milestones, while periodic snapshots represent regular status intervals.
- **Chapter 5: Procurement** — Transaction fact table design requires a choice between separate natural transaction clusters and one combined process.
- **Chapter 6: Order Management** — Role-playing date dimensions, audit dimensions, and junk dimensions apply directly to policy and claim schemas.
- **Chapter 7: Accounting** — Consolidated fact tables combine metrics from multiple business processes at a common grain.
- **Chapter 9: Human Resources Management** and **Chapter 14: Healthcare** — Bridge tables and weighting factors model multivalued relationships.
- **Chapter 10: Financial Services** — Supertype and subtype structures handle heterogeneous business attributes.
