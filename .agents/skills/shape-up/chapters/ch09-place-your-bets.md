# Chapter 9: Place Your Bets

## Core Idea
Bet according to where the product is in its development. Existing products use the standard Shape Up process. New products move through R&D mode, production mode, and cleanup mode, one cycle at a time.

## Frameworks Introduced
- **Existing products**: Shape, bet, build, and ship a version of the work to customers within one cycle.
  - When to use: Use the standard process when the existing code and design provide a stable context.
- **R&D mode**: Senior people spike core ideas and architecture when the product is still a theory.
  - When to use: Use it when the team cannot reliably shape the desired result in advance.
  - How: Bet time on key pieces, keep senior designers and programmers on the team, and aim to learn rather than ship.
- **Production mode**: Use formal shaping, betting, and building after the core architecture settles.
  - When to use: Use it when new contributors can see where features belong.
  - How: Shape a result for the cycle, use multiple teams when possible, and treat “shipping” as merging into the main codebase.
- **Cleanup mode**: Use unstructured capacity before launch to fix omissions, bugs, and details.
  - When to use: Use it after R&D and production work, near the launch.
  - How: Drop normal shaping and team boundaries, merge small changes continuously, and make final-cut decisions. Keep cleanup to two cycles or less.
- **Betting questions**: Ask whether the problem matters, appetite is right, solution is attractive, timing is right, and the right people are available.
  - When to use: Use these questions at the table without doing extended design work there.

## Key Concepts
- **Spike**: Experimental work used to learn whether an idea or architecture can work.
- **Load-bearing structure**: Core code and UI decisions that define future possibilities.
- **Final cut**: The decision about which features remain in the launch product.
- **Production mode**: A new product phase with settled core architecture and formal cycles.
- **Cleanup mode**: A final, flexible phase for launch readiness.

## Mental Models
- Think of development modes as **confidence stages**, not permanent departments.
- Use a one-cycle bet to learn even when the larger product may need many cycles.
- Judge a solution's interface real estate as a scarce resource, not a free add-on.

## Anti-patterns
- **Long-term commitment to a new product**: It assumes future cycles before the current cycle teaches you anything.
- **R&D judged by shipping**: It hides the purpose of learning and architecture discovery.
- **Cleanup without discipline**: It turns launch anxiety into endless additions.
- **Betting-table design session**: It moves the meeting into weeds instead of choosing among shaped options.

## Worked Example
HEY spent about one year in R&D mode with Jason, David, and Jonas exploring the core. It then used almost a year of production-mode cycles with Basecamp teams, followed by two cleanup cycles. Each bet stood alone. The table did not promise two years of work. A different example, Hill Charts, used one cycle to test an experimental feature and a second bet only after the first cycle created confidence.

## Key Takeaways
1. Match expectations to product maturity.
2. In R&D mode, bet on learning and architecture, not a customer release.
3. In production mode, return to formal shaping and shipping.
4. In cleanup mode, cut the final surface area and keep the period short.
5. Ask the five betting questions without redesigning the pitch at the table.

## Connects To
- **Ch 8: The Betting Table**: Defines the one-cycle commitment.
- **Ch 10: Hand Over Responsibility**: Hands a production-mode project to a team.
- **Ch 13: Show Progress**: Uses Hill Charts for work with known and unknown parts.
