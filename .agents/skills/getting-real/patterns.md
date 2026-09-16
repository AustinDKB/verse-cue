# Patterns

## One-Point Vision
**When to use**: Before design and code, or when a difficult choice reaches a sticking point.
**How**: Write one sentence that states the product’s purpose and difference. Use it as a filter. Basecamp’s example was “Project management is communication.”
**Trade-offs**: A narrow vision rejects familiar category features, but it gives the team a clear product boundary. (Ch 15)

## Fix Time and Budget, Flex Scope
**When to use**: When the launch date or budget cannot grow.
**How**: Fix time and budget. Rank the work. Remove lower-value scope. Protect quality instead of rescuing every feature.
**Trade-offs**: The first release contains less, but it avoids the quality loss that follows when time, budget, and scope all stay fixed. (Ch 7)

## The Three Musketeers
**When to use**: For version 1.0 while the product still needs discovery.
**How**: Start with a developer, designer, and sweeper. If three people cannot build version one, change the people or slim the version.
**Trade-offs**: Fewer hands limit scope, but they reduce communication paths and force early trade-offs. (Ch 12)

## Start With No and the Fight Club Test
**When to use**: For every new customer or team feature request.
**How**: Say “not now.” Let the request stand on the porch for three days. Reconsider only when it returns, fits the vision, and proves value.
**Trade-offs**: Some useful requests wait or receive a no, but the product avoids automatic feature permanence and scope growth. (Ch 23)

## Feature Loop Review
**When to use**: After a request survives the first no decision.
**How**: Map related fields, screens, workflows, integrations, tests, help, tours, marketing, pricing, terms, and post-launch risk. Make the feature earn a second yes.
**Trade-offs**: Review takes time before implementation, but it exposes the iceberg behind a “simple” screen. (Ch 24)

## Behavior Test
**When to use**: When a detail, precision level, or option seems attractive.
**How**: Ask, “If this value changes, will the user act differently?” If no, use the sufficient result and say, “It just doesn’t matter.”
**Trade-offs**: The product may omit familiar polish, but it saves software, support, processing, and learning cost. (Ch 22)

## Interface First and Epicenter Design
**When to use**: At the start of a screen, feature, or application.
**How**: Move from paper to HTML to code. Identify the page’s cannot-live-without unit. Complete it before navigation, sidebars, footers, colors, or logos.
**Trade-offs**: Early screens may change often, but change stays cheap and the interface sets scope and budget. (Ch 31, Ch 46, Ch 47)

## Three State Solution
**When to use**: For every screen that shows data or depends on a successful action.
**How**: Design the regular, blank, and error states. Give each state clear meaning and a next action.
**Trade-offs**: It adds design work early, but prevents first-run confusion and error abandonment. (Ch 48)

## One-Page Story and Artifact Test
**When to use**: When a team wants a detailed functional specification.
**How**: Write one plain-language page in one day. Then make paper sketches, HTML, or a live prototype. Keep a document only when it becomes a real artifact.
**Trade-offs**: The team gives up early certainty, but it gains information before making expensive decisions. (Ch 59, Ch 60)

## Real Words
**When to use**: As soon as a screen, form, table, or message needs content.
**How**: Use real names, labels, passwords, messages, and relevant data. Follow the customer’s full entry path.
**Trade-offs**: Real content can slow a mockup, but it exposes field length, effort, table behavior, and missing guidance. (Ch 62)

## Test in the Wild
**When to use**: When a feature needs evidence about behavior, errors, or workflow fit.
**How**: Place the beta feature inside the real application. Use real data and a select group. Collect reports and improve the feature.
**Trade-offs**: Early users see flaws, but the team learns more than it would from a lab-only walkthrough. (Ch 34)

## Hollywood Launch
**When to use**: When a product needs an audience before public release.
**How**: Use a teaser months ahead, a preview weeks ahead, and a launch to a permission list. Invite a small beta group and allow honest feedback.
**Trade-offs**: Early attention creates a delivery obligation, but it gives the launch momentum and a ready audience. (Ch 68)

## Easy On, Easy Off
**When to use**: For signup, trial, billing, cancellation, and data export.
**How**: Keep signup short. Offer a credit-card-free trial. Make cancellation visible. Export customer-created data in a useful format.
**Trade-offs**: Customers can leave easily, but staying becomes stronger evidence that the product earns value. (Ch 65)

## Feel the Pain and Answer Quick
**When to use**: When builders and customer support have become separate.
**How**: Have builders answer real support messages. Learn the reason behind requests. Acknowledge messages quickly, even when the repair needs more time.
**Trade-offs**: Support uses builder time, but direct contact improves empathy, product decisions, and trust. The source example answered 90% of requests within 90 minutes. (Ch 77, Ch 79)

## Impact-Based Bug Prioritization
**When to use**: Whenever a bug competes with another repair or feature.
**How**: Ask how many people the bug affects and how bad the result is. Fix data-destroying failures immediately. Table minor visual annoyances when higher-impact work wins.
**Trade-offs**: Some customers wait for a repair, but the team creates the greatest benefit for the greatest number. (Ch 86)

## Work-Removal Ladder
**When to use**: Before replacing a role or adding headcount.
**How**: Remove the work. Change the practice. Try a small software slice. Hire only when a specific pain remains. Test a candidate with about 20 or 40 hours when possible.
**Trade-offs**: Growth stays slower, but the team avoids training headaches, communication cost, and unnecessary roles. (Ch 40, Ch 41)

## Alone Time and Rare Meetings
**When to use**: When communication fragments focused work.
**How**: Protect a contiguous half-day, such as 10 a.m. to 2 p.m. Hold a meeting only for an important issue needing input, approval, or agreement. Set a 30-minute timer and invite few people.
**Trade-offs**: Some replies wait, but uninterrupted work protects the zone and reduces meeting toxicity. (Ch 37, Ch 38)

## Manage Code and Design Debt
**When to use**: When a shortcut helps the team get real quickly.
**How**: Name the shortcut as debt. Reserve regular time to pay the principal through cleanup or redesign. Do not pay only interest through repeated fixes.
**Trade-offs**: Cleanup competes with new work, but unpaid debt makes later change slower and more expensive. (Ch 57)

## Open Doors
**When to use**: When customers need to read, move, monitor, or reuse their data.
**How**: Provide RSS, APIs, widgets, or other access points. Let outside developers extend the core product.
**Trade-offs**: Data can leave the main interface, but portability creates convenience, extensions, and a boomerang of new value. (Ch 58)
