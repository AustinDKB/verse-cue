# Chapter 15: Electronic Commerce

## Core Idea

Treat clickstream as a dimensional business process, not as raw log data dumped into a warehouse. Resolve visitor origin, session boundaries, and identity as carefully as the source permits, then model the stream at more than one grain. Integrate the result through conformed dimensions and extend the sales transaction process when you need a defensible profit-and-loss view across web, store, and telesales channels.

## Frameworks Introduced

- **Clickstream Session Fact Table** — Use when you need a manageable first model for complete visitor sessions. Set the grain to one row for each completed customer session. Use calendar date, time, customer, entry page, session, and referrer dimensions. Store session seconds, pages visited, orders placed, order quantity, and order dollar amount. Record both universal synchronized date/time and local wall-clock date/time through two role-playing calendar date views. Use a persistent cookie as the preferred session-tracking method. Use time-contiguous host records only with a robust postprocessor that marks uncertain results.

- **Clickstream Page Event Fact Table** — Use when analysts need page behavior, event sequence, product context, promotion context, and abandonment detail. Set the grain to one row for each individual page event, while discarding graphical micro-events unless that atomicity has business value. Add page, event, session, session ID, three role-playing step dimensions, product, referrer, and promotion. Keep the large fact table at its useful grain instead of aggregating away dimensions.

- **Step Dimension technique** — Use for any sequential process. Attach the Step Dimension in multiple roles, such as overall session, purchase subsession, and abandonment subsession. Filter purchase step number to 1 to find starting pages for successful purchases. Filter abandonment steps to zero steps remaining to find the final pages in unsuccessful purchase sessions.

- **Aggregate Clickstream Fact Tables** — Use when recurring reports scan large session or page-event facts. Group by the required rollup dimensions, such as month, demographic type, entry page, and session outcome. Count sessions and sum additive facts. Build the aggregate from conformed shrinking dimensions, such as month from calendar day and demographic type from customer.

- **Enterprise Data Warehouse bus matrix integration** — Use the bus matrix to place Web Visitor Clickstream beside related business processes and identify shared dimensions. A matrix column also acts as an invitation list for the teams that must conform a dimension.

- **Profitability Fact and profit-and-loss structure** — Use when the enterprise needs channel, customer, product, promotion, or time profitability with an explanation of why. Set the grain to each individual line item sold on a sales ticket. Allocate activity and infrastructure costs to that grain, then calculate gross revenue, net revenue, gross profit, and net profit.

## Key Concepts

- **Clickstream**: A collection of web-server page events, often joined with data from partners, ISPs, and search specifications.
- **Page dimension**: A dimension at the grain of an interesting distinguishable page type, not every dynamic page instance.
- **Event dimension**: A small dimension that describes what happened on a page, such as Open Page, Refresh Page, Click Link, or Enter Data.
- **Session dimension**: A dimension that classifies a complete session by local context, overall context, action sequence, success status, and customer status.
- **Referral dimension**: A dimension that describes how a visitor reached the current page, including site, domain, search type, specification, and target.
- **Session ID**: A unique identifier that groups page events for one session and acts as a degenerate dimension in the page-event fact.
- **Session seconds**: Total seconds assigned to a complete session, including a small nominal final interval when the exit cannot be observed.
- **Page seconds**: Seconds from one page event until the next page event. This measure must not be confused with session seconds.
- **Conformed shrinking dimension**: A rollup dimension derived from a more detailed dimension for an aggregate fact table.
- **External data warehouse**: The chapter’s description of Google Analytics, which receives tracking data and supplies dimensions, measures, dashboards, and reports.

## Mental Models

- Use **grain before scale**. Choose a session-grained fact first when raw page and micro-event volume threatens load and query control.
- Treat **universal time and local time as separate roles**. Store synchronized instants for cross-system comparison and local wall-clock values for visitor context.
- Think of **special clickstream dimensions as bridges**, not exceptions. Page, event, session, and referral dimensions add web context while conformed customer, product, media, promotion, and date dimensions connect web behavior to other processes.
- Treat **profitability as allocated evidence**. A P&L row contains fractions of sourced or estimated costs, so improve source quality and business rules over time.

## Anti-patterns

- **Dump raw logs without context**: Stateless page events cannot reliably show sessions, origins, or identities.
- **Create a page row for every dynamic instance**: The page dimension becomes astronomically large without adding useful distinctions. Group dynamic pages by function and type.
- **Assume a cookie identifies a person**: A cookie identifies a browser or computer. Shared devices and multiple devices make person-level identity uncertain.
- **Use product-oriented causal dimensions at session grain**: A session can involve several products, so the causal factor becomes multivalued. Put product-oriented causation at finer page-event grain.
- **Call both measures “seconds”**: Analysts may add non-equivalent measures. Name session seconds and page seconds separately.
- **Build web profitability on sessions**: Cost allocation becomes controversial when a session has no product involvement or immediate sale. Extend the sales transaction fact instead.
- **Claim precise costs from weak sources**: National averages and annual ratios create pro forma allocations. Publish the best available values and identify improved rules as sources mature.

## Worked Example

A web retailer records 100 million page fetches and estimates 20 million completed sessions. It first creates one Clickstream Session Fact row per session. The row stores the entry page, referrer, session classification, customer, orders, order dollars, and session seconds. It stores the session start once in UTC and once in the visitor’s local wall-clock role. This keeps the first load manageable while supporting both cross-server timing and local behavior analysis.

The retailer then creates a Clickstream Page Event Fact at page-event grain. Each row stores the page, event, session ID, product, promotion, page seconds, and three Step Dimension roles. For a successful purchase, purchase step 1 identifies the starting page. For an abandoned purchase, abandonment step zero identifies the last page. The retailer places clickstream beside Product Orders, Customer Communications, and Service Policy Orders in the bus matrix. Shared conformed dimensions let analysts compare web behavior with later purchases and service demand.

For profitability, the retailer extends the sales transaction process. Each line item receives gross revenue, allowances, promotions, markdowns, net revenue, manufacturing or acquisition cost, storage cost, freight cost, special deal cost, overhead, gross profit, and net profit. Website system cost may allocate by product pages, pages visited, or web purchases. The chosen allocation remains a business rule, not a directly observed fact.

## Key Takeaways

- Define the grain explicitly before loading clickstream data.
- Prefer persistent cookies, but label identity and session results as uncertain when evidence is weak.
- Model complete sessions and page events as complementary fact tables.
- Use role-playing calendar dates for universal and local time.
- Use Step Dimension roles to analyze successful and abandoned sequences.
- Build aggregates with conformed shrinking dimensions.
- Measure web profitability by extending the sales transaction process and exposing cost quality.

## Connects To

- **Chapter 8: Customer Relationship Management** — Supplies the Step Dimension technique for sequential session analysis.
- **Enterprise Data Warehouse bus architecture** — Provides conformed dimensions and the bus matrix for integrating clickstream with retail processes.
- **Dimensional modeling** — Applies grain, fact table, dimension, degenerate dimension, role-playing dimension, and slowly changing dimension decisions to web data.
- **Sales transaction process** — Supplies the common grain and dimensions for profitability across web, store, and telesales channels.
