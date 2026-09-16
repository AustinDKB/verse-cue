# Chapter 26: Human Solutions

## Core Idea
Build software for general concepts, not for every convention that people might use. Give people enough structure to solve their own problems, then leave room for their judgment and creativity.

## Frameworks Introduced
- **Human solutions — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Let users create local solutions inside a general framework.
  - **When to use**: Use it when many customers may solve the same root problem in different ways.
  - **How**: Identify the root problem, provide a clean general tool, and omit specialized controls that apply only to some cases. Let people add their own conventions in the content they already control.
- **General framework over forced convention — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Preserve flexibility by refusing to encode every possible workflow.
  - **When to use**: Use it when a proposed field, assignment rule, date system, or category system would make every user handle a concern they may not have.
  - **How**: Add a dedicated feature only when the root problem needs it for most users. Otherwise, let users represent the detail in a simple, visible form.
- **Enough, then get out of the way — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Stop product work at the useful boundary.
  - **When to use**: Use it after the core problem has a clear and usable solution.
  - **How**: Avoid adding conventions that dictate how customers must work. Watch the solutions that people create and change the general framework only when a broad need appears.

## Key Concepts
- **General concept**: A root problem that applies across many user situations.
- **Human solution**: A user-created method inside the product's general framework.
- **General framework**: A small set of tools that supports many local workflows.
- **Forced convention**: A product rule that requires one way to represent a problem.
- **Local convention**: A practice a user creates for a particular need.
- **Clean tool**: An uncluttered interface with only broad, useful structure.
- **Specialized control**: A field or action that serves a narrow case.
- **Product boundary**: The point where the software solves the root problem and stops.

## Mental Models
- **Blank space as capability**: Omitted controls give users room to adapt the tool.
- **Root problem first**: Solve the common need before encoding uncommon details.
- **Users as convention makers**: Treat customers as capable partners who can create useful notation.
- **General tool, local method**: Keep the product broad and let each user make the workflow specific.

## Anti-patterns
- **Convention enforcement**: Force every user to adopt a field or workflow that only some need.
- **Case-by-case software**: Add a control for each request until the general tool becomes crowded.
- **Premature specialization**: Encode dates, categories, or assignments before the root problem requires them.
- **User underestimation**: Assume people cannot create simple solutions without dedicated features.
- **Overbuilt flexibility**: Add many options instead of leaving usable space for human judgment.

## Worked Example
Ta-da List intentionally omitted assignment, due-date, and category features. A user who wanted a date could write `(due: April 7, 2006)` at the front of a to-do item. A user who wanted a category could write `[Books]` at the front. These methods were not as formal as dedicated fields, but they kept the tool clean and remained flexible for cases the designers could not predict. The product solved list-making, then let people create the rest.

## Key Takeaways
1. Solve the root problem before adding specialized controls.
2. Give users a general framework that supports local methods.
3. Omit conventions that do not apply to most cases.
4. Watch user-created solutions before changing the product.
5. Stop when the core problem has a clean, useful answer.

## Connects To
- **Chapter 20, Make Opinionated Software**: Combines a clear product stance with room for user methods.
- **Chapter 21, Half, Not Half-Assed**: Supports a narrow product with enough depth at its core.
- **Chapter 32, Avoid Preferences**: Avoids shifting every small product decision to the customer.
