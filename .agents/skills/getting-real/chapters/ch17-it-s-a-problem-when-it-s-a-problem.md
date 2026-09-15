# Chapter 17: It's a Problem When It's a Problem

## Core Idea
Do not spend time solving problems that do not exist yet. Make decisions just in time, when a real problem and useful information appear. This keeps the product simple and leaves attention for urgent work.

## Frameworks Introduced
- **It is a problem when it is a problem — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use this rule for scale, staffing, hardware, billing, and other future concerns.
  - **When to use**: Use it when a team wants to build for a hypothetical user count, hire for future work, or buy capacity before demand exists.
  - **How**: Name the current problem. If it does not affect current users or work, defer it. Revisit the choice when real information makes the decision necessary.
- **Just-in-time decisions — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use present evidence instead of forecasts.
  - **When to use**: Use it when the team lacks the data needed for a complex solution.
  - **How**: Choose the smallest workable action, learn from actual use, and increase hardware or system software only as necessary.
- **Just Wing It — Basecamp team**: Use a simple temporary approach when a non-urgent gap has a known time window.
  - **When to use**: Use it when launch can proceed safely and the team has time to solve the gap after launch.
  - **How**: Launch without unnecessary bells and whistles, use the available window, and tell customers about growing pains when they occur.

## Key Concepts
- **Current problem**: A problem that affects present work or users.
- **Hypothetical problem**: A feared condition without current evidence.
- **Just-in-time decision**: A decision made when real information can improve it.
- **Overbuilding**: Adding capacity or complexity before a need exists.
- **Growing pains**: Short-term problems caused by increased use or change.
- **Simple solution**: The smallest approach that solves the actual need.
- **Decision window**: Time available before a deferred problem becomes urgent.
- **Candor**: Honest communication about a problem and its effect.

## Mental Models
- **Evidence before architecture**: Wait for real use to show the shape of the problem.
- **Delay preserves options**: A later decision can use better information and avoid needless complexity.
- **Problem as a trigger**: Let a real failure or need start the next investment.
- **Honesty as a buffer**: Clear communication gives customers context while the team repairs a growing pain.

## Anti-patterns
- **Solving for 100,000 users today**: The team spends energy on a scale that may never arrive.
- **Hiring eight programmers for three current needs**: Extra staff expands cost and coordination before demand proves itself.
- **Buying twelve servers early**: Unused capacity ties up money and hides the simplest workable setup.
- **Adding future bells and whistles**: Speculation makes the current product harder to build and change.
- **Hiding slowdowns**: Customers lose trust when the team avoids a clear explanation.

## Worked Example
Basecamp launched without the ability to bill customers. The team knew monthly billing created a 30-day gap, so it used that time for more urgent work. After launch, it solved billing with a simple approach rather than adding unnecessary features. The launch exposed a real need and supplied the information needed to address it.

## Key Takeaways
1. Name the current problem before designing a solution.
2. Defer hypothetical scale, staffing, and capacity work.
3. Use the smallest workable approach during a safe decision window.
4. Revisit decisions when real use supplies better information.
5. Tell customers about growing pains instead of hiding them.

## Connects To
- **Chapter 7, Fix Time and Budget, Flex Scope**: Defers nonessential scope when present limits need attention.
- **Chapter 11, Lower Your Cost of Change**: Favors simple choices that remain easy to change.
- **Chapter 19, Scale Later**: Applies the same rule to server capacity and system growth.
- **Chapter 29, Race to Running Software**: Launch creates the evidence needed for later decisions.
