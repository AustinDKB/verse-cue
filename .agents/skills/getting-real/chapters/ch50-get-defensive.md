# Chapter 50: Get Defensive

## Core Idea
Things will go wrong online, even when the team designs carefully and tests often. Use defensive design to find trouble spots, reduce confusion during failure, and keep customers from feeling abandoned when the normal path breaks.

## Frameworks Introduced
- **Defensive design — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Design for breakdowns as deliberately as for normal use.
  - **When to use**: Use it during interface design, testing, and review of error screens or other crisis points.
  - **How**: Search for conditions that cause confusion or frustration, then give customers a clear and useful response when those conditions occur.
- **Defensive driving — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Treat trouble spots as expected risks, like slick roads or reckless drivers.
  - **When to use**: Use it when a team feels safe because the regular path works well.
  - **How**: Look ahead for dangerous scenarios instead of waiting for customers to discover them.

## Key Concepts
- **Defensive design**: Interface work that prepares for errors and crisis points.
- **Trouble spot**: A condition that can cause customer confusion or frustration.
- **Breakdown**: A failure that prevents the expected path from working.
- **Crisis point**: A moment when a customer needs help because normal use has stopped.
- **Error screen**: The interface shown when a problem interrupts the application.
- **Customer abandonment**: Leaving a person without useful help during failure.
- **Regular path**: The expected flow when the application works correctly.

## Mental Models
- **Ninety-percent warning**: A product that works well most of the time can still lose trust during the remaining failures.
- **Look-ahead scan**: Search for likely trouble before customers meet it.
- **Help at the crisis point**: Give the most care when the customer has the least control.

## Anti-patterns
- **Happy-path design**: Designing only successful use leaves customers exposed when conditions change.
- **Testing-only defense**: Tests can find problems, but they do not replace a useful customer response.
- **Error abandonment**: A silent or confusing error makes a failure memorable and damages trust.
- **Ninety-percent comfort**: Good normal performance does not excuse poor help during the other ten percent.

## Worked Example
An application may work well for 90 percent of visits, but a customer can still meet a failed action or confusing screen. A defensive team lists those trouble spots before release and designs the error response at each crisis point. When the breakdown occurs, the customer receives guidance instead of an empty failure screen.

## Key Takeaways
1. Expect online failures as part of product work.
2. Search for trouble spots before customers report them.
3. Design error screens as carefully as regular screens.
4. Give customers useful help at crisis points.
5. Do not measure customer care only by regular-path success.

## Connects To
- **Chapter 48, Three State Solution**: Makes the error state a required design target.
- **Chapter 49, The Blank Slate**: Prevents first-run confusion before a failure occurs.
- **Chapter 34, Test in the Wild**: Uses real customer behavior to find trouble spots.
