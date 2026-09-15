# Chapter 48: Three State Solution

## Core Idea
Design every screen for three conditions: regular use with data, first use without data, and failure. A complete interface plans for the customer’s normal path and for the two states that often cause confusion.

## Frameworks Introduced
- **Three State Solution — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Treat regular, blank, and error screens as separate design work.
  - **When to use**: Use it for every screen that displays data or depends on a successful action.
  - **How**: Design the data-filled view, the first-run view before data exists, and the failure view when something goes wrong.
- **State-complete design — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Judge a screen by all conditions a customer will meet.
  - **When to use**: Use it before implementation and during interface review.
  - **How**: Check each state for clear meaning and useful next action instead of reviewing only the regular state.

## Key Concepts
- **Regular state**: The screen shown when the application works and contains data.
- **Blank state**: The screen shown before a customer enters data.
- **Error state**: The screen shown after a problem or failed action.
- **First-run view**: The initial screen that sets customer expectations.
- **Data-filled view**: The normal screen that shows the application in active use.
- **Failure view**: The recovery point that appears when the normal path breaks.

## Mental Models
- **Three-condition check**: Ask what the customer sees when the screen is full, empty, and broken.
- **State parity**: Give blank and error states design attention equal to their effect on the customer.
- **Expectation before volume**: Plan the first view before test data hides the real customer experience.

## Anti-patterns
- **Regular-only design**: A full data view hides the confusion that new and blocked customers face.
- **Blank-state neglect**: An empty screen gives no direction when a customer needs it most.
- **Error abandonment**: A failure screen that offers no useful path leaves the customer alone.

## Worked Example
For a record list, design three versions before coding. The regular version shows records. The blank version explains what the list is and what a new customer should do. The error version explains that the normal action failed and gives a useful next step. The screen is not complete until all three conditions have a clear purpose.

## Key Takeaways
1. Design regular, blank, and error states for every screen.
2. Review empty and failed states before implementation.
3. Give each state a clear meaning and next action.
4. Do not let test data hide the first-run experience.

## Connects To
- **Chapter 46, Interface First**: Designs all screen states before expensive programming.
- **Chapter 47, Epicenter Design**: Finds the essential content in each state before adding extras.
- **Chapter 49, The Blank Slate**: Expands the blank state into a useful first-run experience.
- **Chapter 50, Get Defensive**: Applies defensive design to error states and crisis points.
