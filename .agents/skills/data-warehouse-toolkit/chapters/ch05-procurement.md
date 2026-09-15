# Chapter 5: Procurement

## Core Idea

Model procurement as business processes with explicit grain, metrics, dimensionality, and source-system boundaries. Then choose slowly changing dimension techniques per attribute, based on the history and reporting behavior that the business needs.

## Frameworks Introduced

- **Procurement bus matrix**: Use it when procurement contains requisitions, purchase orders, shipping notifications, receipts, invoices, and payments. Put one row per business process, record each row's atomic granularity and metrics, and mark applicable conformed dimensions. Use the matrix to expose shared dimensions and differences before selecting fact tables.
- **Blended versus separate transaction schemas**: Use a blended fact table when users view transactions as one process and the transactions share grain, dimensions, metrics, and source behavior. Use separate fact tables when users recognize distinct processes, source systems capture different granularities, or dimensions apply only to selected transactions. Compare user requirements, process identity, source systems, and dimensionality before deciding.
- **Procurement pipeline accumulating snapshot**: Use it when the business needs movement and duration across procurement milestones. Store milestone dates, quantities, amounts, control numbers, and lag facts in one row that progresses through the pipeline. Do not use it for a continuous flow without well-defined milestones.
- **Slowly changing dimension techniques**: Assign a change strategy to every dimension attribute. Use **Type 0: Retain Original** for immutable original values, **Type 1: Overwrite** for corrections or changes without historical value, **Type 2: Add New Row** for accurate history, and **Type 3: Add New Attribute** for simultaneous current and prior views. Use **Type 4: Add Mini-Dimension** for volatile attributes in a large dimension. Use **Type 5: Mini-Dimension and Type 1 Outrigger**, **Type 6: Add Type 1 Attributes to Type 2 Dimension**, and **Type 7: Dual Type 1 and Type 2 Dimensions** only when the business accepts their added complexity.

## Key Concepts

- **Procurement transaction fact**: A fact design with one row per procurement transaction, transaction dimensions, and transaction quantity and dollar amount facts.
- **Atomic grain**: The precise row meaning for a process, such as one row per purchase order line or one row per receipt line.
- **Degenerate dimension**: A business control number stored in the fact table without a separate dimension table, such as a purchase order number or payment check number.
- **Conformed dimension**: A shared dimension, such as date or product, reused across process-centric fact tables with consistent meaning.
- **Accumulating snapshot**: A fact table that follows a process through known milestones and records milestone dates, lag facts, and updated measures.
- **Slowly changing dimension**: A dimension whose descriptive attribute values change over time and require an explicit response strategy.
- **Surrogate key**: A single-column dimension key that identifies one profile version and links facts to that version.
- **Durable key**: A persistent key that identifies the same business entity across type 2 profile rows and remains a Type 0 attribute when durable.
- **Mini-dimension**: A smaller dimension that stores frequently changing or frequently analyzed attribute combinations, often as discrete bands.
- **Outrigger**: A dimension reference stored in another dimension, such as a current mini-dimension key stored in the primary customer dimension.

## Mental Models

- Treat the bus matrix as a design test. If one proposed fact table requires generic names such as “transaction date” or “employee,” distinct processes may need separate fact tables.
- Treat Type 2 as the safe default when the business has not settled an attribute's history rules. Type 2 preserves a later path to current-value reporting, but Type 1 cannot easily recover lost history.
- Treat every SCD attribute as a business governance decision. Data stewards define whether the organization needs original, current, historical, prior, or point-in-time values.
- Treat flexibility as a cost. Hybrid techniques can support several analytic views, but added columns, keys, joins, and labels can confuse users and increase administration.

## Anti-patterns

- **Blend distinct procurement processes by default**: A single table can hide source-system boundaries, force generic dimensions, and obscure unique control numbers or metrics.
- **Use Type 1 as the default history policy**: Overwrite changes can make old facts appear under today's hierarchy, alter prior report results, and require rebuilding affected aggregates or OLAP cube processing.
- **Put every changing attribute in the fact table**: This treats dimensions as static, creates repeated descriptive data, and does not provide a coherent dimension change strategy.
- **Use natural keys for Type 2 rows**: One natural key can represent several profile versions. Use a new surrogate key for each Type 2 row.
- **Use Type 3 for unpredictable changes**: A single prior value cannot represent useful history when different entities change at different times.
- **Expose hybrid paths without user controls**: Multiple current and historical routes can provide more choices than business users can apply safely.

## Worked Example

An electronics retailer moves IntelliKidz software from Education to Strategy on February 1, 2013. The modeler first chooses the attribute policy, then selects the dimension and fact behavior.

With **Type 1: Overwrite**, the existing product row keeps surrogate key 12345, and its department changes to Strategy. January sales of $500 and February sales of $100 both report under Strategy. This supports correction or current-only reporting, but it destroys the historical Education assignment and can invalidate existing department aggregates.

With **Type 2: Add New Row**, the original row keeps key 12345, Education, effective date 2012-01-01, and expiration date 2013-01-31. A new row uses key 25984, Strategy, effective date 2013-02-01, expiration date 9999-12-31, and a current-row indicator. January fact rows keep key 12345. February fact rows use key 25984. Reports return $500 for Education and $100 for Strategy, without changing historical facts.

If users need both the historically accurate department and the current department for every fact, the modeler can select **Type 6: Add Type 1 Attributes to Type 2 Dimension**. The historic department remains partitioned by Type 2 rows, while a current department attribute is overwritten across prior rows. The decision adds flexibility and complexity, so data stewards and users must approve it.

## Key Takeaways

- Define each procurement process at atomic grain before selecting dimensions or facts.
- Extend the bus matrix with granularity and metrics when transaction-table choices remain unclear.
- Separate fact tables when process identity, source systems, grain, or dimensionality differ.
- Add a procurement pipeline accumulating snapshot when milestone duration matters.
- Select an SCD technique per attribute with data governance representatives.
- Use surrogate keys, effective and expiration dates, and current-row indicators for Type 2 dimensions.

## Connects To

- **Chapter 3: Retail Sales**: Supplies the conformed date and product dimensions used in procurement.
- **Chapter 4: Inventory**: Contrasts one inventory process with procurement's potentially separate transaction processes and introduces accumulating snapshots.
- **Chapter 16: Insurance**: Extends the detailed implementation bus matrix with atomic granularity and metrics.
- **Chapter 19 and Chapter 20: ETL Subsystems and Techniques, and ETL System Design and Development Process and Tasks**: Apply surrogate-key workflows and Type 2 loading rules.
- **Chapter 10: Financial Services**: Extends mini-dimensions, multiple mini-dimensions, and dynamic value banding.
