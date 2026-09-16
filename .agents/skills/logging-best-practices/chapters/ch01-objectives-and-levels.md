# Section 1: Objectives and Log Levels

## Core Idea
Decide why you log before you write a log statement. Then assign every event a severity level. This section is the foundation for all other practices.

## Frameworks Introduced
- **Log with objectives**: Before you write a log statement, answer three questions. What are the application's main goals? What critical operations need monitoring? Which KPIs matter? An error log must give enough context to fix the problem, not just announce that something broke. Start by over-logging, then trim back. Removing noise is easier than adding missing information in production. Review the logging strategy periodically.
- **Use log levels as a scale**: Sort events by severity with four common levels:
  - **INFO**: Business as usual. Examples: successful user login, completed checkout with order number.
  - **WARNING**: Early warning system. Example: payment processing takes longer than usual.
  - **ERROR**: Real problem. Examples: failed payment, failed database connection, crashed service.
  - **FATAL**: Everything went wrong. Example: system out of memory, application shutting down.
- **Runtime verbosity control**: Production most often defaults to INFO to keep output clean. Plan to raise verbosity temporarily while investigating bugs, because the INFO level may not include key troubleshooting information. Give the application a way to manage verbosity when needed, like the verbosity selectors in common developer tools.

## Key Concepts
- **Logging objective**: The purpose of a log statement, such as providing fixable context for an error.
- **KPI**: A metric that matters to the application, such as checkout completion.
- **Critical operation**: A code path that needs monitoring, such as payment processing.
- **Verbosity**: The amount of detail a logger emits at a chosen level.
- **Level filter**: The mechanism that keeps INFO and below out of production output.

## Mental Models
- **Think about the future you**: Write logs for the person debugging at 3:00 a.m., not for the moment the code runs.
- **The objective is the fix**: An error log that cannot help repair the failure is noise.
- **Start full, trim later**: Missing information in production is the expensive failure mode.
- **Levels are a ladder**: Each level means a different degree of urgency, from routine to catastrophic.

## Anti-patterns
- **Logging without objectives**: Throwing log statements everywhere and hoping something sticks.
- **A wall of text with no plan**: Logging everything at one level with no structure or purpose.
- **No verbosity control**: An application that cannot raise detail during an incident.
- **Never reviewing the strategy**: Keeping logs that stopped being useful long ago.

## Worked Example
A payment service logs "payment failed" at ERROR level with no other detail. The on-call engineer sees the message but cannot act. The same service logs the objective-first way: ERROR level, the payment ID, the provider response, the retry count, and the user ID. The engineer now knows what failed, who it affected, and what to look at next.

## Key Takeaways
1. Define objectives before you write a log statement.
2. Use INFO, WARNING, ERROR, and FATAL to sort severity.
3. Plan to raise verbosity during incident investigation.
4. Give the application a runtime way to change verbosity.
5. Review and trim the logging strategy periodically.

## Connects To
- **Section 2, Structure and Context**: Objectives decide what to log; structure decides how to write it.
- **Section 3, Volume Control**: Levels and objectives guide what to sample and what to keep complete.
- **Section 6, Performance and Monitoring**: The level filter also controls cost and throughput.
