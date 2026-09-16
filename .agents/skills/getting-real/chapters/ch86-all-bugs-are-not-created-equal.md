# Chapter 86: All Bugs Are Not Created Equal

## Core Idea
Treat bugs according to their impact, not according to the fear they create. Every software product has bugs, but an annoyance does not need the same response as a defect that destroys a database. Ask how many people a bug affects, how bad the problem is, and what action creates the greatest benefit for the greatest number.

A team can table visual mistakes while it handles destructive failures. A new feature can sometimes matter more than a low-impact bug. Discuss bugs openly without blame, then communicate honestly when lower-priority work waits.

## Frameworks Introduced
- **Impact-Based Bug Prioritization — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Rank bugs by reach, severity, and product impact.
  - **When to use**: Use it whenever the team discovers a bug or receives a customer complaint.
  - **How**: Ask how many people are affected. Ask how bad the problem is. Decide whether the bug needs immediate attention or can wait. Choose the action with the greatest impact for the greatest number of people.
- **Misdemeanor versus Destructive Bug — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Separate annoying or cosmetic mistakes from failures that threaten customer data.
  - **When to use**: Use it during triage when the bug list contains both visible annoyances and serious data risk.
  - **How**: Table “it does not look right” errors and other misdemeanor miscues when necessary. Fix a bug that destroys the database immediately.
- **Feature-versus-Bug Trade-off — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Compare a new feature with a low-impact bug.
  - **When to use**: Use it when both compete for the same work time.
  - **How**: Compare affected customers and expected benefit. Choose the work with greater impact, and explain the choice when customers ask.
- **Open Bug Culture and Honest Bug Communication — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Keep bugs visible and explain delayed work.
  - **When to use**: Use it whenever a team finds a defect or a customer reports one.
  - **How**: Focus on impact and repair without blame. Tell customers that the team noted the issue. Explain when work waits because other areas affect more people.

## Key Concepts
- **Bug**: A product defect that causes incorrect, unexpected, or unwanted behavior.
- **Impact**: The total effect of a bug on customers and the product.
- **Reach**: The number of people affected by a bug.
- **Severity**: How bad the result is for an affected customer.
- **Annoyance**: A problem that frustrates customers but does not destroy important data.
- **Misdemeanor miscue**: A minor error, such as a display problem, that can wait.
- **Database destruction**: A failure that damages or destroys customer data.
- **Bug culture**: The team’s shared way of discussing and repairing defects.

## Mental Models
- **Impact before panic**: A bug report starts an assessment, not an automatic emergency.
- **Reach multiplied by severity**: The team should favor problems that affect many people or cause severe harm.
- **Opportunity cost applies to bugs**: Time spent on one bug cannot serve customers through another repair or feature.
- **Transparency without instant work**: Honest communication can preserve trust even when the team delays a lower-impact fix.

## Anti-patterns
- **Instant-fix reflex**: Fixing every bug immediately ignores reach, severity, and larger customer impact.
- **Panic culture**: Treating every defect as a crisis wastes attention and makes judgment harder.
- **Blame hunt**: Searching for a person to punish discourages people from reporting bugs.
- **Rug hiding**: Concealing defects prevents the team from discussing and repairing them.
- **Severity blindness**: Treating a database-destroying bug like a visual annoyance risks serious customer harm.

## Worked Example
A team finds a visual bug affecting a small group and another bug that can destroy the database. It tables the visual bug and fixes the database failure immediately. When a customer reports the lower-impact issue, the team explains that work affecting more people comes first. Both bugs remain visible without blame.

## Key Takeaways
1. Rank bugs by affected people and problem severity.
2. Fix data-destroying failures immediately.
3. Table minor visual annoyances when higher-impact work needs attention.
4. Compare a feature’s benefit with a low-impact bug’s benefit.
5. Keep bugs visible and remove blame from bug discussion.
6. Explain delayed bug work honestly.

## Connects To
- **Chapter 79, Answer Quick**: Requires a fast acknowledgement even when the repair waits.
- **Chapter 80, Tough Love**: Applies product judgment instead of obeying every request for a fix.
- **Chapter 82, Publicize Your Screwups**: Extends honest failure communication to public incidents.
- **Chapter 85, Better Not Beta**: Defines responsible ownership after public release.
