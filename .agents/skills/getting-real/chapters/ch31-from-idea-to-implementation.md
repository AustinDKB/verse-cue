# Chapter 31: From Idea to Implementation

## Core Idea
Move from broad ideas to paper sketches, then to HTML and CSS, and only then to programming code. Each step makes the product more real while keeping early work cheap enough to discard and redo.

## Frameworks Introduced
- **From idea to implementation — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use a staged path that increases commitment only as understanding improves.
  - **When to use**: Use it when a product or feature needs a new flow, screen, or section.
  - **How**: Brainstorm the high-level product, sketch rough interfaces on paper, create HTML and CSS screens, and code the necessary behavior after the mock-up works and demonstrates enough functionality. Repeat the cycle when a step produces a poor result.
- **Big questions before pixel details — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Keep brainstorming at the right level.
  - **When to use**: Use it at the start of a product or feature, before interface polish has meaning.
  - **How**: Decide what the application must do, how usefulness will show, and what the team will make. Delay pixel-level discussion until the product idea has a form worth refining.
- **Paper-first experimentation — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use cheap sketches to explore many answers.
  - **When to use**: Use it before the team commits to a screen or flow.
  - **How**: Draw boxes, circles, and lines. Put concepts on paper, compare rough interface designs, and discard weak ideas without protecting the work.

## Key Concepts
- **Brainstorm**: High-level exploration of the product's purpose and behavior.
- **Foundation assumption**: A belief about the user need or product behavior that guides early work.
- **Paper sketch**: A quick, cheap interface experiment.
- **Rough interface**: An early visual arrangement that tests a concept, not final detail.
- **HTML screen**: A real browser-facing mock-up made before programming behavior.
- **CSS**: The screen styling used in the HTML mock-up stage.
- **Programming code**: The behavior added after the mock-up proves enough value.
- **Iteration**: Repetition of the stages when a deliverable does not work.

## Mental Models
- **Commitment ladder**: Increase cost from ideas to sketches to HTML to code.
- **Cheap-to-expensive filter**: Test weak ideas while change still costs little.
- **Interface before behavior**: Make the screen understandable before connecting its program logic.
- **Throwaway permission**: Discard any stage when it produces a poor result.

## Anti-patterns
- **Pixel-level brainstorming**: Debate small visual details before answering what the product must do.
- **Code-first exploration**: Spend programming effort before the interface and flow have a useful shape.
- **Sketch attachment**: Protect a paper idea because time has already gone into it.
- **All-at-once implementation**: Build the whole application before testing one real flow.
- **No-iteration process**: Treat each stage as a one-way handoff instead of repeating it.

## Worked Example
For Basecamp, the team began with broad needs: post project updates, let clients participate, represent milestones, centralize archives, and provide a bird's-eye view of projects. The team then sketched rough interfaces on paper. It created an HTML and CSS version of the “post a message” screen, followed by the “edit a message” screen. Only after the mock-up looked good and showed enough needed behavior did the team add programming code. A poor result at any stage could be discarded and rebuilt.

## Key Takeaways
1. Start with product questions, not pixel questions.
2. Use paper to explore interface concepts cheaply.
3. Build HTML and CSS before programming behavior.
4. Add code only after the mock-up demonstrates enough functionality.
5. Repeat or discard any stage when the result does not work.

## Connects To
- **Chapter 29, Race to Running Software**: Pushes the staged process toward a real working result.
- **Chapter 30, Rinse and Repeat**: Makes repeated passes an expected part of implementation.
- **Chapter 16, Ignore Details Early On**: Keeps early decisions at the level that the evidence supports.
