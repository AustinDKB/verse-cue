# Chapter 32: Avoid Preferences

## Core Idea
Decide small details for customers when the product can make a sound default choice. Preferences often transfer product responsibility to customers, add code and test paths, and create interface complexity with little value.

## Frameworks Introduced
- **Avoid preferences — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Use product judgment instead of exposing every small decision as an option.
  - **When to use**: Use it when the team considers a setting for page size, sorting, dashboard content, or another minor detail.
  - **How**: Choose the best default, make the product work that way, and adjust later when customer feedback shows that the decision fails. Do not create a preference only to avoid making the call.
- **Make simple decisions on behalf of customers — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Remove decision work from the customer.
  - **When to use**: Use it when several options appear reasonable but no option has a broad and important benefit.
  - **How**: Select one clear behavior and expose no setting. Treat complaints as useful evidence that can guide a later change.
- **Good defaults that Just Work — Havoc Pennington**: Prefer disciplined defaults over lazy option growth.
  - **When to use**: Use it when a preference seems easier than selecting and defending a default.
  - **How**: Judge each preference by its benefit against its code, design, testing, and permutation cost. Keep the preference only when its interface value justifies that cost.

## Key Concepts
- **Preference**: A customer-controlled option for product behavior.
- **Default**: The product choice that applies without customer action.
- **Decision burden**: Thought and work transferred to the customer.
- **Preference permutation**: A combination of options that creates another behavior path.
- **Testing cost**: Work required to check each option and combination.
- **Interface cost**: Extra screens and controls needed to expose settings.
- **Good default**: A chosen behavior that works for most customers without setup.
- **Crucial interface feature**: A preference whose benefit justifies its full cost.

## Mental Models
- **Preference as a bill**: Every option creates code, design, test, and support work.
- **Default as service**: A clear choice helps customers avoid needless decisions.
- **Option tree**: Each new setting adds paths that can hide layout and pagination bugs.
- **Complaint as correction**: A bad default can change after users provide evidence.

## Anti-patterns
- **Preference escape**: Add an option because the team does not want to make a difficult decision.
- **Endless settings**: Turn every minor product detail into customer work.
- **Permutation blindness**: Test one option while missing failures caused by combinations.
- **Invisible-path testing**: Ignore layouts, tables, and pagination that appear only under rare settings.
- **Default avoidance**: Refuse to choose even when one behavior works for most people.

## Worked Example
Basecamp chose 25 messages per page. Its overview showed the last 25 items, messages appeared in reverse chronological order, and the dashboard showed the five most recent projects. Customers did not receive settings for 25, 50, or 100 messages. The team made clear calls, then kept the ability to adjust when evidence showed a problem. This approach avoided extra controls, tests, and preference combinations.

## Key Takeaways
1. Choose a clear default for minor product details.
2. Do not transfer a product decision to customers without strong value.
3. Count code, design, testing, and permutation cost for each option.
4. Treat customer complaints as evidence for changing a default.
5. Keep a preference only when its benefit makes it a crucial interface feature.

## Connects To
- **Chapter 26, Human Solutions**: Gives users room to adapt without adding formal controls.
- **Chapter 28, Hold the Mayo**: Encourages removal of options that create burden.
- **Chapter 30, Rinse and Repeat**: Allows a default to change after real use and feedback.
