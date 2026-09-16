# Chapter 12: Transportation

## Core Idea
Model a voyage by choosing a fact-table grain that matches the business process and its metrics. Transportation cases often need several fact tables at different granularities, while role-playing dimensions, correlated dimensions, and localized date and time dimensions keep analysis usable.

## Frameworks Introduced
- **Airline bus matrix**: Use it to scope the first deliverable and show which dimensions apply to each business process. Start with the process rows, add dimensional columns, and include degenerate dimensions such as confirmation, ticket, or case numbers. For the initial airline project, prioritize flight activity and defer reservation and ticketing activity that does not produce a boarding.
- **Multiple fact table granularities**: Use this when one voyage supports operational, revenue, and customer-demand questions. Identify leg, segment, trip, and itinerary grains, then assign only metrics valid at each grain. Start at segment grain when it is the lowest level with meaningful revenue metrics, and add leg or trip facts when their users or performance needs justify them.
- **Role-playing technique**: Use separate logical roles when one physical dimension supplies different meanings, such as scheduled departure, actual departure, origin airport, and destination airport. Create views on one underlying date, time, or airport dimension and place the role-specific foreign keys in the fact table.
- **Combining correlated dimensions**: Use this exception when dimension row counts are extremely small or when combined roles produce necessary attributes. Form the Cartesian product of tightly correlated attributes, store the relationship in one dimension, and avoid this pattern for large dimensions without a clear usability gain.
- **Country-specific date dimensions**: Use these when a multinational system needs holidays, seasons, or calendar names that vary by country. Keep generic calendar attributes in the primary date dimension, then key a supplemental dimension by primary date key and country code. Join it as an outrigger or directly to the fact table.
- **Local and equivalized date/time**: Use both views when users need local time-of-day analysis and cross-business simultaneity. Store separate local and standard date and time-of-day foreign keys. Do not treat a UTC offset alone as sufficient because the offset depends on location and date.

## Key Concepts
- **Leg**: One aircraft departure and arrival between adjacent airports without an intermediate stop.
- **Segment**: One flight number flown by one aircraft, composed of one or more legs and represented by a ticket-coupon line item.
- **Trip**: A customer journey between requested origin and destination, which may contain multiple segments and aircraft changes.
- **Itinerary**: The complete airline ticket or reservation, identified by its confirmation context.
- **Segment-level flight activity fact**: A fact table with one row for each passenger boarding pass at segment grain.
- **Passenger profile mini-dimension**: A type 4 mini-dimension containing unique combinations of changing profile attributes, such as elite tier, home airport, club status, and lifetime mileage tier.
- **Aggregate fact table**: A complementary table at a higher grain, such as trip, with rolled-up facts and measures that exist only at that grain.
- **Degenerate dimension**: A business identifier stored in the fact table without a separate dimension row, such as a confirmation, ticket, or bill-of-lading number.
- **Country-specific calendar outrigger**: A supplemental date structure keyed by date and country, carrying local holiday, season, and calendar attributes.

## Mental Models
- Use the lowest grain that preserves the metrics users need. Do not force leg-level allocation when segment-level revenue already answers the first business question.
- Treat a stopover as a business rule, not a reporting guess. The airline derives trip origin and destination during extraction when a ticket contains a stop longer than four hours.
- Keep roles separate by default. Combine them only when small row counts or role-dependent attributes create a clear benefit.
- Store both relative and absolute time. Local time explains daily behavior, while standard time shows simultaneous activity across locations.

## Anti-patterns
- **Mixing grains in one fact table**: This makes measures ambiguous and encourages invalid aggregation. Keep leg, segment, trip, and itinerary facts distinct when their metrics differ.
- **Deriving trip endpoints in every report**: Sequencing segments at the BI layer hides the real trip and creates repeated, difficult processing. Derive stopovers during extraction and add trip roles.
- **Combining role-playing dimensions by default**: Large combined dimensions duplicate attributes and reduce clarity. Use separate logical views unless the exception criteria apply.
- **Using only a UTC offset**: An offset cannot resolve daylight-saving changes or location-and-date dependence. Provide local and equivalized date and time-of-day keys.
- **Using a bridge for origin and destination**: When the existing fact row already contains both airport roles, a bridge adds needless complexity. Store route attributes in a city-pair route dimension or a deliberately combined dimension.

## Worked Example
An airline wants marketing reports about where frequent flyers travel, the fare they pay, upgrades, and earned miles. Operations also wants leg-level delays and capacity, but the first release cannot solve every question.

The team selects segment grain because passenger revenue and mileage credit apply to the ticket-coupon segment. It loads one fact row per boarding pass and links scheduled and actual departure dates and times, passenger and passenger profile, origin and destination airports, aircraft, flown class, fare basis, and booking channel. It stores confirmation number, ticket number, segment sequence number, flight number, revenue components, charges, miles flown, and miles earned.

A San Francisco to Minneapolis journey through Denver illustrates the distinction. If one aircraft and flight number serve both legs, the journey is one segment with two legs. If the passenger changes aircraft in Denver, the journey contains two segments but remains one trip. During extraction, the team marks a stop longer than four hours as a stopover and assigns trip origin and destination airport roles to each segment row. It adds a trip aggregate fact only if repeated segment rollups cause a clear performance or usability problem.

## Key Takeaways
- Choose grain before selecting facts, and state the grain in one precise sentence.
- Separate leg, segment, trip, and itinerary processes when their metrics or users differ.
- Reuse physical dimensions through role-playing views and conforming keys.
- Use a type 4 mini-dimension for large passenger dimensions with changing profile combinations.
- Derive trip roles during extraction when a business stopover rule exists.
- Add aggregate facts only for demonstrated performance or usability problems.
- Design country-specific calendars and both local and equivalized times for multinational analysis.

## Connects To
- **Chapter 3: Retail Sales**: Supplies the time-of-day dimension and time-period groupings used in transportation activity.
- **Chapter 5: Procurement**: Introduces the mini-dimension pattern reused for passenger profiles.
- **Chapter 6: Order Management**: Establishes role-playing dimensions and discusses multi-currency reporting.
- **Chapter 7: Accounting**: Relates country calendars to multiple fiscal accounting calendars.
- **Chapter 8: Customer Relationship Management**: Connects localization to multi-language support.
- **Conformed dimensions**: Let later leg, reservation, ticket, shipping, hotel, and rental facts reuse dimensions built for the first release.
