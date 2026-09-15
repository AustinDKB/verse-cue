# Chapter 8: The Betting Table

## Core Idea
Use six-week cycles, two-week cool-down periods, and a short senior decision meeting to make one-cycle bets. A bet has a payout, a commitment, and a cap on the downside.

## Frameworks Introduced
- **Six-week cycle**: A cycle is long enough to finish meaningful work and short enough for the deadline to feel real from the start.
  - When to use: Use it as the default project and capacity unit.
  - How: Bet one cycle at a time and leave the team alone to finish.
- **Cool-down**: A two-week period after each cycle with no scheduled project work.
  - When to use: Use it to recover, fix bugs, explore ideas, and hold the betting table.
  - How: Let designers and programmers choose useful work under their control.
- **The betting table**: Stakeholders study pitches, capacity, business priorities, recent work, and available people, then produce a cycle plan.
  - When to use: Use it during cool-down.
  - How: Keep the meeting short, decide among the few pitches, select teams, and make the decision final.
- **Meaning of a bet**: A bet has a defined payout, uninterrupted commitment, and capped downside.
  - When to use: Use this definition before committing people.
  - How: State what meaningful result the pitch promises, protect the six weeks, and do not extend by default.
- **Circuit breaker**: A project that misses its cycle normally stops instead of receiving an extension.
  - When to use: Use it to prevent runaway projects and expose shaping errors.
  - How: Reframe the problem during the next shaping period, then present a new pitch if another bet is justified.
- **Bug strategies**: Use cool-down, bring a large bug to the betting table, or schedule an annual **bug smash**.
  - When to use: Use interruption only for a true crisis such as data loss or a major outage.

## Key Concepts
- **Big batch team**: A team that spends one cycle on one project.
- **Small batch team**: A team that ships several one- or two-week projects within one cycle.
- **Uninterrupted time**: The protected time promised by a bet.
- **Clean slate**: A new cycle with no scraps carried forward without a new bet.
- **Calendar Tetris**: The planning problem caused by people becoming available at different times.

## Mental Models
- Think of a bet as an investment with a known maximum loss.
- Treat interruptions as more costly than their hours because they destroy momentum.
- Use cool-down as both recovery time and the decision window for the next cycle.

## Anti-patterns
- **Interrupted bet**: “Just one day” breaks the six-week commitment and can kill a week of momentum.
- **Automatic extension**: It spends multiples of the appetite on a concept that needs rethinking.
- **Bug priority by label**: A bug is not automatically more important than every other problem.
- **Multi-cycle promise**: It removes the option to respond to what the next six weeks reveal.

## Worked Example
A team can use cool-down to fix ordinary bugs. If a slow back-end process needs a larger change, a programmer shapes a pitch and brings it to the betting table. Around the holidays, the company may schedule a whole cycle as a bug smash. A data-loss crisis can interrupt immediately, but an ordinary bug waits for one of these deliberate paths.

## Key Takeaways
1. Make the cycle long enough for meaningful work and short enough for real trade-offs.
2. Protect the team from interruption.
3. Define a payout before making the bet.
4. Stop an unfinished project by default and return it to shaping.
5. Keep only one cycle committed so future options stay open.

## Connects To
- **Ch 7: Bets, Not Backlogs**: Supplies the few pitches considered at the table.
- **Ch 9: Place Your Bets**: Matches the bet to the product's development mode.
- **Ch 14: Decide When to Stop**: Applies the circuit breaker and extension rules.
