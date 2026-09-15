# Chapter 21: Big Data Analytics

## Core Idea

Big data changes the data asset mission, not only the data volume. It includes structured, semistructured, unstructured, and raw data in many formats, often with analysis needs beyond conventional SQL. A DW/BI system must combine flexible big data processing with dimensional integration, durable identity, governance, and fit-for-purpose latency.

## Frameworks Introduced

- **Extended RDBMS Architecture:** Use when relational semantics, indexed lookups, transaction processing, and in-database analytics matter. Extend relational types for complex structures, unstructured text, images, video, and name-value pairs. Execute specially crafted user-defined functions (UDFs) inside the DBMS inner loop, and use a first pass as a fact extractor before a second relational pass.
- **MapReduce/Hadoop Architecture:** Use when data does not require structure at load time, full data scans dominate, or analysis needs complex iteration and branching. Store data in HDFS or another distributed store, then execute general UDF-like MapReduce processing across distributed nodes. Use Hadoop as a flexible environment for ETL and later load useful structure into an RDBMS when needed.
- **Data Highway:** Use when one enterprise needs several latency and quality levels. Plan caches from **Raw Source** through **Real Time**, **Business Activity**, **Top Line**, and **DW and Long Time Series**. Materialize only the caches that the environment needs, and permit multiple paths between them.
- **Fact Extractor from Big Data:** Use when raw or unstructured data contains useful measures that downstream users can trend. Analyze the source, produce relational facts or indicators, and move those results to the next cache.
- **Build From Sandbox Results:** Use when data scientists need freedom to test languages and environments. Permit sandbox prototypes, prove business value, then reimplement the logic in scalable, available, secure technologies that IT can support.
- **Data virtualization:** Use for rapid schema prototyping or schema alteration. Define alternative logical structures over physical data, accept run-time computation during exploration, and materialize tested virtual schemas when performance becomes important.
- **Streaming data analytics:** Use when analysis must begin before an incoming load finishes. Apply SQL-like continuous queries and moving time windows, and stop processing when a threshold exceeds the required limit.

## Key Concepts

- **Big data:** Structured, semistructured, unstructured, and raw data in varied formats that creates a paradigm shift in collection, analysis, and value creation.
- **User-defined function (UDF):** A reusable analytic function that can contain arbitrarily complex processing and run within a database or distributed processing request.
- **Extended RDBMS:** A relational database extended with complex data types and UDF processing for big data use cases.
- **MapReduce:** A distributed processing framework that applies general mapping and reduction logic across many machines.
- **Data highway cache:** A distinct physical data store at a defined latency and data-quality level.
- **Fact extractor:** Big data processing that converts raw observations into numerical, trendable measures or other usable facts.
- **Conformed dimension:** A shared enterprise dimension attribute that allows analysis across separate data sources, even when local dimensions differ.
- **Durable surrogate key:** A unique, simple warehouse identifier with no changeable business meaning. It anchors a major entity across sources and caches.
- **Name-value pair:** A flexible representation that loads an unexpected attribute without requiring a fixed structure at load time.
- **Data virtualization:** A logical data structure defined over physical data, which exchanges run-time computation for prebuilt ETL tables.

## Mental Models

- **Choose architecture by workload:** Prefer an Extended RDBMS for relational semantics and indexed lookups. Prefer MapReduce/Hadoop for massive scans, flexible structure, and complex branching.
- **Treat latency as a quality trade-off:** Immediate data can remain dirty because short intervals limit cleansing and relationship checks. Expect better quality in slower caches with more complete source data.
- **Dimensionalize before integration:** Attach customer, product, location, time, and other dimensions to atomic observations early. Then conformed dimensions and durable surrogate keys make cross-source joins possible.
- **Assume technology change:** Plan to reprogram and rehost big data applications within about two years. Favor portable, metadata-driven approaches instead of a new legacy foundation.

## Anti-patterns

- **Treating big data as only a larger RDBMS:** This fails when data formats, UDF needs, distributed processing, or load rates exceed relational assumptions.
- **Building a new legacy environment:** Rapid changes in data types, hardware, programming methods, and providers make a fixed long-term platform risky.
- **Keeping prototypes separate from production practice:** Sandbox results become unusable when no IT process exists to reimplement, secure, scale, and operate them.
- **Waiting to add value:** Delaying filtering, cleansing, pruning, conforming, matching, joining, or diagnosis increases transfer cost and reduces downstream usefulness.
- **Using source natural keys across caches:** Natural keys conflict across applications and can change under external administration. Use durable surrogate keys instead.
- **Ignoring governance during exploration:** Big data prototypes still create privacy, security, compliance, quality, metadata, and master-data risks.
- **Storing sensitive data without masking or encryption:** Hadoop does not manage updates well. Protect sensitive data on write or mask it on read.
- **Running big data workloads beside warehouse workloads without resource separation:** Changing analytic demands can consume resources needed for conventional DW/BI service levels.

## Worked Example

A stream of customer tweets enters the **Raw Source** cache. Even a short tweet such as “Wow! That is awesome!” receives inferred dimensions such as customer, product, location, provider, cohort group, triggering event, and outcome. A **Fact Extractor from Big Data** produces measures such as share of voice, audience engagement, conversation reach, sentiment ratio, satisfaction score, topic trends, and resolution time. The measures enter a **Real Time** or **Business Activity** cache for current monitoring, then a **Top Line** cache for daily review and the warehouse for historical analysis. At each transfer, ETL replaces source-specific identifiers with durable surrogate keys and applies conformed dimensions. The design accepts lower data quality in the immediate cache, then adds cleansing, matching, and business-rule diagnosis in slower stages.

## Key Takeaways

- Select Extended RDBMS or MapReduce/Hadoop from workload needs, not from platform fashion.
- Plan the Data Highway and materialize only the latency caches that users need.
- Use big data as a Fact Extractor when raw observations can become trendable facts.
- Build from sandbox results, but prepare to reprogram and rehost prototypes.
- Add value early, and replace proprietary keys with durable surrogate keys at every cache boundary.
- Think dimensionally, use conformed dimensions, and preserve slowly changing dimensions (SCDs).
- Declare structure at analysis time when the source is variable, and use name-value pairs for unexpected content.
- Apply enterprise governance, with privacy protection as the highest-risk concern for identifying data.

## Connects To

- **Chapter 5, Procurement:** Supplies slowly changing dimensions (SCDs) for tracking time variance in big data dimensions.
- **Chapter 8, Customer Relationship Management:** Shows conformed enterprise attributes and incremental integration across varied customer sources.
- **Chapter 19, ETL Subsystems and Techniques:** Provides filtering, cleansing, conforming, matching, key replacement, and other ETL operations along the Data Highway.
- **Dimensional modeling:** Supplies grain, fact table, dimension, conformed dimension, and surrogate key practices that integrate structured and unstructured data.
