# Chapter 7: Accounting

## Core Idea

Model accounting as complementary dimensional processes, not as one universal ledger table. The general ledger needs a periodic snapshot for balances at the close of each accounting period and a journal transaction fact table for detail. The budget process needs a chain of budget, commitment, and payment fact tables. Each table must state its grain clearly, use dimensions that match that grain, and preserve atomic detail for drill-down.

Accounting analysis depends on shared definitions. A uniform chart of accounts acts as a conformed account dimension across organizations. The organization dimension may need an organization map bridge table when its rollup is ragged, changes over time, or includes shared ownership. The DW/BI system should complement operational financial statements, not replace them.

## Frameworks Introduced

- **Accounting case study and bus matrix:** Use this when planning the accounting subject area. Add rows for General Ledger Transactions, General Ledger Snapshot, Budget, Commitment, Payments, and Actual-Budget Variance. Mark their dimensions, then identify shared dimensions such as Date, Ledger, Account, Organization, Budget Line, Commitment Profile, and Payment Profile. Use the matrix to expose conformance needs and audience requirements.
- **General Ledger Periodic Snapshot:** Use this for balances at the end of each fiscal period. Set the grain to one row per accounting period for the most granular level in the chart of accounts. Store period end balance, debit, credit, and net change. Treat balance as semi-additive across time, while retaining it because recalculating it from the beginning of time is costly.
- **General Ledger Journal Transactions:** Use this when analysts must investigate a summary anomaly or inspect disparities hidden by monthly balances. Set the grain to one row for each general ledger journal entry transaction. Reuse account, organization, and ledger dimensions. Use a daily-grained post date and add an effective accounting date when source rules need a second date role.
- **Budgeting chain:** Use this for the event flow from approved budget to commitment to payment. Model separate budget, commitment, and payment fact tables. Start with budget amounts, add commitment document and party dimensions, then add payment and payee detail. Compare separate fact tables with a drill-across using multipass SQL.
- **Organization map bridge table:** Use this for a ragged variable depth hierarchy of indeterminate depth. Set its grain to each path from a parent to every child below that parent, including a parent-to-itself row. Store parent key, child key, depth from parent, highest parent flag, and lowest child flag. Join the bridge to the organization dimension and fact table to roll facts through the tree without traversing it at query time.
- **Consolidated fact tables:** Use this when users repeatedly compare measures from separate business processes. Combine facts only at a common grain and dimensionality, such as actual amount, budget amount, and budget variance by accounting period, account, and organization. Retain the atomic source facts for more detailed analysis.
- **OLAP and packaged analytic solutions:** Use OLAP for fast financial queries, complex organizational rollups, inter-row calculations, financial functions, and consolidation. Use packaged analytic solutions to reduce cost and risk when they fit the need. Conform their dimensions with the wider DW/BI environment.

## Key Concepts

- **Chart of accounts:** The general ledger structure that identifies accounts, account types, and rollups. Account type belongs as a dimension attribute, rather than as meaning hidden in account-number digits.
- **Uniform chart of accounts:** A master conformed account dimension whose account names have the same financial meaning across organizations.
- **Period close:** The finance process that reconciles and balances results before official internal and external reporting. DW/BI analysis focuses on closed results, although trial balances can help locate needed operational adjustments before close.
- **Semi-additive fact:** A measure, such as period end balance, that can aggregate across some dimensions but not across time. Its storage remains useful for direct period analysis.
- **Degenerate dimension:** A transaction identifier stored in the fact table without a related dimension table. A journal entry number can identify and order journal lines.
- **Year-to-date facts:** Stored to-date totals that do not match the fact grain. They produce overstated or nonsensical results under arbitrary summarization and should be calculated in the BI application.
- **Multiple fiscal accounting calendars:** Fiscal period systems that differ from the Gregorian calendar or vary by subsidiary. A fixed, low number can fit as parallel attributes in one date dimension. Many calendars can use a date dimension outrigger, separate physical date dimensions with common surrogate date keys, or a subsidiary fiscal period dimension.
- **Net change grain:** The amount by which a budget line changes during a month. Each change creates an additive row, so summing from the beginning of time yields the current approved budget without duplicated unchanged rows.
- **Fixed depth positional hierarchy:** A hierarchy with a fixed set of named levels, such as day, fiscal period, and year. Each level must have a meaningful business name.
- **Slightly ragged variable depth hierarchy:** A narrow hierarchy with a small range of missing levels. Populate missing attributes by propagating labels according to business governance rules, but only when the level names remain meaningful.
- **Ragged variable depth hierarchy:** A tree with an indeterminate number of levels. An organization map bridge table separates the rollup definition from the organization dimension.
- **Consolidated fact table:** A fact table that combines metrics from multiple business processes at a common granularity. It improves repeated comparison but can sacrifice dimensional detail.

## Mental Models

- **Choose the grain before the measure.** If a fact does not describe the declared grain, do not store it in the relational fact table.
- **Summarize, then investigate.** Use the periodic snapshot to find an anomaly, then use journal transactions to explain it.
- **Separate the tree from the nodes.** Store organization members in the dimension and rollup paths in the bridge so the hierarchy can change without relabeling the tree.
- **Conform before buying or building.** A packaged finance solution still needs conformed dimensions to integrate with customer, product, employee, and other subject areas.

## Anti-patterns

- **Storing year-to-date or quarter-to-date columns in a fact table:** These values violate grain and overstate results when users summarize arbitrary combinations. Calculate them in the BI application instead.
- **Leaving the ledger dimension unconstrained:** A fact table that stores multiple ledgers can double count values. Present separate views with the ledger pre-constrained to one value.
- **Promising that general ledger data will tie to operational reports:** Account and organization dimensions usually do not conform to customer, product, service, or facility dimensions. Explain this source-data limit during interviews.
- **Using abstract fixed hierarchy levels:** Names such as Level-1 and Level-2 hide a ragged hierarchy and give users no clear constraint or report meaning.
- **Using recursive pointers as the main ragged hierarchy solution:** Recursive pointers entangle the rollup with the organization dimension. Type 2 changes and rollup changes can ripple through many keys.
- **Using pathstring or modified preordered tree traversal without assessing change cost:** These alternatives can cause a relabeling disaster. A small tree change may require relabeling much of the tree.
- **Forcing unlike facts into one consolidated fact table:** Facts from different grains cannot support a one-to-one correspondence. Do not invent artificial facts or dimensions to force the fit.
- **Creating stovepipe packaged analytics:** Separate vendor solutions for finance, CRM, human resources, and ERP may not integrate. Conform dimensions across the complete environment.

## Worked Example

A company stores annual budgets for each cost center and budget line. Finance needs current budget, monthly changes, commitments, payments, and actual-budget variance. Model the budget fact at the net change of a budget line for an organization and G/L account during the effective month. The original approved amount becomes one row. A $40,000 June increase becomes a second row, and a $25,000 October reduction becomes a third row with a negative amount. Summing all rows through October returns the current approved amount. Filtering June returns only the June change.

Create separate commitment and payment facts that reuse the month, organization, account, and budget dimensions. Add commitment document and party details to commitments. Add payment type and payee details to payments. Compare budget and commitments by separately summing each fact through the selected month, then combine the result with a drill-across. If users make actual-versus-budget analysis frequently, create a consolidated fact at the common accounting-period, account, and organization grain. Keep the budget, commitment, payment, and journal facts for drill-down.

## Key Takeaways

- Declare the grain for every accounting fact before selecting measures.
- Pair a general ledger periodic snapshot with journal transaction detail.
- Use a uniform chart of accounts when account meanings must conform across organizations.
- Store budget changes as additive net-change rows, not monthly status snapshots.
- Use an organization map bridge table for flexible, shared, or time-varying ragged rollups.
- Constrain a ledger or time-varying bridge to one consistent value or date.
- Combine business-process facts only at a common grain and dimensionality.

## Connects To

- **Chapter 3: Retail Sales:** Reuses the four-step dimensional design process and grain-first reasoning.
- **Chapter 6: Order Management:** Provides the multiple-currency pattern for local and corporate currency facts.
- **Conformed dimensions:** Links the uniform chart of accounts and shared organization dimensions to enterprise integration.
- **Drill-across and multipass SQL:** Supports comparisons across budget, commitment, payment, and consolidated variance processes.
- **Slowly changing dimension and surrogate key techniques:** Explain why bridge tables limit the impact of organization changes and support parent snapshot relationships.
