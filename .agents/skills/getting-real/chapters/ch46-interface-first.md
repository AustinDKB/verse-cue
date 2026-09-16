# Chapter 46: Interface First

## Core Idea
Design the interface before programming because design stays cheap to change while code becomes expensive to change. The interface is the product, so real screens must guide scope, budget, usability, and later feature decisions.

## Frameworks Introduced
- **Interface First — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Start an application with the interface rather than a program-first plan.
  - **When to use**: Use it at the start of a new application or feature, before the team commits to expensive code.
  - **How**: Sketch the screen on paper, move to simple HTML when useful, revise the design with real screens, and ask whether it makes sense, works easily, and solves the problem.
- **Design before programming — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Keep early decisions flexible by making the lightest artifact first.
  - **When to use**: Use it when the team does not yet know the best interface, scope, or implementation cost.
  - **How**: Change or discard sketches and HTML before programming fences the team into costly decisions.
- **Design as project benchmark — Josh Williams**: Use a finished interface design as a scope and budget guide.
  - **When to use**: Use it when bootstrapping a project and the team must predict developer effort and cost early.
  - **How**: Show the design to the developer, estimate the work from the screens, and return to the design when a new feature requests a place.

## Key Concepts
- **Program-first mentality**: Starting with code before the team understands the interface.
- **Interface**: The visible product that customers use and judge.
- **Paper sketch**: A cheap design artifact that the team can change quickly.
- **HTML design**: A simple screen model that makes an application feel real before code exists.
- **Real screen**: A visible interface used to judge sense, ease, and problem fit.
- **Flexibility**: The ability to change direction before expensive programming locks decisions.
- **Scope benchmark**: A design that defines the first project boundary.
- **Feature gate**: A question about where a proposed feature belongs in the existing design.
- **Programming cost**: The heavier cost of building and changing working software.

## Mental Models
- **Cheap-to-expensive sequence**: Move from paper to HTML to programming so the cost of change rises only after the idea gains clarity.
- **Interface is the product**: Judge the product through the screens customers see, not through code hidden behind them.
- **Screen question loop**: Revisit whether the screen makes sense, feels easy, and solves the problem throughout development.
- **No-place rule**: If a new feature has no clear place in the design, do not add it automatically.

## Anti-patterns
- **Code-first start**: Programming creates expensive decisions before the team can judge the interface.
- **Late interface layer**: Adding the interface at the end exposes gaps that early screens would have shown.
- **Design-free scope**: Accepting features without a screen boundary causes uncontrolled growth.
- **Invisible design handoff**: Waiting until every detail aligns delays the dialogue between designer and developer.
- **Mockup neglect**: Skipping cheap sketches removes a fast way to find confusion and waste.

## Worked Example
Josh Williams became frustrated with off-the-shelf invoicing software. He used an orange pen to draw about 75 percent of his preferred interface in a few hours. Over the next two weeks, he refined the drawings into static HTML for most of Blinksale’s first version. He then showed the design to developer Scott. The screens gave Scott a clear vision, helped estimate effort and budget, and set the first project scope. When new features appeared, the team asked where each one belonged. A feature without a place did not enter the application.

## Key Takeaways
1. Design the interface before writing expensive code.
2. Start with paper when paper is enough.
3. Use HTML to make the product real before implementation.
4. Revise screens while the team can still change them cheaply.
5. Use the interface to estimate effort, budget, and scope.
6. Reject features that have no clear place in the design.

## Connects To
- **Chapter 16, Ignore Details Early On**: Keeps early work light while the main shape becomes clear.
- **Chapter 29, Race to Running Software**: Moves from design to a usable product without unnecessary delay.
- **Chapter 47, Epicenter Design**: Gives the interface-first process a priority order inside each page.
- **Chapter 49, The Blank Slate**: Makes the first-run screen part of the interface instead of an afterthought.
