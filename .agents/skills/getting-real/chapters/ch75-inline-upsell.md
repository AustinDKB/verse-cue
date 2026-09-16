# Chapter 75: Inline Upsell

## Core Idea
Promotion should continue inside the application. When a free account or lower pricing tier blocks an action, explain the barrier at the moment it appears and show how an upgrade removes it. The message should connect the unavailable capability to a clear reason to pay.

Existing customers already know and use the product, so they offer the strongest opportunity for repeat business and upgrades. A contextual offer reaches them when the product has made the need visible.

## Frameworks Introduced
- **Inline Upsell — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Present an upgrade opportunity inside the product when a plan limit prevents an action.
  - **When to use**: Use it when the application has a free version, tiered pricing, or a higher account level with more capability.
  - **How**: Detect the blocked action. Explain why the action is unavailable on the current plan. Tell the customer that an upgrade removes the barrier. Explain why the higher plan is useful.
- **Contextual Upgrade — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Offer a higher plan at the point where the customer reaches its current limit.
  - **When to use**: Use it when an existing customer maxes out the current account or needs a restricted capability.
  - **How**: Connect the offer to the customer’s immediate task. Make the value of the next level clear instead of sending the customer to a general marketing message.
- **Existing-Customer Sales — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Seek repeat business from people who already understand the product.
  - **When to use**: Use it when current customers can gain more value from a paid version or higher level.
  - **How**: Explain the added capability without being shy about the sales opportunity. Respect the customer’s existing knowledge and use.

## Key Concepts
- **Inline upsell**: An upgrade message shown inside the application.
- **Upgrade opportunity**: A point where a customer can pay for more capability.
- **Tiered pricing**: Pricing levels that provide different product limits.
- **Free account**: An account that uses the product without payment and with defined limits.
- **Barrier**: The plan restriction that prevents an action.
- **Current plan**: The account level the customer uses now.
- **Higher level account**: A paid tier with more capability.
- **Existing customer**: A person who already knows and uses the product.

## Mental Models
- **Barrier-to-path**: A blocked action should point to the path that removes the block.
- **Contextual offer**: The best upgrade message appears when the customer understands the need.
- **Earned upgrade**: The product proves value first, then the customer meets a limit worth paying to remove.
- **Known-user leverage**: Existing customers need less product explanation than new prospects.

## Anti-patterns
- **Dead-end refusal**: Blocking an action without explaining the reason leaves the customer frustrated and without a next step.
- **Generic upsell**: Sending every customer to a broad sales page ignores the task that created the upgrade need.
- **Hidden limit**: Failing to state the current plan’s boundary makes the product feel arbitrary.
- **Timid sales path**: Avoiding a clear upgrade invitation loses a useful opportunity with a customer who already knows the product.
- **Wrong-time offer**: Showing an upgrade unrelated to the customer’s current task weakens trust and relevance.

## Worked Example
In Basecamp, a free account cannot upload files. When a customer tries to upload one, the application does not simply reject the action. It explains why file uploading is unavailable, encourages an upgrade to the paid version, and explains why that upgrade is useful. The same approach applies when a customer reaches the limit of a current plan and needs the next level.

## Key Takeaways
1. Continue promotion inside the product.
2. Explain a plan limit when the customer meets it.
3. Connect the blocked action to the upgrade that removes the barrier.
4. Show why the higher plan is useful.
5. Treat existing customers as the strongest source of repeat sales.

## Connects To
- **Chapter 64, Free Samples**: Uses a free product path to demonstrate value before payment.
- **Chapter 65, Easy On, Easy Off**: Keeps the product path simple and clear.
- **Chapter 69, A Powerful Promo Site**: Extends public promotion into the application itself.
- **Chapter 68, Hollywood Launch**: Converts early product use into a later paid path.
