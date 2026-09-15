# Chapter 5: Risks and Rabbit Holes

## Core Idea
Before a bet, remove the problems that could multiply the appetite. A well-shaped project has a thin-tailed risk profile, with familiar parts and few large unknowns.

## Frameworks Introduced
- **Thin-tailed probability distribution**: A shaped project may run slightly long, but it has no visible path to taking several times the appetite.
  - When to use: Use this as the readiness test before a pitch.
  - How: Remove technical unknowns, unsolved design problems, and misunderstood interdependencies.
- **Slow-motion use-case walk-through**: Play the proposed flow step by step to expose gaps.
  - When to use: Use it after broad exploration finds a promising concept.
  - How: Ask what happens at every transition, then question the viability of each element.
- **Patch a hole**: Choose a deliberate compromise when a complex case would threaten the cycle.
  - When to use: Use it when a hard edge case is important enough to address but not worth a new design exploration.
  - How: Keep the core value and choose the simplest behavior that removes the risk.
- **Declare out of bounds**: Explicitly exclude valid-looking use cases that do not fit the project.
  - When to use: Use it when a behavior could spread across many parts of the product.
  - How: Name the supported case and mark the other cases outside the project.
- **Present to technical experts**: Review the concept with a small trusted group before wider presentation.
  - When to use: Use it when a technical assumption, data assumption, or code dependency remains uncertain.
  - How: Ask, “Is X possible in six weeks?” rather than “Is X possible?” Keep the clay wet and invite simplification.

## Key Concepts
- **Rabbit hole**: A technical, design, or dependency problem with an open-ended cost.
- **Fat tail**: A long risk tail caused by an unresolved problem that can multiply the original appetite.
- **Patch**: A bounded compromise that removes a dangerous unknown.
- **Out of bounds**: A case that the project intentionally does not support.
- **De-risked**: Shaped so the remaining unknowns should not stop shipping within the appetite.

## Mental Models
- Think of each unresolved rabbit hole as a time bomb inside the bet.
- Use a **patch** to protect the project, not to claim the compromise is the ideal design.
- Treat technical review as a search for risk, not a request for general approval.

## Anti-patterns
- **Push the knot to the team**: A team cannot fairly solve a tangled design problem inside a short fixed window.
- **Support every use case**: Broad coverage turns a narrow win into an unbounded project.
- **Ask “Is it possible?”**: Everything may be possible, but the appetite still limits what is useful.
- **Freeze the artifact too early**: A polished document discourages revisions that could remove risk.

## Worked Example
The To-Do Groups concept used dividers for loose and grouped items. A review found no answer for completed items. Rather than redesign completed-item rendering inside every group, the shaped concept kept the old completed-item section and appended the group name to each completed item. This was a little messy, but it preserved the core incomplete-item groups and removed a large design and performance risk. The pitch called out the patch so the team would not reopen it.

## Key Takeaways
1. Walk the use case slowly after the fast exploration stage.
2. Hunt for technical assumptions, design gaps, and interdependencies.
3. Patch risky edges and state the trade-off.
4. Mark tempting but unsupported cases out of bounds.
5. Ask experts about the appetite, not abstract possibility.

## Connects To
- **Ch 4: Find the Elements**: Supplies the rough concept that needs stress-testing.
- **Ch 6: Write the Pitch**: Records rabbit holes and no-gos for the bet.
- **Ch 8: The Betting Table**: Uses the circuit breaker when shaping missed a risk.
