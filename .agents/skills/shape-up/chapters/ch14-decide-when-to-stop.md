# Chapter 14: Decide When to Stop

## Core Idea
Ship a strong improvement against the current baseline instead of chasing an ideal. Fixed time and variable scope give teams the authority to hammer away work that does not deserve the remaining time.

## Frameworks Introduced
- **Compare to baseline**: Judge the work against what customers use today, not against a perfect design.
  - When to use: Use it when the team feels work is never good enough.
  - How: Ask whether the result works better than the current workaround and whether customers can feel the improvement.
- **Scope grows like grass**: New details and improvements appear naturally as the team enters the work.
  - When to use: Expect it in every project.
  - How: Give the team authority and responsibility to cut scope continuously.
- **Scope hammering**: Forcefully question each new task so the project fits the fixed time box.
  - When to use: Use it throughout the cycle.
  - How: Ask whether the task is a must-have, whether the project can ship without it, whether it is new or pre-existing, how often it occurs, who sees it, and its real impact.
- **Must-haves and nice-to-haves**: A scope is done when must-haves are complete. Mark optional work with `~` and cut it first.
  - When to use: Use this distinction whenever new work appears.
- **QA is for the edges**: Designers and programmers own basic quality. QA hunts edge cases late in the cycle.
  - When to use: Use QA as a level-up, not as a release gate.
  - How: Treat QA findings as nice-to-haves by default, then elevate severe issues to the affected scope.
- **Rare extension**: Extend a project only when true must-haves survived every cut and all remaining work is downhill.
  - When to use: Use it only when no unknown or open question remains.
  - How: Prefer cool-down slack or a new bet over a habit of extension.

## Key Concepts
- **Baseline**: The current customer solution used for comparison.
- **Scope hammering**: Repeated decisions that remove nonessential work.
- **Must-have**: Work required for the scope to count as done.
- **Nice-to-have**: Optional work marked with `~` and cut when time is short.
- **Edge case**: A less common condition outside the core flow.

## Mental Models
- Think of quality as **selective excellence**, not equal polish everywhere.
- Use the **baseline** to replace “perfect” with “meaningfully better.”
- Treat the deadline as a **decision tool**, not only a pressure source.

## Anti-patterns
- **Ideal comparison**: It creates endless refinement without a shipping decision.
- **Scope-creep blame**: Scope grows from hidden detail in the work, not only from bad people.
- **Automatic extension**: It removes the circuit breaker and hides shaping errors.
- **QA gate**: It makes the team depend on a final checkpoint for basic quality.
- **Extending uphill work**: Unknowns are too risky for an extension.

## Worked Example
A team discovers a new edge case during QA. It records the issue on a separate QA list. The team checks severity and time. If it is a true must-have, the team moves it into the relevant scope, so that scope remains unfinished until the issue is fixed. If it is optional, the issue stays marked as a nice-to-have and is cut when the cycle ends. An extension remains possible only after all must-haves survive hammering and the remaining work is downhill.

## Key Takeaways
1. Compare the result with the customer's baseline.
2. Expect scope to grow, then cut it with authority.
3. Mark optional work with `~` as soon as it appears.
4. Let the team own core quality and use QA for edges.
5. Extend only rare, downhill, must-have work.

## Connects To
- **Ch 8: The Betting Table**: Supplies the circuit breaker.
- **Ch 12: Map the Scopes**: Uses `~` and scope boundaries.
- **Ch 15: Move On**: Prevents shipped work from creating immediate debt.
