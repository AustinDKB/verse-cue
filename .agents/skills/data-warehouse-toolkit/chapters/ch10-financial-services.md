# Chapter 10: Financial Services

## Core Idea

Model financial services around the business process grain, then preserve both the integrated portfolio view and each line of business's special detail. A retail bank needs a monthly account snapshot with common measures, plus designs for household relationships, multivalued customers, changing profiles, flexible value bands, and heterogeneous products. Separate dimensions improve analytic entry points, usability, and type 2 slowly changing dimension control. The chapter's patterns apply beyond banking when one customer base uses varied products.

## Frameworks Introduced

- **Bus matrix snippet for a bank:** Use it when a bank must align processes with shared dimensions. List processes such as account initiation, account transactions, account monthly snapshot, and account servicing activities, then mark their common dimensions, including date, prospect, customer, household, branch, account, and product. Use the matrix to expose reuse and conformed dimensions before designing facts.
- **Dimension triage:** Use it when an initial fact table has too few dimensions. Start with the declared grain, inspect descriptive data that users analyze, and test for causal, multiple date, degenerate, role-playing, status, audit, and junk dimensions. Add a dimension when it offers a natural analytic entry point or a single-valued description of the fact measurements without changing grain.
- **Account-to-customer bridge table with weighting factor:** Use it when an account has multiple customers but the fact remains at account grain. Store account and customer surrogate keys, and assign weights that sum to 1.00 for each account. Apply weights for correctly allocated totals, or omit them for an impact report that knowingly permits overcounting.
- **Multiple mini-dimensions in a single fact table:** Use type 4 mini-dimensions when demographic, credit bureau, risk, or behavior attributes change too quickly for a large type 2 dimension. Group correlated attributes, place each mini-dimension key in the fact table, and record the key at each periodic snapshot.
- **Dynamic value banding of facts:** Use it when users need query-time ranges for a numeric fact. Store band groups, names, sort order, lower values, and upper values in a band definition table. Join the table to the fact with less-than and greater-than conditions, and optimize scans with a suitable fact index when needed.
- **Supertype and subtype schemas for heterogeneous products:** Use a supertype fact table for common measures across all products, and use one subtype schema per line of business for special facts and attributes. Reuse the same surrogate keys, and make each subtype dimension a shrunken conformed dimension of the supertype dimension.
- **Hot swappable dimensions:** Use it when many clients need one shared fact table but each client needs confidential dimension attributes. Keep one fact table and switch the joined dimension copy at query time. Relational implementations may need referential integrity constraints disabled for these query-level switches.

## Key Concepts

- **Grain:** The monthly account snapshot grain is one row for each account each month. Declare this before selecting dimensions or facts.
- **Monthly account snapshot fact:** This fact table records primary month-ending balance and common measures such as transaction count, interest paid, and fees charged.
- **Household dimension:** This dimension represents an economic unit that can contain several accounts and account holders. Its demographic attributes change over time.
- **Multivalued dimension:** A customer is multivalued for an account-grained fact because one account can have several holders. A customer cannot become an ordinary fact-table dimension without changing grain.
- **Weighting factor:** This numeric allocation value assigns each account holder a share of additive facts. All holder weights for one account sum to exactly 1.00.
- **Correctly weighted report:** A report that applies bridge weighting factors and preserves the correct grand total across account holders.
- **Impact report:** A report that associates unallocated facts with every related holder. It supports influence analysis but may overcount totals.
- **Type 4 mini-dimension:** A separate dimension for correlated, rapidly changing attributes. Its key joins to the fact and avoids repeated type 2 rows in a large base dimension.
- **Supertype fact table:** A cross-product fact table containing only measures that make sense for virtually every product type.
- **Subtype schema:** A line-of-business fact and dimension design containing special facts and attributes for one product type while retaining supertype facts and attributes.

## Mental Models

- **If the model has two dimensions, question the model.** A low dimension count often means natural business dimensions remain embedded in a large dimension.
- **Put volatile relationships at the fact grain.** A changing account-to-household relationship belongs in the snapshot fact rather than in a huge type 2 account dimension.
- **Share keys, not incompatible facts.** Common facts belong in the supertype, while disjoint product facts belong in subtype schemas with shared surrogate keys.
- **Separate routine bands from analytic precision.** Use banded mini-dimension values for consistent reports, and retain discrete values as facts when data mining or expert analysis needs them.

## Anti-patterns

- **Too few dimensions:** Embedding household, branch, product, and status in the account dimension hides natural entry points, harms usability, and increases type 2 row growth.
- **Customer as an account attribute:** This loses additional holders and violates account dimension granularity.
- **Customer as a fact-table foreign key:** This changes the one-row-per-account-per-month grain when several holders exist.
- **Physically multiplying fact rows by bridge weights:** This enlarges the fact table, becomes worse with multiple multivalued dimensions, and removes easy access to unallocated values.
- **One mini-dimension per attribute:** This creates too many fact-table keys. Group correlated attributes into clumps.
- **All product facts in one table:** This creates a wide table with many nulls, like “Swiss cheese,” and weakens both cross-product and line-of-business analysis.
- **Type 2 tracking for volatile monster dimensions:** Monthly demographic changes can make account, customer, or bridge tables unmanageable.

## Worked Example

A bank declares the grain as one account per month and records the primary month-ending balance. John and Mary share a checking account, so the account-to-customer bridge stores two rows with customer surrogate keys and weights of 0.50 each. A customer report that applies weights assigns half of the balance and fees to each holder, preserving the account total. An impact report omits weights when the question asks which customer profiles touch the account portfolio, and users accept the resulting overlap. The snapshot fact also stores household, product, branch, status, and mini-dimension keys. A shared supertype row supports portfolio analysis, while a checking subtype row stores overdraft and transaction details.

## Key Takeaways

- Declare the fact grain before choosing dimensions, measures, or relationship techniques.
- Use dimension triage when the design contains only a few dimensions.
- Keep account, household, and customer relationships explicit when their cardinality or volatility differs.
- Use bridge weighting for allocated totals and label unweighted analysis as an impact report.
- Use multiple mini-dimensions for correlated, rapidly changing attribute groups.
- Use dynamic value banding when report ranges must change at query time.
- Pair supertype portfolio facts with subtype schemas for heterogeneous product detail.

## Connects To

- **Chapter 3: Retail Sales:** causal dimensions, junk dimensions, and generic product hierarchies support dimension triage.
- **Chapter 4: Inventory:** periodic snapshots, nonadditive balances, multiple dates, and value banding provide related patterns.
- **Chapter 5: Procurement:** account status illustrates a mini-dimension-like status design.
- **Chapter 6: Order Management:** audit, degenerate, role-playing, and junk dimensions extend triage options.
- **Chapter 7: Accounting:** time-stamped bridge relationships support time-variant account associations.
- **Chapter 8: Customer Relationship Management:** rapidly changing customer attributes motivate mini-dimensions.
