# Chapter 53: One Interface

## Core Idea
Put administrative actions inside the regular application interface. Separate admin screens usually receive less design care, force the team to maintain two interfaces, and make customers switch applications for tasks that belong together.

## Frameworks Introduced
- **One Interface — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Make the application the place where regular and administrative work happens.
  - **When to use**: Use it when a product needs functions such as editing, adding, deleting, or changing preferences and people.
  - **How**: Add those functions to the regular application screens. Let authorized people manage content in the same context that customers use. Avoid a second set of screens unless the task truly needs a separate product.
- **No Separate Interface — Edward Knittel, Director of Sales and Marketing at KennelSource**: Keep management work in the application instead of sending people to a separate admin product.
  - **When to use**: Use it when one person must switch between customer work and management work during the same session.
  - **How**: Make the management area show the same application and customer context. Let the person adapt to one interface instead of learning and maintaining two.

## Key Concepts
- **One interface**: A shared application surface for regular and administrative work.
- **Admin function**: An action that manages preferences, people, or application content.
- **Public-facing interface**: The screens that customers use for their main work.
- **Separate admin screen**: An extra screen set built only for management tasks.
- **Interface tax**: The repeated design and maintenance cost of a second interface.
- **Customer context**: The application view that shows what a customer sees.
- **Management area**: The part of the application where authorized changes occur.
- **Context switching**: Moving between applications to complete related work.

## Mental Models
- **Application is everything**: If a value can change, the main application should provide the path to change it.
- **One-tax model**: One interface concentrates design, testing, and maintenance effort in one place.
- **Customer-eye model**: Let support and sales see the same screens that customers see so they can understand problems directly.
- **In-place management**: Perform a management action where the related work already occurs.

## Anti-patterns
- **Separate admin product**: A second product gets less attention and tends to look and feel worse than the public interface.
- **Dual-interface maintenance**: Repeating screens and behavior doubles the work and increases the chance of sloppy changes.
- **Forced context switching**: Making a person log into another application interrupts related work and adds friction.
- **Admin-only assumptions**: Designing management screens without the customer context makes support questions harder to understand.

## Worked Example
KennelSource lets a person manage client appointments and then add a new employee without leaving the application. The person does not log into a separate admin interface. Sales and support can also view the same application that customers use, which helps them understand a problem and guide the customer through it. One interface supports both the main task and the needed management action.

## Key Takeaways
1. Put edit, add, delete, and preference actions in the regular application.
2. Avoid a second interface when the work belongs in the same context.
3. Count the design and maintenance tax before creating admin screens.
4. Let support staff see what customers see.
5. Reduce application switching for people with mixed responsibilities.

## Connects To
- **Chapter 20, Make Opinionated Software**: Chooses one clear product direction instead of multiplying interfaces.
- **Chapter 46, Interface First**: Designs management actions as part of the real interface.
- **Chapter 51, Context Over Consistency**: Keeps only the controls that fit the current management task.
- **Chapter 52, Copywriting is Interface Design**: Makes admin actions clear through customer-facing language.
