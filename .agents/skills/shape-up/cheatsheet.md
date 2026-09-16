# Cheatsheet

## Raw Idea to Bet

| If you see | Do | Because |
|---|---|---|
| A new request | Say “Interesting. Maybe some day.” | A first contact is not a commitment. |
| A broad feature label | Find the specific failing use case. | A narrow problem creates a test of fitness. |
| A solution larger than the time | Set appetite and vary scope. | Fixed time forces useful trade-offs. |
| A promising concept | Walk it slowly, patch holes, and write a pitch. | Unresolved risk creates a fat tail. |

**Flow**: raw idea → appetite → narrow problem → elements → rabbit holes and no-gos → pitch → one-cycle bet.

## Appetite Defaults

| Size | Team | Time |
|---|---|---|
| **Small Batch** | One designer and one or two programmers | One or two weeks |
| **Big Batch** | Same team | One full six-week cycle |

## Shape Readiness
A concept is ready to pitch only when it is:
- **Rough**: Later builders have room for judgment.
- **Solved**: The macro elements connect and visible rabbit holes have answers.
- **Bounded**: The appetite and out-of-bounds cases are clear.

## Betting Rules
- Bet one cycle at a time.
- Give the bet a meaningful payout.
- Protect the team from interruption.
- Stop by default when the project misses the cycle.
- Re-shape before asking for another bet.
- Use cool-down for recovery, bugs, experiments, and the next betting table.

## Product Mode

| Product state | Mode | Expect |
|---|---|---|
| Core idea and architecture unknown | **R&D mode** | Senior team spikes. Learn, do not promise a customer ship. |
| Core architecture settled | **Production mode** | Shape deliberately. Merge finished work into the main codebase. |
| Launch is near | **Cleanup mode** | Drop normal shaping. Fix must-haves, merge small bites, make the final cut. |

## Build Order
Choose the first piece that is:
1. **Core** to the project's value.
2. **Small** enough to finish in a few days.
3. **Novel** enough to remove uncertainty.

Then integrate affordances, code, and real data. Build only enough back-end support for the next step.

## Scope and Hill Tells
- Use scopes, not designer or programmer lists.
- Redraw a scope when “done” is unclear, its name is generic, or it is too large.
- Keep **Chowder** at three to five items or fewer.
- Prefix nice-to-haves with `~`.
- Move the scariest unknowns uphill first.
- Treat a motionless Hill Chart dot as a raised hand.
- Split a scope when its parts move independently.

## Stop and Ship
Ask:
- Is this a must-have?
- Can customers use the feature without it?
- Is it a new problem or a baseline problem?
- How often does it occur, and who sees it?
- What is the real impact?

Compare down to the customer baseline, not up to perfection. Consider an extension only when surviving must-haves are all downhill and no unknown remains.

## After Release
Let the storm pass. Keep a clean slate. Shape feedback before the next bet.
