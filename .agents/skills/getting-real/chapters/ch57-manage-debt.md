# Chapter 57: Manage Debt

## Core Idea
Code and design can create bills even when they do not involve money. A quick hack or good-enough page can help the team get real quickly, but the team must name that work as debt and reserve time to repay it.

## Frameworks Introduced
- **Manage Code and Design Debt — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Accept a temporary shortcut when it helps the product move, then plan the cleanup that makes the shortcut sound.
  - **When to use**: Use it when speed matters and a functional solution needs hairy code or a design that is only good enough.
  - **How**: Record the shortcut as debt. Put aside regular time to clean the code or redesign the page. Do not let temporary work become the permanent system.
- **Principal and Interest Model — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Cleanup pays the principal, while repeated fixes pay interest.
  - **When to use**: Use it when the team must choose between moving forward and repairing an earlier shortcut.
  - **How**: Schedule work that removes the underlying hack. Otherwise, spend future time repairing the same problem without improving the system.

## Key Concepts
- **Code debt**: A shortcut in code that creates future cleanup work.
- **Design debt**: A temporary or weak design that needs later improvement.
- **Shortcut**: A fast solution accepted to move the product forward.
- **Hairy code**: Functional code that is difficult to understand or change.
- **Good-enough design**: A usable design that still needs refinement.
- **Principal**: The underlying debt that cleanup removes.
- **Interest**: Repeated repair work caused by unpaid debt.
- **Debt payment**: Planned time spent cleaning code or improving design.

## Mental Models
- **Financial debt analogy**: A shortcut can help now but creates a future bill.
- **Principal-versus-interest test**: Choose cleanup that removes the cause instead of another repair that treats the symptom.
- **Regular-payment rule**: Reserve time for debt payment before new work consumes all available time.
- **Get-Real trade-off**: Speed can justify a shortcut only when the team also protects later cleanup.

## Anti-patterns
- **Shortcut denial**: Calling a hack complete hides the future work it creates.
- **Permanent temporary work**: Leaving hairy code or a so-so page in place increases later repair cost.
- **Interest-only repair**: Fixing each symptom without cleaning the underlying code spends time without paying down debt.
- **No payment plan**: Starting new work without reserved cleanup time lets debt grow unnoticed.

## Worked Example
A team ships a functional feature with code that feels hairy and a page that is only good enough. That choice helps the team get real quickly, so it records both items as debt. During later cycles, it reserves time to clean the code and redesign the page. The team then pays the principal instead of repeatedly fixing the same hack.

## Key Takeaways
1. Name shortcuts as code or design debt.
2. Use a shortcut only when it helps the product move.
3. Reserve regular time to repay the debt.
4. Clean the cause instead of paying interest through repeated fixes.
5. Do not let good-enough work become permanent by accident.

## Connects To
- **Chapter 29, Race to Running Software**: Explains why a fast first release can include temporary shortcuts.
- **Chapter 54, Less Software**: Reduces the amount of code that can create future debt.
- **Chapter 56, Code Speaks**: Treats technical difficulty as a signal that cleanup may be due.
- **Chapter 59, There’s Nothing Functional about a Functional Spec**: Keeps change possible while real work reveals what needs improvement.
