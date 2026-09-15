# Chapter 24: Hidden Costs

## Core Idea
Expose the full price of a feature before you build it. A small request can create a feature loop, expand the interface, add support work, change public promises, and become a major operational burden.

## Frameworks Introduced
- **Expose the price of new features — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use this before a feature moves from an approved idea to implementation.
  - **When to use**: Use it after a request survives the initial no decision and proves enough value for further review.
  - **How**: Trace the feature from no, proof of value, and a second decision through interface sketches, interface design, code, repeated testing and tweaking, documentation, product-tour and marketing updates, terms-of-service review, promise review, pricing review, launch, and post-launch risk.
- **Feature loop — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Treat one feature as a possible source of more features.
  - **When to use**: Use it when a request looks simple because its first screen or action seems small.
  - **How**: List every supporting object, workflow, integration, document, and promise that the feature could require. Count the work outside the visible screen.
- **Make the feature work hard to earn implementation — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Preserve the default no rule while examining cost.
  - **When to use**: Use it when value seems possible but the request still creates uncertain work.
  - **How**: End the review when the feature fails to prove value. Continue only when value survives and the complete cost remains manageable.

## Key Concepts
- **Hidden cost**: Work that a feature creates outside its primary code path.
- **Feature loop**: A feature that causes requests for related features and support systems.
- **Proof of value**: Evidence that justifies moving beyond the default no.
- **Interface sketch**: A rough screen used to expose scope before design and code.
- **Support surface**: Help text, tours, marketing, and other material that must describe the feature.
- **Public promise**: A statement about product behavior that a feature can change.
- **Pricing impact**: A change to the cost or plan structure caused by new capability.
- **Post-launch risk**: The uncertainty that remains after release.

## Mental Models
- **Feature iceberg**: See the visible screen as the small part of a larger work system.
- **Snowball test**: Ask what this request pulls behind it before calling it simple.
- **Breath-before-launch**: Treat launch as the start of exposure, not the end of work.
- **Cost follows commitment**: Every released promise creates future design, support, and maintenance work.

## Anti-patterns
- **Screen-only estimation**: Count only the visible interface and miss integrations, help, pricing, and legal work.
- **Feature-loop blindness**: Accept a meeting tab without examining locations, times, rooms, people, invites, calendars, and support material.
- **Second-yes shortcut**: Skip the renewed value decision after the initial review.
- **Launch-and-forget**: Release without checking broken promises, changed pricing, or updated public information.
- **False simplicity**: Call an idea easy because the first action needs little code.

## Worked Example
A request for a meetings tab in Basecamp sounds small. A fuller review exposes fields for location, time, room, and people. It also raises email invites, calendar integration, support documentation, product-tour changes, promotional screenshots, frequently asked questions, help pages, and terms of service. The team must then sketch and design the screens, code them, repeat testing and tweaking, check promises and pricing, update related material, launch, and accept the risk that users will depend on the new feature. The request becomes a product change, not a single tab.

## Key Takeaways
1. Say no before you spend time on a feature.
2. Require proof of value before detailed design.
3. Map the feature loop and all support work.
4. Review promises, pricing, documentation, and marketing before launch.
5. Stop when the hidden cost exceeds the proven value.

## Connects To
- **Chapter 23, Start With No**: Supplies the first decision before hidden-cost analysis.
- **Chapter 25, Can You Handle It?**: Tests whether the remaining commitment fits the organization.
- **Chapter 32, Avoid Preferences**: Shows how one small option can create extra code and test paths.
