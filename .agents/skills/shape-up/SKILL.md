---
name: shape-up
description: "Knowledge base from \"Shape Up: Stop Running in Circles and Ship Work that Matters\" by Ryan Singer. Use when applying Shape Up frameworks for shaping, appetites, betting, cycles, scopes, Hill Charts, and scope hammering, studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Shape Up: Stop Running in Circles and Ship Work that Matters
**Author**: Ryan Singer | **Pages**: ~176 | **Chapters**: 20 | **Generated**: 2026-08-13

## How to Use This Skill

- **Without arguments** — load the core frameworks and decision rules.
- **With a topic** — ask about `appetite`, `rabbit holes`, `Hill Charts`, or another indexed topic.
- **With a chapter** — ask for `ch05` or `ch14` to load that chapter.
- **Browse** — ask which chapters or supporting files cover a topic.

When a question needs detail outside Core Frameworks, read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### 1. Shape before you bet
Use **shaping** when a raw idea may consume a fixed cycle. Set the **appetite**, narrow the problem to a concrete use case, find the elements, remove **rabbit holes**, and write a **pitch**. A shaped concept must be **rough**, **solved**, and **bounded**. Rough work leaves room for the builders. Solved work connects the macro elements and answers visible open questions. Bounded work states the appetite and what the team will not do.

Use the right **level of abstraction**. Wireframes are too concrete because they commit detail and reduce room for later design. Words are too abstract because they do not give the team enough context for trade-offs. Use **breadboards** for flow and topology. Draw **Places**, **Affordances**, and **Connection lines**. Use **fat marker sketches** when visual arrangement carries the idea. Keep shaping private until the concept is ready to present.

### 2. Set appetite, then vary scope
Use **fixed time, variable scope**. **Small Batch** means one or two weeks for one designer and one or two programmers. **Big Batch** means one full six-week cycle for the same team. An appetite starts with a number and ends with a design. An estimate starts with a design and ends with a number.

Treat “good” as relative to the appetite and the customer baseline. Ask what is really going wrong instead of asking what a broad feature should contain. Respond to raw ideas with **“Interesting. Maybe some day.”** A broad label such as “Files 2.0” is a **grab-bag** until it becomes a specific problem with a clear definition of done.

### 3. De-risk the concept
Before the bet, walk the use case in slow motion. Ask whether each element needs new technical work, assumes hidden dependencies, relies on a design solution you cannot see, or contains a decision the team should not make under deadline. A **rabbit hole** creates a fat risk tail. Patch it with a deliberate compromise, declare unsupported cases **out of bounds**, and cut attractive but unnecessary parts.

Ask technical experts, **“Is X possible in six weeks?”** Do not ask only whether X is possible. Keep the clay wet during review so the concept can change. Put patches, assumptions, and **No Gos** in the pitch.

### 4. Pitch a potential bet
A pitch has five ingredients:

1. **Problem** — a specific story that shows why the current baseline fails.
2. **Appetite** — the time worth spending.
3. **Solution** — the core elements that fit the appetite.
4. **Rabbit holes** — details that prevent later traps.
5. **No Gos** — functionality or use cases excluded on purpose.

Present the problem and solution together. Use an embedded or annotated sketch only when readers need it to understand a linchpin. Post the pitch for asynchronous reading and comments. Let the **betting table** make the commitment.

### 5. Bet one cycle with a capped downside
Use a **six-week cycle** as the standard time horizon. Six weeks is long enough for meaningful work and short enough for the deadline to feel real. Follow each cycle with a two-week **cool-down** for recovery, bugs, experiments, and the next betting table. Bet only one cycle ahead so future options stay open.

A bet has a payout, a commitment, and a cap on the downside. Protect the team from interruption. By default, a project that misses the cycle does not get an extension. This **circuit breaker** prevents runaway work and sends a missed concept back to shaping. Ordinary bugs wait for cool-down, a deliberate bug bet, or an annual **bug smash**. Only a true crisis justifies interruption.

### 6. Match the product mode
For an existing product, shape, bet, build, and ship a version to customers. For a new product, use three modes:

- **R&D mode** — senior people spike core ideas and architecture. Learn rather than promise a customer ship.
- **Production mode** — use formal shaping, betting, and building after the core architecture settles. Shipping means merging into the main codebase.
- **Cleanup mode** — near launch, drop normal shaping and team boundaries, merge small changes continuously, and make the final cut. Keep it to two cycles or less.

Keep each commitment to one cycle even when the larger product may need many cycles.

### 7. Hand over responsibility and integrate early
Assign a whole project, not tasks. The team owns its tasks, trade-offs, and result within the pitch boundaries. **Done means deployed**, including essential testing within the cycle. Respect the first few days of orientation. If silence does not break after about three days, ask what is happening.

**Get One Piece Done** by choosing a first slice that is **core**, **small**, and **novel**. Integrate design and code early. Use affordances before pixel-perfect screens. Program only enough for the next step, including temporary scaffolding or simple authentication when those choices support learning. First make it work, then make it beautiful.

### 8. Map scopes and show uncertainty
Organize by project structure, not by person. **Scopes** are integrated slices that can finish independently. Discover them through real work. Use scope names as the language of the project. Use a **Chowder** list only for a few loose tasks. More than three to five items signals a missing scope. Mark nice-to-haves with `~`.

Use the **Hill Chart** instead of task counts or numerical estimates. **Uphill** means unknowns or unsolved problems remain. **Downhill** means the path is known and execution remains. Build your way uphill: think about the approach, validate it, then build enough to expose remaining unknowns. Solve the riskiest important work first. A motionless dot is a raised hand. Split a scope when its parts move independently.

### 9. Hammer scope and move on
Compare the work to the customer **baseline**, not to an ideal. Scope grows like grass because real work reveals details. Constantly ask whether a task is a must-have, whether customers can use the feature without it, whether it is new or pre-existing, who sees it, how often it occurs, and what its real impact is. Cutting scope is not lowering quality. It focuses quality on the core use cases.

QA hunts edge cases after the team owns basic quality. Treat QA findings as nice-to-haves by default, then elevate severe issues into the affected scope. Extend a project only in rare cases when true must-haves survived every cut and all remaining work is downhill.

After release, let the storm pass. Keep a clean slate. Feedback is a raw idea that needs shaping before a new bet.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|---|---|
| [ch01](chapters/ch01-introduction.md) | Introduction | Six-week cycles, shaping, target risk |
| [ch02](chapters/ch02-principles-of-shaping.md) | Principles of Shaping | Rough, solved, bounded, two tracks |
| [ch03](chapters/ch03-set-boundaries.md) | Set Boundaries | Appetite, fixed time, narrow problem |
| [ch04](chapters/ch04-find-the-elements.md) | Find the Elements | Breadboarding, fat marker sketches |
| [ch05](chapters/ch05-risks-and-rabbit-holes.md) | Risks and Rabbit Holes | Thin-tailed risk, patches, out of bounds |
| [ch06](chapters/ch06-write-the-pitch.md) | Write the Pitch | Five pitch ingredients, No Gos |
| [ch07](chapters/ch07-bets-not-backlogs.md) | Bets, Not Backlogs | Potential bets, decentralized lists |
| [ch08](chapters/ch08-the-betting-table.md) | The Betting Table | Six-week cycle, cool-down, circuit breaker |
| [ch09](chapters/ch09-place-your-bets.md) | Place Your Bets | R&D, production, cleanup modes |
| [ch10](chapters/ch10-hand-over-responsibility.md) | Hand Over Responsibility | Projects not tasks, done deployed |
| [ch11](chapters/ch11-get-one-piece-done.md) | Get One Piece Done | Vertical slices, core-small-novel |
| [ch12](chapters/ch12-map-the-scopes.md) | Map the Scopes | Scopes, layer cakes, icebergs, Chowder |
| [ch13](chapters/ch13-show-progress.md) | Show Progress | Hill Chart, uphill, downhill |
| [ch14](chapters/ch14-decide-when-to-stop.md) | Decide When to Stop | Baseline, scope hammering, QA |
| [ch15](chapters/ch15-move-on.md) | Move On | Let the storm pass, stay debt-free |
| [ch16](chapters/ch16-conclusion.md) | Conclusion | Connected method, key concepts |
| [ch17](chapters/ch17-how-to-implement-shape-up-in-basecamp.md) | How to Implement Shape Up in Basecamp | Teams, projects, scope lists, Hill Charts |
| [ch18](chapters/ch18-adjust-to-your-size.md) | Adjust to Your Size | Basic truths, scale-dependent practices |
| [ch19](chapters/ch19-how-to-begin-to-shape-up.md) | How to Begin to Shape Up | Three adoption options, shipping first |
| [ch20](chapters/ch20-glossary.md) | Glossary | Term distinctions |

## Topic Index

- **Appetite** → ch01, ch02, ch03, ch06, ch08, ch14
- **Baseline** → ch03, ch14
- **Betting table** → ch06, ch07, ch08, ch09
- **Breadboarding** → ch02, ch04, ch06
- **Building track** → ch02, ch10
- **Circuit breaker** → ch01, ch08, ch14
- **Cleanup mode** → ch09
- **Cool-down** → ch01, ch08
- **Discovered tasks** → ch10, ch11, ch12
- **Fat marker sketches** → ch02, ch04, ch06
- **Fixed time, variable scope** → ch03, ch14
- **Hill Chart** → ch13, ch17
- **Icebergs** → ch12
- **Level of abstraction** → ch02, ch04
- **Must-haves and nice-to-haves** → ch12, ch14
- **No Gos** → ch05, ch06
- **Pitch** → ch05, ch06, ch08
- **Product modes** → ch09
- **Rabbit holes** → ch02, ch05, ch06, ch08
- **R&D mode** → ch09
- **Raw ideas** → ch03, ch07, ch15
- **Scope hammering** → ch12, ch14
- **Scopes** → ch11, ch12, ch13, ch14
- **Shaping** → ch01, ch02, ch03, ch04, ch05
- **Six-week cycles** → ch01, ch08, ch09, ch19
- **Small Batch and Big Batch** → ch03, ch08
- **Uphill and downhill** → ch13, ch14
- **Vertical slices** → ch11, ch12

## Supporting Files

- [glossary.md](glossary.md) — key terms and chapter references
- [patterns.md](patterns.md) — techniques and patterns
- [cheatsheet.md](cheatsheet.md) — decision rules and quick reference

---

## Scope & Limits

This skill covers Ryan Singer's book content only. Combine it with project-specific tools for implementation. For topics beyond the book, check related skills or ask the agent directly.
