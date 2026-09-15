# Section 5: Security

## Core Idea
Logs hold user IDs, IP addresses, database queries, authentication attempts, and error messages with internal details. Protect them like the sensitive data they are, and make sure sensitive data never enters them in the first place.

## Frameworks Introduced
- **Secure logs in transit, at rest, and by access**: Lock logs down three ways:
  - **Encryption in transit**: Protect logs as they move from the application to storage.
  - **Encryption at rest**: Keep them secure while they are stored.
  - **Access controls**: Only the right people can read them. Junior developers see basic application logs. Senior engineers see more sensitive system logs. The security team gets full access for investigations.
  - Some log managers provide audit logging, so you can track who accessed what and when.
- **Never log sensitive data**: Even if information seems mundane, follow security-by-obscurity and keep it out of logs. The video's incidents: in 2018 Twitter forced a reset of all user passwords because plain-text passwords were logged. GitHub was caught in a similar situation. These were companies with excellent engineers. Defenses:
  - Mask sensitive fields at the source. Go's `slog` package, when given a whole user object, logs only the ID as a safety net.
  - Add filters in the logging pipeline that catch and redact anything sensitive: credit card numbers, social security numbers, API keys, before they reach log storage.
  - Use the OpenTelemetry Collector for pipeline redaction.

## Key Concepts
- **Encryption in transit**: Protecting data while it travels between systems.
- **Encryption at rest**: Protecting stored data.
- **Access control**: Rules about who may read logs.
- **Audit logging**: Recording who accessed what, and when.
- **Redaction**: Removing sensitive values from log records.
- **Security by obscurity**: Keeping sensitive information out of reach by not exposing it.

## Mental Models
- **The best leak is the one that never happens**: If the data was never logged, it cannot leak.
- **Assume logs will be read**: Write logs as if an attacker will see them.
- **Layers, not a single lock**: Transit encryption, at-rest encryption, and access controls work together.
- **Small companies are not the only victims**: Twitter and GitHub made these mistakes; plan as if you will too.

## Anti-patterns
- **Logging passwords in plain text**: The Twitter 2018 incident and its forced password reset.
- **Logging whole user objects**: Dragging every field of a user record into the logs.
- **No redaction pipeline**: Sensitive values reaching storage because nothing filters them.
- **Open access for everyone**: Every employee able to read production logs and their contents.

## Worked Example
An engineer adds a debug line that logs the entire user object during a login investigation. In Go with `slog`, the record shows only the user ID, because the framework masks the rest. In a system without that safety net, the same line would write the user's personal data to storage. A pipeline filter that redacts patterns such as credit card numbers and API keys catches the cases the framework misses.

## Key Takeaways
1. Encrypt logs in transit and at rest.
2. Grant access by role: developers, senior engineers, security team.
3. Use log managers with audit logging.
4. Never log passwords, tokens, or personal data.
5. Mask sensitive fields at the source, for example with Go's `slog`.
6. Redact sensitive patterns in the pipeline, for example with the OpenTelemetry Collector.

## Connects To
- **Section 2, Structure and Context**: Context fields are exactly what needs redaction care.
- **Section 4, Aggregation and Retention**: The central store concentrates security risk and access rules.
- **Section 6, Performance and Monitoring**: Redaction filters run in the pipeline, where performance matters.
