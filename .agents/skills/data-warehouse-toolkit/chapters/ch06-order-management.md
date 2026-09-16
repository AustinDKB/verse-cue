# Chapter 6: Order Management

## Core Idea
Order management contains linked business processes for ordering, shipping, invoicing, payment, and returns. Model each process at its natural grain, share conformed dimensions, and add an accumulating snapshot when users need the current state and velocity of one order through a finite fulfillment pipeline.

## Frameworks Introduced
- **Order Management Bus Matrix**: Use it to map quoting, ordering, shipping, invoicing, payments, and returns to shared dimensions. Mark dimensions such as Date, Customer, Product, Sales Rep, Deal, Warehouse, and Shipper. Record roles such as Order Date and Requested Ship Date.
- **Fact Normalization**: Use it only when facts are numerous, sparsely populated per row, and not computed with one another. Replace measures with one amount and a measurement-type key. Resist it for ordinary order facts because it multiplies rows and complicates ratios.
- **Dimension Role Playing**: Use this technique when one fact table references one dimension several times. Store each foreign key, then present each role through a separately labeled view or alias of one physical dimension. Give role attributes unique names.
- **Junk Dimensions**: Use it to group low-cardinality flags and indicators that do not deserve separate dimensions or bulky fact-row text. Place one surrogate key in the fact table. Use separate dimensions when the Cartesian product becomes too large.
- **Allocating**: Use it to move a header-level fact, such as shipping charges, to line-item grain. Obtain an enterprise rule and label alternative methods separately when needed.
- **Accumulating Snapshot Fact Table**: Use it for a short-lived process with a clear beginning and end. Insert one row at the process grain, then update it as milestones occur.

## Key Concepts
- **Order transaction fact table**: One row per order line item, with quantity and extended gross, discount, and net amounts.
- **Natural grain**: The business event represented by one fact row. Orders and invoices use line-item grain.
- **Conformed dimension**: A shared dimension that permits drill-across analysis between order and invoice facts.
- **Role-playing dimension**: One physical dimension that appears through several logical roles in one fact table.
- **Degenerate dimension**: An operational identifier stored in a fact table without a joined dimension, such as Order Number.
- **Factless fact table**: A table that records an event or relationship without numeric facts. Sales rep-customer assignments use effective and expiration date keys.
- **Audit dimension**: A dimension that exposes fact-row processing context, including quality, adjustment, allocation-version, and currency-version attributes.
- **Service Level Dimension**: A qualitative shipment-performance classification that complements numeric counters and lag facts.
- **Accumulating snapshot fact table**: A revisable table that updates dates, quantities, and lags as a pipeline item advances.

## Mental Models
- **Model the event, not the operational record**: Keep order-line grain in the fact table and distribute descriptive header information into analytic dimensions.
- **Use allocation before splitting grain**: If a header fact must support product analysis, allocate it to lines. Otherwise, create separate fact tables rather than mixing granularities.
- **Treat conversion factors as row context**: Store currency or unit-of-measure conversion factors with the facts they convert, then expose converted measures through views.
- **Separate process views from pipeline views**: Transaction facts explain what moved through each stage. An accumulating snapshot explains where each item is now and how long it took to reach milestones.

## Anti-patterns
- **Normalize ordinary facts into one amount per row**: This multiplies rows and complicates arithmetic between gross, discount, and net values.
- **Create a transaction header dimension**: It replicates the operational header, grows with every order, and weakens dimensional analysis.
- **Join a header fact to a line fact for inherited context**: Users must join large tables whenever they slice line facts by header attributes.
- **Repeat an unallocated header fact on every line**: Summation overstates the amount. Storing it on one line hides it under filters.
- **Mix header and line grains in one fact table**: Allocate higher-level facts or create separate fact tables.
- **Use a special product key to hide header facts**: This makes the model illegible and forces a decoder rule.

## Worked Example
A build-to-order company records one order-line fact row with Order Date, Requested Ship Date, Product, Customer, Sales Rep, Deal, Order Number, and Order Line Number. The row stores quantity, extended gross, discount, and net amounts. Order Number and Order Line Number remain degenerate dimensions.

The order has a shipping charge. The team allocates it to lines using an agreed rule, such as extended gross amount. Users can then analyze the charge by Product, Customer, or Deal without double counting. If finance and logistics use different rules, store two clearly labeled allocated facts. If allocation fails, use a separate order-header fact table.

For fulfillment, create one accumulating snapshot row at line-item grain. Use Unknown or To Be Determined for unavailable dates. Update the row through backlog, manufacturing release, finished inventory, shipment, arrival, and invoicing. Calculate milestone lags to expose current status and bottlenecks.

## Key Takeaways
- Define order and invoice facts at one row per line item.
- Reuse physical dimensions through separately labeled role-playing views.
- Keep transaction identifiers as degenerate dimensions when no descriptive dimension exists.
- Allocate header facts to line grain before offering product-level analysis.
- Use junk dimensions for manageable sets of low-cardinality indicators.
- Store local and standard currency facts together, and store conversion factors with the fact row.
- Use an accumulating snapshot for short-lived fulfillment pipelines that need milestone updates and lag analysis.

## Connects To
- **Chapter 3: Retail Sales**: Promotion and date role-playing examples support Deal dimensions and role-playing dates.
- **Chapter 4: Inventory**: Shrunken conformed dimensions and the bus matrix provide related documentation patterns.
- **Chapter 5: Procurement**: Surrogate keys, slowly changing dimension type 2, and SCD type 5 inform dimension handling.
- **Chapter 7: Accounting**: Customer organizational hierarchies extend the customer discussion.
- **Chapter 14 and Chapter 19**: Measurement Type dimensions and ETL status tables support normalization and audit-dimension decisions.
