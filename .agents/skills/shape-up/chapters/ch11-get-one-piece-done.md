# Chapter 11: Get One Piece Done

## Core Idea
Integrate one meaningful vertical slice early instead of finishing separate horizontal layers. A working, demoable piece exposes design and implementation problems before the cycle is almost over.

## Frameworks Introduced
- **Integrate one slice**: Combine design, front-end, and back-end work on one small piece.
  - When to use: Use it during the first week and repeat it through the project.
  - How: Choose a core interaction, wire enough code to click through it, and refine it with real data.
- **Affordances before pixel-perfect screens**: Give programmers the endpoints and basic behavior before visual polish.
  - When to use: Use it when the team needs to test whether the interaction makes sense.
  - How: Start with inputs, buttons, places, copy, and working routes. Add typography, color, and spacing later.
- **Program just enough for the next step**: Build only the scaffolding that lets the team test the next design or behavior.
  - When to use: Use it while the product is still being discovered.
  - How: Use mock data, partial models, temporary routes, or simple authentication when those choices do not block learning.
- **Start in the middle**: Choose the first piece by three criteria: **core**, **small**, and **novel**.
  - When to use: Use it when the project has many possible starting points.
  - How: Prefer the central interaction, make it finishable in a few days, and choose the part that teaches something new.

## Key Concepts
- **Vertical slice**: An end-to-end piece that a person can use and evaluate.
- **Affordance**: The input, button, place, or copy that forms the core interaction.
- **Scaffolding**: Temporary or partial code that enables the next design decision.
- **Core**: Central to the value of the project.
- **Novel**: Unfamiliar enough to reduce important uncertainty when built early.

## Mental Models
- Think of the first slice as a **proof of reality**, not a miniature final product.
- Use **roughness** to make wrong choices cheap.
- Prefer learning from a working interaction over confidence from a long task list.

## Anti-patterns
- **Horizontal layers**: Separate design and back-end work create many completed tasks but no working feature.
- **Pixel-perfect first pass**: It spends time on styling before the team answers whether the idea works.
- **Login-first construction**: It delays the central problem with peripheral setup work.
- **Full back-end first**: It builds more than the designer needs to test the next step.

## Worked Example
In Clients in Projects, the team chose the visibility toggle as its first slice. The designer tested radio buttons, a checkbox, and a custom button in HTML. The programmer wired the toggle across supported content types, saved its state, and made it clickable on staging data. The toggle did not yet change client visibility, but the team could judge the core interaction after about three days. They then settled it and returned to the access model and later design work.

## Key Takeaways
1. Build a working slice during the first week.
2. Let designers and programmers take turns on the same piece.
3. Use affordances and basic wiring before visual polish.
4. Build only enough back-end support for the next learning step.
5. Start with work that is core, small, and novel.

## Connects To
- **Ch 4: Find the Elements**: Defines affordances before polished screens.
- **Ch 10: Hand Over Responsibility**: Lets the team choose tasks and sequence.
- **Ch 12: Map the Scopes**: Turns integrated slices into scopes.
