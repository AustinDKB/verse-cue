---
name: data-panels
description: Define, design, and implement reusable data panels with clear data views, states, placement, and responsive behavior.
---

# Data Panels

Use this skill when a page shows one or more related data sets in bounded visual surfaces.

## Core rule

The component name describes its function, not its current page position.

Use `DataPanel` for the reusable surface.

Use `right rail` or `right sidebar` only for the current layout position.

Use `card` only when the visual treatment matters.

## Component terms

| Term | Use | Do not use it for |
|---|---|---|
| `DataPanel` | A surface with a heading, context, state, and data view | A page column or layout region |
| `DataTable` | Data with fixed columns and row values | A label and value pair |
| `DataList` | Items with one label and one value | A multi-column table |
| `SeniorityTable` | The domain-specific seniority data view | A generic table shell |
| `PanelGrid` | A layout for multiple panels | A data source |
| `PanelStack` | A vertical group of panels | A panel component |
| `right rail` | A placement beside the main content | A component name |
| `contextual panel` | A panel that supports the main content | Every panel on the page |

For the current seniority view, use these terms:

- **Product term:** seniority list
- **Panel term:** seniority data panel
- **Table term:** seniority table
- **Placement term:** right rail when the profile uses two columns

Do not call the view a sublist.

## Panel anatomy

A data panel can contain these parts:

1. **Header**
   - Title
   - Optional description
   - Optional list selector
   - Optional action
2. **Body**
   - Data table or data list
3. **Status**
   - Loading state
   - Empty state
   - Error state
   - Permission state
4. **Footer**
   - Optional count, pagination, or secondary action

Keep the header and body stable when the selected data changes.

Keep data access and business rules outside the panel template.

## Standard visual contract

Use `<section class="card data-panel">` for the panel shell.

Use `card-header flex items-center justify-between gap-3` for the header.

Use `card-body space-y-3` for the panel body.

Use `data-panel-table` for the bounded table surface.

Use `members-table w-full` for profile data tables.

Use `text-label` for table headers and `text-body` for table values.

Use `data-panel-preview-rows="5"` for the five-row preview rule.

Use a table empty row with muted text when the panel has no records.

Keep action buttons in the header and use `btn-outline btn-sm` for secondary actions.

Use `data-panel-rail` on a right rail that contains one or more data panels.

Keep the primary panel sticky and stack supporting panels below it.

Stack the rail below the main column on narrow screens.

## Reuse boundary

Create a shared `DataPanel` shell only when two current call sites share the same behavior.

Keep a domain-specific partial when only one call site exists.

For the current seniority view, keep the domain partial at:

```text
templates/partials/worksites/seniority_card.html
templates/partials/worksites/seniority_table.html
```

Extract a shared shell only after another panel needs the same header, state, action, and body behavior.

Use this structure after that point:

```text
templates/partials/shared/data_panel.html
templates/partials/shared/data_table.html
templates/partials/worksites/seniority_table.html
```

Keep `SeniorityTable` responsible for seniority columns.

Keep `DataPanel` responsible for panel chrome and state presentation.

Do not make `DataPanel` decide the data scope, query the database, or apply authorization.

## Data view choice

Use `DataTable` when users compare values across fixed columns.

Use `DataList` when users read label and value pairs.

Use a table for these seniority fields:

- Rank
- Member
- Seniority date
- Hours

Keep the table compact when it supports a profile.

Do not hide a required column without a clear mobile rule.

## Preview and internal scroll

Show five data rows by default, plus the table header.

Keep extra rows inside the panel body with vertical scrolling.

Keep the panel height bounded so the page layout does not grow with row count.

Keep the table header visible while the body scrolls.

Use `data-panel-preview-rows="5"` when the markup needs to record the preview rule.

Do not make the full page scroll to reveal rows inside a data panel.

Keep horizontal scrolling inside the panel when narrow columns need more width.

## Multiple panels

Use `PanelGrid` when panels form columns.

Use `PanelStack` when panels form a vertical group.

Keep panel order based on user work, not database order.

Place the primary work data first.

Place supporting data in a secondary panel.

Use a stable panel title for each data type.

Do not name panels `LeftPanel`, `RightPanel`, or `BottomPanel`.

Use names such as `SeniorityPanel`, `WorksitesPanel`, or `DuesPanel` when a domain name improves clarity.

## Scoped profile lists

Do not show a list selector in a worksite or bargaining unit profile panel.

Resolve one list from the current profile scope.

Use the `WORKSITE` dimension and current `worksite_id` for a worksite profile.

Use the `UNIT` dimension and current bargaining unit for a unit with no worksites.

Filter rows by the current scope before the template renders them.

Use a list selector only in a list-management view where the user compares different list definitions.

Keep list selection inside page state when a selector is required.

Do not place list selection in the public address bar when the project rules exclude that state.

Show an empty state when the scope has no list or no rows.

## Placement and semantics

Use `<section>` when the panel forms part of the primary page content.

Use `<aside>` when the panel remains complementary to the main content.

Use a right rail when the panel sits beside the main profile content.

Let the same panel move to the main column on a narrow screen.

Do not change the component name when its placement changes.

## Project implementation

Follow the project route and service boundary:

1. Let the route receive the request and select the response type.
2. Let the service load scoped data and apply the soft-delete filter.
3. Let the route pass prepared context to the template.
4. Let the panel template render the shell.
5. Let the domain table partial render rows and columns.

Use existing URL helpers for member links.

Set member links to the public member URL.

Use the partial URL for an HTMX request when the page needs a partial response.

Set `hx-boost="false"` on partial links.

Target the required panel or page content according to the existing HTMX rules.

Use the existing preload system for hover fetches.

Put `data-preload-hover` on every GET navigation link inside the panel.

Do not use `htmx-ext-preload` or `preload="mouseover"`.

Do not add a second preload script.

Mark the panel with `data-posthog-panel` and a non-sensitive `data-posthog-scope` value.

Capture a `data_panel_viewed` event after the first render and after HTMX content swaps.

Capture a `data_panel_interaction` event for panel links and buttons.

Do not send member names, member IDs, or other private data in custom panel events.

## State rules

Every data panel needs a defined state for these cases:

- Data exists
- Data does not exist
- A selector has no options
- Data loads through HTMX
- The request fails
- The user lacks access

Use one clear message per state.

Keep empty states useful and short.

Do not show an empty table with no explanation.

Do not hide an error inside a blank panel.

## Responsive rules

Keep the panel readable at narrow widths.

Keep the most important column visible first.

Allow lower-priority columns to hide only when the design defines a replacement.

Keep member names readable.

Keep dates and hours aligned with their headers.

Let panels stack in priority order on narrow screens.

Do not force horizontal page scrolling for a compact profile panel.

## Accessibility rules

Give each panel a clear heading.

Use table headers for every data column.

Associate a selector label with its control.

Do not use color as the only state signal.

Keep keyboard focus visible.

Announce HTMX status changes when the update changes the user task.

Use buttons for actions and links for navigation.

## Review checklist

- Does the name describe the function instead of the position?
- Does the view use a table or a list that matches the data shape?
- Does the panel define empty, loading, error, and permission states?
- Does the panel work in a main column and a right rail?
- Does the panel keep data access outside the template?
- Does every panel GET link use the project preload system?
- Does PostHog capture panel views and interactions without private data?
- Does the panel follow the project URL and HTMX rules?
- Does a shared abstraction have at least two real call sites?
- Does the narrow layout preserve the most important data?
- Does each table have accessible headers?

## Recommended terms

Use `data panel`, `data table`, `seniority table`, `panel grid`, `panel stack`, `right rail`, and `contextual panel`.

Avoid `sublist`, `side list`, `left card`, `right card`, and `miscellaneous panel`.
