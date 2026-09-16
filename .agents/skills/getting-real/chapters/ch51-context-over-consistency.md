# Chapter 51: Context Over Consistency

## Core Idea
An interface should give each page the controls and information that help a person take the next step. Consistency helps only when it serves that context. A page can break a site-wide pattern when the change makes the page clearer and more useful.

## Frameworks Introduced
- **Context Over Consistency — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Prefer a page’s immediate need over a rule that repeats the same elements everywhere.
  - **When to use**: Use it when choosing controls, layouts, navigation, search, footers, or other repeated elements.
  - **How**: Ask what the person must do on this page. Choose a button or link based on the action. Choose a list or grid based on where a calendar appears and the length of the period. Keep only elements that help the next step.
- **Intelligent Inconsistency — Mark Hurst, founder of Creative Good and creator of Goovite.com, from *The Page Paradigm***: Deliberately vary each page so it supplies exactly what the person needs at that point in the process.
  - **When to use**: Use it in a web process where each page has a different task or decision.
  - **How**: Review each page on its own. Remove navigation, search, footer, or other elements that do not support the current task. Keep the page focused on quick and easy progress.

## Key Concepts
- **Context**: The page situation that determines which controls and information matter now.
- **Consistency**: Repeating the same interface pattern across pages.
- **Intelligent inconsistency**: A deliberate change that gives a page the right content for its current task.
- **Page process**: The sequence of pages through which a person completes a task.
- **Next step**: The immediate action that moves a person forward.
- **Superfluous navigation**: A navigation element that adds no value to the current page.
- **Global search**: A search control repeated across the site whether or not each page needs it.
- **Interface rule**: A repeated design choice that may need to yield to page context.

## Mental Models
- **Context test**: Ask, “What does this person need here?” before asking whether another page looks the same.
- **Right over consistent**: Prefer the choice that makes the task clearer, even when it breaks a visual pattern.
- **Page-by-page lens**: Judge a web interface one page at a time, not only as one uniform system.
- **Removal test**: Hide a repeated element and check whether the person loses a needed next step.

## Anti-patterns
- **Consistency dogma**: Applying one interface rule everywhere makes some pages carry controls they do not need.
- **Global-everything design**: Repeating navigation, search, and footers adds noise and slows the current task.
- **Control-by-convention**: Choosing a button or link because of a general rule ignores the action that the control performs.
- **Uniform calendar layout**: Using one list or grid form for every time period can make the calendar harder to read.

## Worked Example
A team reviews a calendar and several process pages. It uses a list for a short period and a grid for a longer period because each form fits its setting. It keeps the action control that helps the current page, but removes global navigation, search, or a footer when those elements do not help the next step. The result is intentionally inconsistent, but each page is easier to use.

## Key Takeaways
1. Judge each page by the person’s immediate task.
2. Choose buttons, links, lists, and grids from their context.
3. Remove repeated elements that do not help the next step.
4. Treat intelligent inconsistency as a design tool, not a defect.
5. Prefer a clear page over a uniform page.

## Connects To
- **Chapter 20, Make Opinionated Software**: Makes clear choices instead of adding every possible option.
- **Chapter 46, Interface First**: Uses visible screens to test whether a design makes sense.
- **Chapter 47, Epicenter Design**: Keeps the page’s essential content ahead of supporting elements.
- **Chapter 48, Three State Solution**: Applies context checks to regular, blank, and error states.
