# Chapter 52: Copywriting is Interface Design

## Core Idea
Every word in an interface affects what a person understands and does. Button labels, field examples, status messages, instructions, and policy explanations are design elements, so write them for the reader with short, clear language.

## Frameworks Introduced
- **Copywriting Is Interface Design — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Treat every word beside a control or content area as part of the interface.
  - **When to use**: Use it whenever you design a button, label, form, status message, instruction, or policy explanation.
  - **How**: Put yourself in the reader’s position. Decide what the reader needs to know. Explain it clearly and briefly. Test the exact words, not only the surrounding pixels.
- **Audience Language — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Speak in the terms that customers understand instead of using internal or technical language.
  - **When to use**: Use it when the team writes labels, examples, instructions, or messages for people outside the development team.
  - **How**: Remove acronyms, internal lingo, and engineer-to-engineer language. Select words that describe the customer’s action and result.
- **Every Letter Matters — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Small wording choices can change clarity and behavior.
  - **When to use**: Use it during interface review, even when the layout and visual style already look complete.
  - **How**: Compare alternative labels, sentence lengths, examples, capitalization, numbers, and status terms. Keep the shortest wording that remains clear.

## Key Concepts
- **Interface copy**: Words that explain, label, or guide an interface.
- **Button label**: Text that tells a person what a control will do.
- **Field example**: Text that shows the kind of value a person should enter.
- **Status message**: Text that reports a change or current condition.
- **Audience language**: Words that match the customer’s knowledge and vocabulary.
- **Internal lingo**: Team language that customers may not understand.
- **Acronym**: A shortened term that can hide meaning from the reader.
- **Clarity**: The quality that lets a person understand the next action quickly.

## Mental Models
- **Words as controls**: Treat a label as part of the control’s function, not as decoration around it.
- **Reader’s shoes**: Read the screen as a customer who does not know the team’s internal terms.
- **Shortest clear path**: Remove words until the message is brief, but stop before meaning becomes uncertain.
- **Pixel-and-letter review**: Review wording with the same care given to icons, typefaces, and layout.

## Anti-patterns
- **Vague control labels**: Labels such as “Submit” hide the result and make the next action harder to predict.
- **Technical language**: Jargon, acronyms, and internal lingo force customers to translate the interface.
- **Word-count neglect**: Adding sentences without checking their value makes instructions slower to read.
- **Icon-only design**: An icon without a useful name can leave the customer unsure of its meaning.
- **Engineer-to-engineer voice**: Writing for the team instead of the audience makes a customer-facing interface feel foreign.

## Worked Example
A team reviews a form and compares labels such as “Submit,” “Save,” “Update,” “New,” and “Create.” It chooses the word that describes the result of the current action. It also compares “New,” “Updated,” “Recently Updated,” and “Modified,” plus “There are 5 new messages,” “There are new messages: 5,” and “5.” The team keeps the shortest version that still tells the audience what the number means. The same review checks field examples, step instructions, icon names, and refund-policy text.

## Key Takeaways
1. Treat every interface word as a design decision.
2. Write from the reader’s point of view.
3. Use customer language instead of jargon or internal lingo.
4. Label controls by their real result.
5. Keep messages short without removing needed meaning.
6. Review words with the same care as visual elements.

## Connects To
- **Chapter 20, Make Opinionated Software**: Makes clear choices instead of hiding behind generic controls.
- **Chapter 46, Interface First**: Uses real screens to review the complete customer experience.
- **Chapter 49, The Blank Slate**: Uses clear words to guide a person through the first-run state.
- **Chapter 51, Context Over Consistency**: Chooses words and controls that fit the current page.
