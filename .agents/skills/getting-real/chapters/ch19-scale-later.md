# Chapter 19: Scale Later

## Core Idea
Do not build for millions of users before the product shows that millions of users exist. Build a solid core product with the simplest setup, launch it, collect real data, and address scale when success makes it a real problem.

## Frameworks Introduced
- **Scale later — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use this rule when an early product faces fear about future traffic.
  - **When to use**: Use it before launch, when the team considers clusters, server farms, or months of architecture work without current demand.
  - **How**: Build the core product first. Choose the simplest setup that supports present use. Launch, observe actual load, and improve the parts that real benchmarks show need attention.
- **Single-server start — Basecamp team**: Use a small deployment as an early test of product demand and system needs.
  - **When to use**: Use it when a single server can support current users and the team lacks real load data.
  - **How**: Start with the simple setup, monitor its limits, and add capacity only after use creates a clear reason.
- **Revisit every aspect — Dare Obasanjo**: Treat scale as a later design problem that may require broad changes.
  - **When to use**: Use it when growth changes the service from its original size and assumptions no longer hold.
  - **How**: Accept that a service moving from zero to millions needs review of almost every design and architecture choice. Use new data to guide each revision.

## Key Concepts
- **Scalability**: The ability of a service to support increased use.
- **Scale problem**: A capacity problem created by real demand.
- **Solid core product**: A useful product whose primary work operates well.
- **Simple setup**: The smallest system arrangement that supports current use.
- **Real-world data**: Measurements from actual users and service load.
- **Benchmark**: A measured result used to locate a system limit.
- **Server farm**: A large group of servers prepared for expected demand.
- **Growing pain**: A temporary service problem caused by increased use.

## Mental Models
- **Scale as an earned problem**: Treat the need to scale as evidence of success, not as a starting requirement.
- **Data beats prediction**: Use actual load and benchmarks instead of imagined millions of users.
- **Simple first commitment**: Make the early system easy to build and easy to replace when evidence demands it.
- **Communication reduces impact**: A brief slowdown is less damaging when customers know what happens.

## Anti-patterns
- **Perfect setup before launch**: Months of preparation delay learning and may solve a problem that never occurs.
- **Starting with fifteen boxes**: Large infrastructure adds cost and complexity before the product proves demand.
- **Treating scale as all or nothing**: A service can usually adjust in stages as load increases.
- **Ignoring the core product**: Capacity work cannot help a product that does not yet provide value.
- **Hiding service problems**: Silence makes ordinary growing pains harder for customers to accept.

## Worked Example
Basecamp ran on a single server for its first year. The simple setup took about one week to implement, so the team did not delay launch to create a cluster of fifteen boxes. The service had a few problems, including brief slowdowns, but customers often found those problems acceptable when the team kept them informed. After launch, the team had real data and benchmarks instead of guesses about the perfect setup.

## Key Takeaways
1. Make the core product useful before optimizing for extreme scale.
2. Start with the simplest setup that supports current demand.
3. Launch to obtain real load data and benchmarks.
4. Increase capacity when evidence shows a need.
5. Treat a scaling problem as good evidence that the product reached users.
6. Tell customers about growing pains while the team responds.

## Connects To
- **Chapter 11, Lower Your Cost of Change**: Simple systems leave more room for later architecture changes.
- **Chapter 17, It Is a Problem When It Is a Problem**: Scale matters after real demand creates it.
- **Chapter 22, It Just Doesn't Matter**: Early capacity that changes no current behavior does not matter yet.
- **Chapter 29, Race to Running Software**: Launch supplies the data needed for scale decisions.
