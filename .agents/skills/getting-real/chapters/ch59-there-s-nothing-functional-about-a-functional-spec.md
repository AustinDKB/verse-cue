# Chapter 59: There's Nothing Functional about a Functional Spec

## Core Idea
Do not write a functional specifications document before building. An application is not real until builders build, designers design, and people use it. A spec can describe fantasy, appease participants, hide different meanings, force early decisions, add features, and block later change.

## Frameworks Introduced
- **No Functional Spec — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Replace a locked blueprint with artifacts that the team can build, see, and change.
  - **When to use**: Use it before the team has learned from building and use.
  - **How**: Write a one-page story, sketch the interface, turn it into simple HTML, and start building before backend decisions become fixed.
- **One-Page Story — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Describe what the application needs to do in brief, plain language.
  - **When to use**: Use it when the team needs a shared starting point but lacks enough information for a detailed design.
  - **How**: Keep it to one page and finish it in one day. If it needs more space, simplify the problem or question its complexity.
- **Interface as Common Ground — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use screens, not paragraphs, to create shared understanding.
  - **When to use**: Use it before detailed backend work or when people interpret a written plan differently.
  - **How**: Draw paper screens, code them into HTML, and let everyone look at, use, and click through the customer experience.
- **Useless Specs — Linus Torvalds, creator of Linux, from *Linux: Linus On Specifications***: A spec cannot be both large enough to guide all work and accurate enough to match reality.
  - **When to use**: Use it when a team treats a document as a guarantee of software quality.
  - **How**: Prefer a working prototype that exposes behavior over software written to match theory.
- **Fight the Blockers — Mark Gallagher, corporate intranet developer, from *Signal vs. Noise***: Do not let extensive requirements documents delay design and learning.
  - **When to use**: Use it when people demand a long requirements phase before design or prototypes.
  - **How**: Start with a few concepts, make a static prototype, change it, and build a live prototype with real data.

## Key Concepts
- **Functional spec**: A blueprint that claims to describe an application before it exists.
- **Appeasement**: Requirements writing that makes people feel involved without making hard choices.
- **Illusion of agreement**: Shared text that hides different meanings in each reader’s mind.
- **Early decision**: A major choice made when the team has the least information.
- **Feature overload**: Excess functionality added because written bullets have no immediate cost.
- **One-page story**: A plain-language description of the needed application.
- **Paper sketch**: A quick screen drawing used to explore the interface.
- **Live prototype**: A working interface that uses real data and exposes behavior.

## Mental Models
- **Reality over theory**: Let building and use teach the team what the product needs.
- **Information-timing rule**: Make important decisions after the team gains information.
- **Prototype ladder**: Move from story to paper, HTML, and real data as understanding grows.
- **Screen-agreement test**: Shared screens reduce different interpretations of written paragraphs.

## Anti-patterns
- **Spec fantasy**: Words on paper ignore builders, designers, and users.
- **Signature agreement**: Sign-off does not prove that everyone imagines the same behavior.
- **Bullet-point growth**: No pushback lets free additions create an overloaded site with thirty tabs.
- **Early lock-in**: A signed feature becomes hard to remove after development exposes its problems.
- **Theory-driven software**: Matching code to a spec can produce poor work when the spec misses reality.
- **Requirements blockade**: Long documents delay prototypes, design changes, and customer learning.

## Worked Example
Mark Gallagher’s team started with a few ideas for improving a site. It made a quick static prototype, changed the design, and built a live prototype with real data. After testing that prototype, the team had a real project and a better result. Screens and use taught more than a long requirements document.

## Key Takeaways
1. Replace a detailed functional spec with a one-page story.
2. Finish the story in one day and use plain language.
3. Sketch and build the interface before backend work.
4. Use screens to expose different interpretations.
5. Make key decisions after building provides information.
6. Let prototypes change before locking the product.
7. Treat long requirements phases as possible blockers.

## Connects To
- **Chapter 31, From Idea to Implementation**: Moves ideas toward real implementation through small steps.
- **Chapter 46, Interface First**: Uses the interface as the first shared artifact.
- **Chapter 54, Less Software**: Prevents feature overload and questions complex plans.
- **Chapter 56, Code Speaks**: Lets working code reveal a simpler direction.
