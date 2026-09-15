# Chapter 54: Less Software

## Core Idea
Keep code and features simple because complexity grows faster than size. Reframe hard problems into smaller problems, and build only the software that today’s need justifies. Less software lowers maintenance, change cost, bugs, support, and staff burden.

## Frameworks Introduced
- **Less Software — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Choose fewer features, less code, and less waste instead of adding every possible capability.
  - **When to use**: Use it when a request adds dependencies, maintenance, support work, or uncertain future behavior.
  - **How**: Restate the hard problem as a simple one. Write only the code that the current product needs.
- **80/20 Reframe — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Solving 80 percent of the original problem with 20 percent of the effort can be a major win.
  - **When to use**: Use it when full coverage needs far more effort than the extra value.
  - **How**: Keep the important result, remove lesser cases, and compare the smaller solution with the full cost. The original problem rarely needs five times the effort.
- **Programmer Counteroffer — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Ask programmers to challenge an expensive implementation with a smaller alternative.
  - **When to use**: Use it before accepting a plan that needs many hours or many lines.
  - **How**: Hear both paths and compare what the shorter path omits.
- **There Is No CODE That Is More Flexible Than NO Code — Brad Appleton, software engineer**: Leaving code out can create more flexibility than adding a design for every case.
  - **When to use**: Use it when a requirement seems to demand a new model or many special cases.
  - **How**: Look for a simpler rule, input limit, or interface change that removes the need for code.
- **Complexity Does Not Scale Linearly With Size — The Ganssle Group, from *Keep It Small***: A larger program needs more than a proportional increase in development effort.
  - **When to use**: Use it when someone treats added code as a simple cost.
  - **How**: Count interdependencies and maintenance effects, then keep the program small.

## Key Concepts
- **Less software**: A product strategy based on fewer features, less code, and less waste.
- **Big Ball of Mud**: A tangled system created by reckless additions and dependencies.
- **Interdependency**: A connection in which one change affects another part of the system.
- **Cost of change**: The effort needed to alter working software.
- **Phantom issue**: A feared future problem that may never occur.
- **Counteroffer**: A programmer’s simpler proposal that meets the main need with less work.
- **Detour**: A path that avoids writing more software while still helping the customer.
- **No code**: A deliberate choice to solve a need without adding implementation.

## Mental Models
- **Compounding complexity**: Treat each addition as a change that can affect many existing parts.
- **80/20 lens**: Separate the main result from extra cases before choosing the full solution.
- **Crystal-ball refusal**: Solve today’s real problem instead of fears about tomorrow.
- **Detour search**: Before changing the software model, ask whether copy or input limits can solve the need.

## Anti-patterns
- **Reckless feature growth**: Added code creates cascading changes, bugs, support work, and confusion.
- **Future-problem building**: Phantom issues consume time even when they never occur.
- **Automatic feature acceptance**: Hard requests enter without a value test or smaller alternative.
- **Unchallenged implementation**: A first plan can hide a one-hour solution behind a twelve-hour plan.
- **Server-side overreach**: Software manipulation can replace a simpler rule, such as requesting an image at a specific size.

## Worked Example
A team receives a request that appears to need a large feature and many lines of code. The programmer says the proposed path needs twelve hours, then offers a one-hour version that omits one part but provides the main result. The team keeps the smaller path when it serves the real need. If the need only concerns image dimensions, copy can request a specific size instead of adding server-side image manipulation.

## Key Takeaways
1. Reframe hard problems before writing a large solution.
2. Compare the main result with the cost of extra cases.
3. Ask programmers for counteroffers to expensive plans.
4. Solve today’s problems instead of phantom future problems.
5. Search for copy or input changes that remove software work.
6. Let an idea sit for a week before committing to it.

## Connects To
- **Chapter 04, Build Less**: Sets the product direction toward a smaller application.
- **Chapter 11, Lower Your Cost of Change**: Shows why a smaller codebase stays easier to change.
- **Chapter 56, Code Speaks**: Uses technical difficulty as a signal to search for a better path.
