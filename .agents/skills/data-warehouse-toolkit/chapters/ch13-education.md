# Chapter 13: Education

## Core Idea

Educational institutions contain many analytic processes, but two dimensional-modeling techniques receive primary attention. Use an **accumulating snapshot fact table** when a short-lived workflow has a defined beginning, end, and standard milestones. Use a **factless fact table** when the important information is an event or a coverage relationship, and no measured fact exists. These techniques support applicant pipelines, research proposals, admission events, course registrations, facility utilization, and student attendance.

## Frameworks Introduced

- **Accumulating Snapshot Fact Table** — Use it for a workflow or pipeline with standard milestones, such as applicant admissions or research grant proposals. Store one row for each workflow instance, place a date foreign key for each milestone, and revisit the row whenever the instance changes. Update milestone keys, status values, counts, and elapsed measures as the instance progresses.
- **Factless Fact Table** — Use it to record an event or a relationship among dimensions without variable measurements. Set the grain at the event level, then store the participating dimension keys. Count rows to analyze the event.
- **Coverage Factless Fact Table** — Use it when the institution must represent possible use, whether or not use occurs. Insert one row for each facility, standard hourly block, day of week, and term. Store a utilization status so analysts can compare available and utilized capacity.
- **Artificial Count Metric** — Use a count column that always equals 1 when clearer SQL, aggregate rollups, or OLAP cube counts need an explicit measure. The column adds no business information, but `SUM` expresses the row count directly.
- **Type 4 Mini-Dimension** — Use it when groups across the university need to track changes in selected student attributes, such as declared major, class level, or graduation attainment. Place the tracked attributes in a separate mini-dimension.
- **Slowly Changing Dimension Type 7** — Use it when reports must preserve the student profile at registration time and also filter by current student characteristics. Store both a surrogate student key for the type 2 history and a durable student identifier for the current-row view.
- **Bridge Table** — Use it when a course registration has multiple instructors. Associate an instructor group key with individual instructor keys. Add weighting factors only when the teaching workload allocation is clearly defined.

## Key Concepts

- **Grain**: The precise level represented by one fact row. Applicant pipeline grain is one row per prospective student. Course registration grain is one row per registered course, student, and term.
- **Milestone**: A standard stage in a workflow, such as initial inquiry, campus visit, application submitted, file completed, admission notification, or enrollment or withdrawal.
- **Role-Playing Dimension**: One date dimension used through several roles. Each applicant milestone date uses a date view or role and a surrogate key, including an unknown-date key for new or in-process rows.
- **Factless Fact Table**: A fact table with dimension foreign keys but no variable measurement facts. The keys identify a business event or relationship.
- **Event Fact**: A row that records a participating set of dimensions, such as a student registration or admission-event attendance. Row counts provide the main analysis.
- **Coverage Fact**: A row that represents a possible state across a complete set of dimensions, including periods when utilization does not occur.
- **Conformed Term Dimension**: A term dimension that conforms to the calendar date dimension. Shared attributes, such as term and academic year, must use identical labels and values.
- **Explicit Non-Event Row**: A row added for an event that did not occur. In attendance, a registered student can receive an attendance metric of 0, while attendance receives 1.
- **Durable Identifier**: A stable student identifier that links facts to the current student row, while a surrogate key links to historical type 2 rows.

## Mental Models

- Use an accumulating snapshot to answer, “Where is each pipeline instance now, and how long did it take to reach each milestone?”
- Use a factless event table to answer, “Which dimensions participated, and how many such relationships occurred?”
- Use a coverage table when absence itself must be measured against every possible facility and time combination.
- Preserve event grain before solving multi-valued dimensions. A convenient instructor join can create overstated registration counts.

## Anti-patterns

- Do not use an accumulating snapshot as the only history for calendar cutoffs. Row updates show current status but do not preserve applicant counts at critical dates. Complement it with transaction facts, periodic snapshots, or retained cutoff snapshots.
- Do not add rows for every event that did not happen in a sparse relational star schema. The method becomes unreasonable for promoted products that customers did not purchase. Add zero rows only when the non-event has the same dimensionality, remains small, and supports a clear analysis, as with course no-shows.
- Do not change course-registration grain to one row per instructor, course, student, and term merely to handle co-teaching. This unnatural grain can overstate registration counts.
- Do not assume `COUNT(DISTINCT key)` and `COUNT(key)` answer the same question. Count a key for row volume, and use `COUNT DISTINCT` for unique key instances.
- Do not treat an artificial count metric as a business measurement. Its value of 1 supports readable queries, summaries, and cubes, but it carries no additional information.

## Worked Example

Model the applicant pipeline at one row per prospective student. Store foreign keys for inquiry, campus visit, application submission, file completion, admission notification, and enrollment or withdrawal dates. Treat each date as a role-playing use of the date dimension, and use the unknown surrogate key for milestones that have not occurred. Add the applicant key, application status key, and application ID. Store counts for inquiry, visits, submissions, completions, decisions, and enrollments. Analysts can group the current pipeline by high school, credentials, geography, intended major, or application source, then compare milestone dates to find delays. If admissions staff must compare early-decision totals at the notification date, retain cutoff snapshots or add an admission transaction fact because later row updates erase that historical state.

## Key Takeaways

- Define the workflow grain before selecting an accumulating snapshot.
- Give every standard milestone its own role-playing date key.
- Revisit accumulating rows as workflow status changes.
- Use factless facts for events and coverage, then count rows or an artificial count metric.
- Conform term attributes with the calendar date dimension.
- Protect registration counts when courses have multiple instructors.
- Add explicit zero attendance rows only when their dimensionality matches attendance rows and the volume stays reasonable.

## Connects To

- **Chapter 3: Retail Sales** — Introduces factless fact tables through promotion events.
- **Chapter 4: Inventory** — Uses accumulating snapshots for product movement pipelines.
- **Chapter 5: Procurement** — Describes Type 4 mini-dimensions and the slowly changing dimension Type 7 pattern.
- **Chapter 6: Order Management** — Applies accumulating snapshots to order fulfillment workflows.
- **Chapter 8: Customer Relationship Management** — Introduces bridge tables and supplies the customer and alumni relationship comparison.
- **Chapter 10: Financial Services** — Discusses bridge weighting and its possible overstatement.
