# Chapter 9: Human Resources Management

## Core Idea

Human resources data needs models that preserve employee profile history while keeping business events in process-specific fact tables. Start with an employee dimension, a headcount periodic snapshot, and a bus matrix.

## Frameworks Introduced

- **Employee dimension with type 2 slowly changing dimension tracking**
  - **When to use:** Use it when the business must analyze an employee’s complete profile at an exact historical point in time.
  - **How:** Store one row per profile state with a surrogate employee key, durable natural employee ID, effective and expiration date/time, current row indicator, and change reason. Expire the old row just before the new row becomes effective. Insert a new row when an employee returns to an earlier profile.

- **Change reason tracking**
  - **When to use:** Use it when analysts need to identify why type 2 employee dimension rows changed.
  - **How:** Add a change reason attribute for changed attributes, such as `Last Name` or `ZIP`. Use delimited text for simple searches, or a multivalued bridge table for relational treatment. Group source micro-transactions into a super transaction, such as a promotion.

- **Employee headcount periodic snapshot**
  - **When to use:** Use it for regular status, count, payment, and balance reporting across employees and organizations.
  - **How:** Create one row per employee per month with month, employee, and organization dimensions. Use the employee row effective at month end. Store counts and monthly metrics in the fact table. Add facts across dimensions, but average balances across the month dimension.

- **HR bus matrix**
  - **When to use:** Use it to map HR business processes, fact types, and shared dimensions before extending the model.
  - **How:** List processes such as hiring, benefits, performance review, separation, and compensation. Mark dimensions and fact type for each process. Use transaction, periodic snapshot, or accumulating snapshot facts as needed. Include factless facts for benefit eligibility or participation.

- **Recursive employee hierarchy bridge**
  - **When to use:** Use it when users must drill through a variable-depth management chain in a relational environment.
  - **How:** Create one bridge row for each manager and employee directly or indirectly in that manager’s chain, plus a self-row. Store levels from top and top or bottom flags. Use durable natural keys with effective and expiration dates when relationship history matters. Restrict this structure to a canned BI application or power BI users.

- **Skill keyword bridge and skill keyword text string**
  - **When to use:** Use these techniques for an open-ended, variable number of employee skills.
  - **How:** A skill keyword bridge groups employees with the same skill set and links each group to a skills dimension. AND searches across skill rows need UNION and INTERSECTION logic. A delimited string, such as `|Unix|C++|`, supports standard SQL AND and OR searches, but not counts by skill.

- **Survey questionnaire fact**
  - **When to use:** Use it when HR analyzes survey responses by question, respondent, reviewed employee, survey, and response category.
  - **How:** Store one row per question on a respondent’s survey. Use role-playing employee dimensions for responding and reviewed employees, and role-playing date dimensions for sent and received dates. Add survey, question, and response category dimensions.

- **Text comments outside the fact table**
  - **When to use:** Use this design when the business requires freeform comments that do not fit numeric fact or discrete dimension values.
  - **How:** First determine whether text can become dimension attributes. Use a comments dimension when comments repeat and have lower cardinality than transactions. Use a transaction-grained dimension attribute for unique comments. Keep text away from the fact table.

## Key Concepts

- **Factless fact table:** A fact table with dimensional keys and no numeric metrics, useful for counting events.
- **Durable natural employee ID:** The operational employee identifier that persists across type 2 profile rows and remains a dimension attribute.
- **Surrogate employee key:** The dimension primary key that identifies one employee profile state and links facts to the profile effective at the event time.
- **Precise effective and expiration timespan:** The interval in which a type 2 employee row accurately describes an employee. Date/time stamps support multiple states on one day.
- **Super transaction:** A business action that encapsulates source micro-transactions, such as promotion changes.
- **Periodic snapshot:** A fact table that records status at regular intervals, such as one employee per reporting month.
- **Semi-additive balance:** A balance that adds across non-time dimensions but requires averaging across the month dimension.
- **Role-playing dimension:** A dimension used for different roles, such as employee and manager, or responding and reviewed employee.
- **Outrigger:** A dimension linked from another dimension, such as a manager role-play linked from the employee dimension.
- **Conformed dimension:** A shared dimension used across bus matrix processes for consistent analysis.

## Mental Models

- Use the employee dimension for profile state, but use a separate fact table when an event needs its own dimensions.
- Treat type 2 history as a choice about the business question, not as a default for every employee attribute.
- Choose manager-key history only after deciding whether manager profile changes or only reporting-relationship changes matter.
- Select a skill bridge for relational skill analysis, or a delimited string for simpler AND and OR searches without skill counts.

## Anti-patterns

- **One profile-transaction fact row for every type 2 employee row:** Avoid this redundant design because both tables have nearly identical row counts and almost always join. Embellish the employee dimension when no numeric metrics exist.
- **Using the employee dimension for every HR event:** Avoid putting reviews, benefits, development, and separations into one dimension. Separate facts preserve each process’s dimensions.
- **Overloading the employee dimension with event outriggers:** Avoid foreign keys for reviewers, benefits, separation reasons, and event details. The result becomes difficult to navigate.
- **Cascading manager profile changes through the organization:** Avoid making a manager’s type 2 key change force a new employee row for every subordinate unless the business explicitly needs that history.
- **Storing freeform comments in the fact table:** Avoid treating comments as degenerate dimensions. Text adds bulk to queries that otherwise need only performance metrics.
- **Buying a packaged model without testing conformance:** Avoid vendor terminology and isolated data when the model cannot use business vocabulary or conform dimensions.

## Worked Example

Suppose Abby manages Hayden. Hayden’s employee dimension row stores a manager key that points to Abby’s role-playing manager dimension row. If Hayden changes managers and the business needs reporting history, make the manager foreign key a type 2 attribute and insert a new Hayden row. If Abby only changes her home address, do not let that unrelated Abby profile row create new rows for every subordinate. Use a durable natural manager key for current-manager reporting, or make the manager key type 1 when current association matters and history does not. For a variable-depth chain, use a management hierarchy bridge with self, direct, and indirect relationships, while accepting its larger row count and more difficult BI navigation.

## Key Takeaways

- Define the employee profile grain before selecting type 2 attributes or separate HR facts.
- Use precise date/time intervals and a current row indicator for point-in-time profile analysis.
- Record change reasons and consolidate source micro-transactions into meaningful super transactions.
- Build a monthly headcount periodic snapshot for additive metrics and carefully treat balances.
- Use the HR bus matrix to identify process-specific facts and conformed dimensions.
- Match hierarchy and skill techniques to history, query, and usability requirements.
- Keep freeform comments outside the fact table.

## Connects To

- **Chapter 5: Procurement:** Type 2 slowly changing dimension techniques and effective or expiration handling provide the employee profile history pattern.
- **Chapter 7: Accounting and finance:** The chapter uses bus matrix thinking and discusses recursive hierarchies, including alternatives such as a pathstring attribute.
- **Chapter 14: Healthcare:** The chapter notes that multivalued bridge tables can also join directly to fact tables.
- **Dimensional modeling fundamentals:** Grain, fact table, dimension, conformed dimension, surrogate key, role-playing dimension, outrigger, bridge, and periodic snapshot choices govern the HR designs.
