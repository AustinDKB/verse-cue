# Chapter 78: Zero Training

## Core Idea
Build a product that needs no manual or training. Yahoo, Google, and Amazon do not need manuals for ordinary use. Simplicity reduces the number of places where customers need help, while inline help and FAQs prevent support problems at the point of confusion.

The goal is not to hide a manual better. The goal is to remove enough complexity that customers can use the product without one. Add help only where a known problem can stop a customer from completing an action.

## Frameworks Introduced
- **Zero Training — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Design the product so that customers can learn it through use.
  - **When to use**: Use it when a product needs a manual, training session, or repeated explanation for ordinary tasks.
  - **How**: Keep the application simple. Remove unnecessary complexity. Make the remaining actions clear enough that customers can proceed without outside instruction.
- **Inline Help at the Confusion Point — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Put a short help link or explanation beside the action that causes confusion.
  - **When to use**: Use it when support requests cluster around one screen or one product action.
  - **How**: Find the exact point where customers become stuck. Place the relevant help next to that point. Do not force the customer to search a general manual.
- **Preemptive FAQ — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Answer a predictable support question before it becomes a support request.
  - **When to use**: Use it when a known technical condition produces repeated customer messages.
  - **How**: State the symptom and the specific action that fixes it. Link the FAQ beside the related control.

## Key Concepts
- **Zero training**: A product-use goal in which customers do not need formal instruction.
- **Simplicity**: A reduction in product complexity that reduces the need for help.
- **Inline help**: Guidance placed beside the action that may confuse a customer.
- **FAQ**: A focused answer to a question that customers ask repeatedly.
- **Confusion point**: The screen or action where a customer is likely to stop or ask for help.
- **Preemptive support**: Help that prevents a support request before it reaches the team.
- **Browser cache**: Stored browser data that can make an old image appear after an upload.
- **Force reload**: A browser action that fetches the current image instead of the stored one.

## Mental Models
- **Complexity creates support**: Every unnecessary product step can create another explanation, question, or manual page.
- **Help belongs at the decision**: A customer needs guidance where the problem occurs, not several screens away.
- **Repeated questions are design evidence**: A support pattern can identify a missing product explanation.
- **One small link can remove a queue**: A precise FAQ can prevent many individual support messages.

## Anti-patterns
- **Manual-first design**: Requiring a manual before ordinary use shifts product complexity onto the customer.
- **Generic help center**: Sending a confused customer to broad documentation makes the customer find the answer alone.
- **Late support**: Waiting for repeated emails before adding known guidance leaves a preventable problem in place.
- **Incomplete symptom repair**: Fixing the upload action while ignoring the browser-cache symptom leaves customers seeing the old logo.

## Worked Example
Basecamp customers uploaded a new logo but sometimes continued to see the old logo because of browser caching. The team placed an FAQ link beside the logo submission area. The FAQ told customers to force-reload the browser so the new logo appeared. Before the inline FAQ, the team received about five emails each day about the problem. Afterward, those emails stopped.

## Key Takeaways
1. Aim for zero training through simpler product design.
2. Treat repeated support questions as evidence of a product or help gap.
3. Place guidance beside the action that causes confusion.
4. Write FAQs that give a specific repair, not general advice.
5. Use one precise inline explanation to prevent a larger support queue.

## Connects To
- **Chapter 4, Build Less**: Less product complexity reduces the need for training and support.
- **Chapter 77, Feel The Pain**: Direct support contact reveals where inline help can prevent frustration.
- **Chapter 79, Answer Quick**: Preemptive help reduces the number of questions that need a fast reply.
- **Chapter 26, Human Solutions**: A focused human explanation can solve a problem without adding software.
