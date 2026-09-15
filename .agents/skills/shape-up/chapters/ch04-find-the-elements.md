# Chapter 4: Find the Elements

## Core Idea
Move from a problem in words to a concrete solution without falling into wireframe detail. Breadboarding and fat marker sketches expose the flow and preserve room for later design.

## Frameworks Introduced
- **Breadboarding**: A low-fidelity interface map that uses words and connections instead of visual styling.
  - When to use: Use it when the key question is how the flow works and where the feature fits.
  - How: Draw **Places**, **Affordances**, and **Connection lines**. Play the use case from start to finish.
- **Places**: Screens, dialogs, or menus that a user can navigate to.
- **Affordances**: Buttons, fields, and interface copy that a user can act on or read for information.
- **Connection lines**: Links that show how affordances take the user from place to place.
- **Fat marker sketch**: A broad, low-fidelity sketch for a visual concept where two-dimensional arrangement matters.
  - When to use: Use it when topology alone misses the central visual problem.
  - How: Use a thick marker or large pen so detail is difficult to add.
- **Elements are the output**: End shaping with a short, narrow list of concrete solution elements, not a finished design.

## Key Concepts
- **Topology**: What connects to what, without deciding whether the result is a screen or modal.
- **Level of detail**: The amount of specificity that enables progress without locking later choices.
- **Affordance**: A visible action or information cue that supports the next user action.
- **Room for designers**: The space left for later visual and interaction decisions.
- **Private shaping**: Early work that may be dropped before a commitment.

## Mental Models
- Use a **breadboard** as an electrical prototype. Include components and wiring, but not industrial design.
- Use a **fat marker** to make premature detail physically difficult.
- Think of the shaped concept as the **boundaries and rules of a game**, not a specification.

## Anti-patterns
- **Wireframe-first shaping**: Layout detail slows exploration and biases later designers.
- **Polished early artifact**: A polished screen looks like a deliverable and hides open questions.
- **Conveyor belt shaping**: Treating every shaped idea as committed work removes the option to stop.
- **Detached layers**: Designing full screens or building full back-end layers before integrating a slice creates late surprises.

## Worked Example
For an Autopay feature, the team first mapped an invoice place and a “Turn on Autopay” affordance. The flow raised key questions: Does setup happen on a separate screen or a modal? Does enabling Autopay pay the current invoice? Can the customer use ACH? How does the customer turn Autopay off? The team moved the option into the payment flow to remove the current-invoice ambiguity. It avoided a new username and password flow by putting “disable Autopay” on the invoicer’s existing customer-detail page. The resulting elements were concrete, but the later visual design stayed open.

## Key Takeaways
1. Choose the right people or work alone with no room for slow discussion.
2. Use Places, Affordances, and Connection lines for interaction flows.
3. Use fat marker sketches when arrangement is the problem.
4. End with a narrow list of solution elements.
5. Stop before the artifact becomes a deliverable or a commitment.

## Connects To
- **Ch 2: Principles of Shaping**: Applies roughness and the right level of abstraction.
- **Ch 5: Risks and Rabbit Holes**: Stress-tests the elements before a bet.
- **Ch 11: Get One Piece Done**: Uses affordances as the first working interface.
