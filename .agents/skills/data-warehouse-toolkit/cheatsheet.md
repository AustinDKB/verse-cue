# Cheatsheet

## Start with the grain

| Question | Rule |
|---|---|
| What is one row? | Write one concise business sentence before columns. |
| Does a dimension fit? | Keep it only if it has one value per fact row. |
| Does a fact fit? | Keep it only if it measures the declared event. |
| Do rows multiply? | Stop. Split the grain, allocate the fact, or use a bridge. |

## Choose the fact pattern

- **Point event** → Transaction Fact Table.
- **Regular state or balance** → Periodic Snapshot Fact Table.
- **Finite workflow with known milestones** → Accumulating Snapshot Fact Table.
- **Arbitrary status interval** → Timespan Fact Table.
- **Event or relationship without a measure** → Factless Fact Table.
- **Possible use versus actual use** → Coverage Factless Fact Table.
- Need both event detail and state? Build complementary facts. Do not force one table to answer both.

## Integrate the enterprise

1. Put business processes in the **Enterprise Data Warehouse Bus Matrix**.
2. Put reusable dimensions in columns at the lowest common grain.
3. Reuse **Conformed Dimensions** and **Conformed Facts**.
4. Compare separate facts with **Drill Across** or multipass SQL.
5. Never join fact tables directly through a shared dimension.

## Select history per attribute

| Need | Choice |
|---|---|
| Original value only | Type 0: Retain Original |
| Correction or current value only | Type 1: Overwrite |
| Accurate point-in-time history | Type 2: Add New Row |
| Current and one prior value | Type 3: Add New Attribute |
| Large, volatile attribute group | Type 4: Add Mini-Dimension |
| Current and historical paths | Type 5, Type 6, or Type 7, only with governance approval |

Default to Type 2 when history matters or the decision remains open. Type 1 cannot recover lost history.

## Fast smells

- More than about 20 fact foreign keys → collapse hierarchies or combine correlated dimensions.
- A dimension nearly as large as its fact → use a Degenerate Dimension.
- Year-to-date columns in facts → remove them and calculate with the Date Dimension.
- Null foreign keys → use explicit Unknown, No Promotion, or Not Applicable rows.
- Generic “person,” “location,” or “level” dimensions → separate clear business dimensions.
- One mini-dimension per attribute → group correlated attributes into clumps.
- Unweighted many-to-many bridge → label totals as impact reports because they can overcount.
- Raw clickstream dump → derive session and page-event facts with identity and time context.

## ETL order and quality

- Profile sources early. Record source limits and data-quality defects.
- Capture inserts, edits, deletes, reason codes, and compliance metadata.
- Archive raw extracts and stages with lineage.
- Load dimensions before facts. Resolve each fact key to the correct Type 2 row.
- For late dimensions, create a keyed dummy row, then overwrite or add history when details arrive.
- Tag minor quality failures when risk permits. Halt or suspend only serious failures.

## Latency and big data

- **Instantaneous need** → EII or streaming, with provisional quality.
- **Intra-day need** → micro-batch ETL.
- **Daily need** → conventional batch ETL.
- Prefer **Extended RDBMS** for indexed relational work.
- Prefer **MapReduce/Hadoop Architecture** for flexible structure, massive scans, and complex branching.
- Use **Data Highway** caches by need. Add value early, protect sensitive data, and use durable surrogate keys across boundaries.
