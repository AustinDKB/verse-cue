# Chapter 14: Healthcare

## Core Idea
Healthcare dimensional design must integrate clinical, financial, and operational events while preserving their distinct grains. Start with conformed dimensions and explicit business-process grains, then apply specialized patterns for claims workflows, multivalued diagnoses, sparse measurements, text, images, and asset utilization.

## Frameworks Introduced
- **Healthcare bus matrix**: Use when a healthcare organization must link patient encounter, clinical, billing, and operational processes. Map each process to its grain and mark its shared dimensions, including Date, Patient, Physician, Diagnosis, Payer, Employee, Facility, and Procedure. Use the matrix to expose integration points between administrative and clinical information.
- **Accumulating snapshot fact table**: Use for the claims billing and payment workflow, a short-lived process whose line items move through known milestones. Define one row per medical claim line, create it when charges arrive and bills are generated, and revisit the row as billing and payment events occur. Store milestone date foreign keys, workflow amounts, and lag measures. Add companion transaction schemas for unusual payment relationships.
- **Role-playing dimension**: Use when one fact row contains several dates or business roles from one dimension. Create separate views over the single Date dimension for the eight claim dates, with clear role labels. Apply the same approach to payer roles and physician roles such as admitting, attending, referring, consulting, or assisting.
- **Multivalued dimension with bridge table**: Use when an event has an open-ended set of diagnoses or participants. Replace the fact table’s diagnosis foreign key with a diagnosis group key, then connect the group to individual diagnoses through a Diagnosis Group Bridge. Use a group dimension only when a modeling tool needs conventional primary-key relationships.
- **Measurement type dimension**: Use for extremely sparse, heterogeneous measurements such as laboratory results. Set the grain to one row per measurement per event. Put the unit of measure and additivity restrictions in the measurement type dimension, and add new measurement types as rows rather than altering the fact table.
- **Supertype and subtype for charges**: Use when inpatient facility charges and outpatient professional charges share core billing behavior but need specialized roles or attributes. Keep common claim structure in the supertype and add subtype-specific dimensions and physician roles where the hospital process requires them.
- **Inventory utilization grains**: Choose a periodic snapshot for recurring bed or facility status, a transaction fact for movements, or a timespan fact table when states change infrequently. Match the representation to volatility and the required utilization question.

## Key Concepts
- **Conformed dimension**: A shared dimension with consistent meaning across healthcare fact tables, with Patient as the most important example.
- **Transaction grain**: One row for each billing or claim payment transaction.
- **Accumulating snapshot grain**: One row for a claim line that accumulates its history from creation through the current state.
- **Role-playing date dimension**: Multiple labeled views of one Date dimension, each joined to a different date foreign key.
- **Diagnosis group key**: A key that represents a set of diagnoses associated with one fact event.
- **Diagnosis Group Bridge**: A table with one row for each diagnosis in a diagnosis group, supporting the many-to-many relationship.
- **Measurement type dimension**: A dimension that defines what a generic numeric fact means, including its unit and additivity restrictions.
- **To Be Determined date**: A reserved Date dimension row used when an accumulating snapshot date is not yet known.
- **Timespan fact table**: A fact table that records a state with row effective and expiration dates and times.

## Mental Models
- Use the accumulating snapshot for a standard workflow, not for a complete record of every exceptional payment event.
- Treat multivalued diagnoses as relationships, not as fixed role slots, because their count and meaning vary by event.
- Use measurement type rows while facts remain sparse. Return to fixed fact columns when density makes row counts excessive.
- Let the business question select the inventory grain: status over time, movement events, or state intervals.

## Anti-patterns
- **Periodic snapshot for short-lived claims**: It does not capture the behavior of a relatively short billing process as directly as an accumulating snapshot.
- **Multiple diagnosis foreign keys**: Fixed slots fail when diagnoses exceed the assumed maximum and force inefficient queries across unknown slots.
- **Unweighted diagnosis allocation**: Do not imply that each diagnosis owns a share of treatment or billing metrics without a realistic business rule. Impact analysis can overcount because the same metric links to multiple diagnoses.
- **Unique diagnosis groups for every encounter**: This can create astronomical row counts and duplicate identical groups. Reuse a portfolio of diagnosis groups through ETL lookup and creation.
- **Text in the fact table**: Freeform comments waste fact storage, add clutter, and rarely support quantitative queries. Store them in a comments dimension or transaction event dimension based on comment cardinality.
- **Dense use of the measurement type dimension**: One row per measurement per event can produce too many rows and complicate arithmetic across measurements. Use fixed columns when facts are no longer sparse.
- **Null future dates in accumulating snapshots**: Date foreign keys cannot remain null. Point unknown milestone dates to the reserved To Be Determined date row.

## Worked Example
A consortium models its claims billing and payment pipeline with an accumulating snapshot. The fact row represents one line on a medical claim and starts when a physician or facility charge arrives. It carries Patient, Physician, Procedure, Facility, Diagnosis, payer, responsible party, employer, and Master Bill ID dimensions.

The row also contains eight role-playing Date keys: treatment, primary billing, secondary billing, responsible-party billing, last primary payment, last secondary payment, last responsible-party payment, and zero balance. It stores billed, paid, collections, write-off, and unpaid amounts, plus payment and zero-balance lags. At first, future billing and payment dates point to To Be Determined. When each event occurs, ETL revisits the same row and updates the appropriate date keys and facts. Companion transaction facts preserve multiple payments for one line or one payment applied across several claims.

## Key Takeaways
- Define the fact row before selecting healthcare dimensions or measures.
- Build the bus matrix around shared Patient and other conformed dimensions.
- Use an accumulating snapshot for normal claim-line workflow milestones.
- Use role-playing views for multiple dates and repeated business roles.
- Model diagnoses and physician teams with bridge tables when membership is open-ended.
- Select measurement, text, image, and inventory patterns according to sparsity, cardinality, volatility, and query behavior.
- Treat late-arriving facts and retroactive dimension changes as common healthcare ETL conditions.

## Connects To
- **Chapter 4: Inventory**: Provides transaction and periodic snapshot grains for facility and equipment utilization.
- **Chapter 7: Accounting**: Relates date-effective bridge changes to historical change tracking.
- **Chapter 8: Customer Relationship Management**: Establishes the 360-degree view and timespan fact concepts.
- **Chapter 10: Financial Services**: Provides multivalued bridge weighting and supertype/subtype patterns.
- **Chapter 19: ETL Subsystems and Techniques**: Covers diagnosis-group bridge administration and late-arriving fact and dimension processing.
- **Chapter 21: Big Data Analytics**: Connects electronic medical records with unstructured data and growing data volumes.
