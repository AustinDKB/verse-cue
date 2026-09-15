# Chapter 58: Open Doors

## Core Idea
Let customers get their data when they want it and in the form they need. RSS feeds and APIs make an application more useful, let third-party developers extend it, and create a boomerang effect that can bring more value back to the product.

## Frameworks Introduced
- **Open Doors — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Do not lock customers into one application screen or access method.
  - **When to use**: Use it when customers need to read, monitor, move, or reuse information outside the application.
  - **How**: Expose data through RSS feeds, APIs, and other useful access points. Let people choose when and how they use it.
- **Data Runs Free — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: Treat data access as a customer benefit instead of a threat.
  - **When to use**: Use it when the team considers restriction to increase lock-in.
  - **How**: Let feeds and APIs carry information into tools, readers, and services that customers already use.
- **Third-Party Extension — Jason Fried, David Heinemeier Hansson, and Matthew Linderman**: An API lets other developers build valuable products around the application.
  - **When to use**: Use it when outside developers can solve access or workflow needs the core team cannot cover.
  - **How**: Provide an API that lets developers read or change permitted data, then support add-ons without building every use case.
- **Widget Access Point — Todd Dominey, founder of Dominey Design, from *Trying on Backpack***: A small tool can make an application useful when an idea occurs.
  - **When to use**: Use it when customers need to capture or change information without opening the full application.
  - **How**: Connect the widget to the web application so input stays available across devices without local version control or synchronization.

## Key Concepts
- **Data portability**: The ability to get and use information outside the main application.
- **Lock-in**: A condition that makes customers stay because data access is difficult.
- **RSS feed**: A stream that lets a customer follow changing content in a reader.
- **API**: An access method that lets another product work with application data.
- **Third-party developer**: An outside builder who creates a product that uses the application.
- **Add-on**: An extra product or tool that extends the main application.
- **Mashup**: A service that combines data from different sources.
- **Commercial API**: An API that lets another business create services for customers.
- **Widget**: A small tool that gives fast access to a web application.

## Mental Models
- **Open-door model**: Give customers more entrances to their data instead of one required screen.
- **Boomerang effect**: Data that leaves the application can create uses that increase its value.
- **Extension network**: An API turns outside developers into sources of products the core team did not plan.
- **Immediate brain dump**: Make capture fast, then let the web application preserve access later.

## Anti-patterns
- **Data lock-in**: Restricting information to the main screen reduces customer choice and convenience.
- **Login-only access**: Requiring repeated visits makes changing content harder to follow.
- **Closed extension path**: Blocking APIs prevents outside developers from making useful add-ons.
- **Local sync burden**: Separate local versions create version-control and synchronization concerns.

## Worked Example
Backpack supplied an API that Chipt Productions used to build a Mac OS X Dashboard widget. The widget let a person add and edit reminders and list items from the desktop. Todd Dominey described using it whenever an idea arrived: open the widget, type, and submit. Web-based data avoided local versions and synchronization. Basecamp feeds also let customers follow project messages, to-do lists, and milestones without repeated logins. The same open-door pattern appears in Google Maps apartment-listing mashups, del.icio.us linkrolls, and Stewart Butterfield’s Flickr commercial APIs for photo books, posters, DVD backups, and stamps.

## Key Takeaways
1. Give customers access to data outside the main screen.
2. Use RSS to follow changing content without repeated logins.
3. Offer APIs when outside developers can extend the product.
4. Treat open data as a source of convenience and new value.
5. Use widgets or other access points for fast input.

## Connects To
- **Chapter 18, Hire the Right Customers**: Builds trust with customers who value control of information.
- **Chapter 20, Make Opinionated Software**: Keeps the core focused while APIs support varied extensions.
- **Chapter 54, Less Software**: Lets outside builders solve uses without adding every feature to the core.
- **Chapter 55, Optimize for Happiness**: Gives people tools that make daily work faster and more pleasant.
