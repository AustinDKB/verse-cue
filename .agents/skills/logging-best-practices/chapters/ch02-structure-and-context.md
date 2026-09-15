# Section 2: Structure and Context

## Core Idea
Write logs as structured fields, and fill those fields with the context needed to replay an incident. Machines must be able to read the logs, and humans must be able to reconstruct what happened.

## Frameworks Introduced
- **Log in structured fields**: Give every piece of information its own field. Example fields: `event`, `user_id`, `order_id`, `duration_ms`. Structured logs let you filter, search, and analyze: find all timeout errors, or count how many errors happened last Tuesday. Use a logging framework that emits structured records for your language. When a service only emits text logs, use a tool such as Vector to transform them into parseable JSON. Unstructured logs are essentially expensive text files.
- **Log the context to replay the incident**: Capture the who, what, where, and why in one entry. A useful entry for broken logins holds the user ID, the location, the device info, and the attempt count. Capture these in every log entry:
  - **Request IDs**: For tracing a request across microservices.
  - **User IDs**: For session context when needed.
  - **System state**: Database or cache status.
  - **Full error context**: Stack traces when relevant.

## Key Concepts
- **Structured log**: A record with named fields that machines can parse.
- **Parseable JSON**: A text format for logs that tools can load as data.
- **Request ID**: An identifier that links one request's log entries across services.
- **Stack trace**: The call path that produced an error.
- **Black box recorder**: The model for logs that are detailed enough to replay any scenario.

## Mental Models
- **Logs are the black box recorder**: Logs must let you replay and understand any scenario, not just know that it happened.
- **A field is a query**: Every named field is a future filter, search, or aggregation.
- **Human-readable is not enough**: Text that people can read may be unreadable to machines.
- **Context is the fixer**: The who, what, where, and why turn a message into a repair.

## Anti-patterns
- **Writing expensive text files**: Emitting prose lines that tools cannot parse.
- **"Something's wrong" messages**: Log entries with no field, no cause, and no actor.
- **Skipping request IDs**: Losing the ability to join entries from one request.
- **Omitting stack traces**: Keeping the error message but removing the path to the failure.

## Worked Example
A log entry says "login failed". It is technically true and completely useless. The structured version adds fields: `user_id`, `attempt_count`, `device`, `ip_location`, `failure_reason`. When logins break, the engineer has everything needed without a second query.

## Key Takeaways
1. Put every piece of information in its own field.
2. Use a structured logging framework for your language.
3. Transform text logs into parseable JSON with a tool like Vector.
4. Capture request IDs, user IDs, system state, and error context.
5. Make logs detailed enough to replay the incident.

## Connects To
- **Section 1, Objectives and Levels**: Objectives say what to capture; structure says how to write it.
- **Section 3, Volume Control**: Structured fields make canonical log lines and selective sampling possible.
- **Section 4, Aggregation and Retention**: Centralized search works only when logs share a structure.
