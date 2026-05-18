# Beautiful Notion: A Design Reference for Agents

A synthesis of patterns from Marie Poulin (Notion Mastery), Thomas Frank, Easlo, William Nutt (Notion VIP), Red Gregory, August Bradley (PPV), and recurring patterns from the Notion template marketplace and r/Notion. The goal of this document is to give an AI agent enough taste and judgment to build a Notion page that does not just function, but feels considered.

The single most important idea, repeated across every source: **a beautiful Notion page is restrained, contextual, and consistent.** Almost every anti-pattern in this document is some variant of "too much, too dense, or too inconsistent." When in doubt, remove a block, increase whitespace, and use fewer colors.

---

## Part 1: The Anatomy of a Great Notion Page

A page reads top-to-bottom like a magazine spread: cover, title, intro, body, supporting databases. Top creators all converge on roughly the same skeleton:

```
+------------------------------------------------------+
|                   COVER IMAGE                        |  <- 1500x600, calm
+------------------------------------------------------+
| [icon]                                               |
|  Page Title (H1, implicit)                           |
|                                                      |
|  > Callout: 1-2 sentence purpose / intro             |  <- the "why"
|                                                      |
|  ----------------------- (divider) -----------------  |
|                                                      |
|  Quick Links  |  This Week  |  Inbox                 |  <- 3-col dashboard
|  ...          |  ...        |  ...                   |
|                                                      |
|  ## Section heading (H2)                             |
|  body content                                        |
|                                                      |
|  ## Section heading (H2)                             |
|  body content                                        |
+------------------------------------------------------+
```

### 1.1 Icons: emoji vs custom

| Use | When |
|---|---|
| Emoji | Personal pages, dashboards, anything playful, inline databases where a 16px icon needs to read instantly. Default choice. |
| Custom icon (Notion's built-in icon library) | Wikis, team workspaces, anything that needs to feel like a "product." Pick one color across the workspace (mid-gray on light mode is the safe bet). |
| Uploaded SVG/PNG | Brand-driven workspaces, client deliverables, premium-feeling templates (Easlo's signature is monochrome line icons uploaded as PNG). |
| No icon | Almost never. An iconless page in a sidebar list looks broken. |

**Sizing rule:** Notion renders the page icon at 78x78 on the page itself and 16x16 in the sidebar / inline mentions. Icons that read well at 16x16 (high contrast, single subject, no fine detail) win. A photo-realistic emoji set against a dense cover competes for attention; a flat icon on a flat gradient cover does not.

**Consistency rule (William Nutt's iconography principle):** within one workspace, pick one style and stay there. Mixed emoji + custom + uploaded icons across sibling pages reads as chaotic. The eye notices the inconsistency before it notices anything else.

### 1.2 Covers

- **Aspect ratio: 5:2.** Native size 1500x600, retina 3000x1200. Anything else gets cropped unpredictably across mobile/desktop.
- **Left third must stay calm.** That space holds the icon, title, and breadcrumb. Busy left edges fight the title.
- **Sources, ranked by how "designed" they feel:**
  1. Gradient generators (htmlcsscolor, notion-better-covers, coolors gradients). Most professional-feeling. Universal.
  2. Solid hex color exported as 1500x600 PNG. Easlo's whole brand is this.
  3. Unsplash via the built-in picker. Always free, always credited. Good for personal pages, weak for product/team pages because everyone uses the same five photos.
  4. Brand photography or illustration. Highest effort, highest payoff for client work.
- **When to omit a cover:** dense reference docs (specs, runbooks, meeting notes from a recurring meeting). A cover on every meeting note is visual noise; the cover loses its meaning as a "this page is special" signal.

### 1.3 Heading hierarchy

Notion gives you H1, H2, H3 and nothing else. Use them like this:

```
Page Title              <- this is the implicit H1. Do not put H1 in the body.
  ## H2 - section
    ### H3 - subsection
      body, lists, blocks
```

- **Maximum depth: 3 levels.** If you need H4, you actually need a sub-page.
- **Use H2 as your top body heading**, not H1. H1 in the body competes visually with the page title and makes the page feel like it has two beginnings. This is one of the most common amateur tells.
- Toggle headings (H2 toggle, H3 toggle) are the single best feature for managing long pages. Use them anytime a section is "important but not always needed." Wikis live or die by this.

### 1.4 Callouts as section headers

Two valid patterns:

**Pattern A: Callout as intro under H1.** One callout, at the top, 1-3 sentences explaining what this page is for. This is the Notion-native equivalent of a doc abstract. Marie Poulin's dashboards always have one.

**Pattern B: Callout as section divider.** Replace `## Heading` with a colored callout containing the heading text. Visually heavier than H2, lighter than a colored divider + H2. Best for dashboards where each section is a "card."

```
> [icon] Today's Focus
  (database inline below)

> [icon] This Week
  (database inline below)
```

**Do not mix.** Either every section is a callout, or every section is an H2. Mixing reads as indecision.

### 1.5 Toggle headings for collapsible sections

The defining move of well-organized Notion pages. Toggle H2 lets a page hold ten sections of content while only showing the one you need. The visual rule:

- Always-relevant content: ungated (H2 or callout).
- Sometimes-relevant content: toggle H2.
- Rarely-relevant content: sub-page link, not toggle.

A page made entirely of toggles is also an anti-pattern because nothing is visible on load - you get a wall of triangles. Aim for roughly 1/3 visible, 2/3 toggled on a reference page.

### 1.6 Columns: when 2-col vs 3-col vs full-width

```
Full width (default):
+------------------------------------------------+
| Long-form writing, single database table       |
+------------------------------------------------+

2-column:
+------------------------+-----------------------+
| Primary content        | Sidebar (metadata,    |
|                        | properties, links)    |
+------------------------+-----------------------+

3-column dashboard:
+-----------+--------------+----------------------+
| Quick     | Today's      | Inbox /              |
| Links     | Tasks        | Quick capture        |
+-----------+--------------+----------------------+
```

Heuristics:
- **1 column (full width off):** body writing, single big database, anything that wants to be read linearly.
- **1 column with `Full width` toggled on:** databases you want to give breathing room, especially wide tables.
- **2 columns:** project pages (content left, metadata right), meeting notes (notes left, attendees/action items right), article pages with a TOC sidebar.
- **3 columns:** dashboards only. More than three columns and Notion's gutters get too tight on a 13" laptop. Avoid 4+ unless every column is a tiny stat callout.
- **Mixed-width columns:** Notion lets you drag the column divider. Use it. A 70/30 split for "content + meta" reads better than 50/50.

### 1.7 Whitespace

Whitespace in Notion is achieved with three blocks: empty paragraphs, dividers, and the implicit padding around callouts/quotes. William Nutt's "Spacing" principle is the single highest-leverage tweak for making a page feel professional.

- Put **one empty paragraph** between major sections.
- Use **dividers** only between major regions (cover/intro vs body, or between the two databases at the bottom of a dashboard). A page full of dividers is as noisy as a page with none.
- Adjacent columns should be **allowed to differ in height.** Don't pad columns to match - the asymmetry is fine and often more pleasing.

### 1.8 Synced blocks for nav and headers

The "header bar" pattern: a synced block at the top of every page in a workspace containing links to the 4-6 places you go most often.

```
[Home]  [Tasks]  [Projects]  [Notes]  [Inbox]   <-- synced block
```

Place this once, sync it to every top-level page. When you add a new top-level destination, update the synced block in one place and it propagates. August Bradley's PPV system, Thomas Frank's Ultimate Brain, and most premium templates do this.

Other good uses for synced blocks:
- A "current quarter" goals callout that appears on Home and on each project page.
- A standard footer ("Last updated: ..., Owner: ...") on every doc in a wiki.

### 1.9 Inline vs full-page databases

| Use | When |
|---|---|
| Inline database | Database is a section of a larger context (e.g. tasks on a project page). The page is the unit of meaning. |
| Full-page database | The database is the unit of meaning (Tasks, Projects, Notes). It owns its own page, icon, cover, and views. |
| Linked database (inline) | You want to show a filtered view of a full-page database in another context. **This is the most-used pattern in any mature workspace.** |

**Rule:** every database should exist exactly once as a full-page database (the "source of truth"), and be referenced via linked views everywhere else. Inline databases that are not linked views are typically an early-stage mistake that turns into a fragmented data problem.

---

## Part 2: Named Visual Hierarchy Patterns

Twelve repeated structures. Each has a name, a use case, and a pseudo-block layout.

### 2.1 Hero with Callout Intro

The default for any "important" page (project root, doc, wiki entry).

```
[cover]
[icon] Title
> [icon] One-sentence purpose. Why this page exists.
---
## First section
```

When to use: top-of-hierarchy pages, any page someone might land on cold.

### 2.2 Three-Column Dashboard

The signature Notion home page. Marie Poulin, Thomas Frank, and every Notion-influencer dashboard variant.

```
[cover] [icon] Home
> Greeting callout: "Good morning. Here's what matters today."
---
| Quick Links | Today's Tasks      | Inbox / Capture     |
| (bookmarks) | (linked DB view,   | (linked DB, new-row |
|             |  filter = today)   |  inline)            |
---
## This Week
(wider linked DB below, full width)
```

When to use: personal home page, team space landing.

### 2.3 Quick Links Bar

A horizontal row of bookmarked pages or external links. Lives in a synced block at the top of every page, or as the first row of a dashboard.

```
[Home] [Tasks] [Calendar] [Inbox] [Wiki]
```

Implementation: 4-6 columns, each a single "link to page" block. Keep icons consistent.

### 2.4 Hub and Spoke

A parent page that mostly exists to link out to child databases. No content of its own beyond the links.

```
[icon] Engineering
> Everything the eng team needs lives here.
---
| [icon] Projects | [icon] Runbooks | [icon] Postmortems |
| [icon] Specs    | [icon] Onboarding | [icon] Tools     |
```

Each cell is a "link to page" with the database's own icon. When to use: any team workspace landing page.

### 2.5 Wiki Home (nested toggles)

```
[icon] Company Wiki
> Search above, or browse by team.
---
> Engineering
    > Backend
        - Runbooks
        - On-call
    > Frontend
        - Component library
        - Release process
> Sales
    > Playbooks
    > Onboarding
> People
    > Benefits
    > Policies
```

When to use: workspaces with deep content but where flat navigation would overwhelm. Pair with Notion's built-in Wiki feature for verified pages.

### 2.6 Meeting Note Template

```
[icon] [Meeting name] - 2026-05-16

| Date:       2026-05-16          | Attendees:    |
| Type:       Weekly 1:1          |  - @Alex      |
| Project:    [relation]          |  - @Sam       |

## Agenda
- [ ] item 1
- [ ] item 2

## Notes

## Action Items
- [ ] @owner - due date

## Decisions
```

Properties on the database: Date (date), Type (select), Attendees (people / multi-select), Project (relation), Status (status).

### 2.7 Project Page

Top-level metadata, then linked tasks DB filtered to this project, then notes.

```
[cover] [icon] Project Name
> Why this project, the outcome, the deadline.

| Status:    In Progress     | Owner: @Sam       |
| Start:     2026-05-01      | Due:   2026-06-15 |
| Priority:  P1              | Health: On track  |

---
## Tasks   (linked Tasks DB, filter: Project = this page)
(board view by status)

## Notes   (linked Meeting Notes DB, filter: Project = this page)

## Resources
- bookmarks, files, links
```

### 2.8 OKR Rollup

```
[icon] 2026 Q2 OKRs
---
## Objective 1: [title]
> Why this objective matters.
(linked Key Results DB, filter: Objective = this)
  - KR 1 - rollup: avg(progress %)
  - KR 2
  - KR 3
## Objective 2: ...
```

Objectives database has a relation to Key Results; Key Results has a number property `Progress` (0-100). Objectives shows a rollup property `Avg Progress` = `average of related Progress`. August Bradley's PPV is essentially this, scaled.

### 2.9 Reading List / Library

Gallery view, card preview = page cover, status property, rating.

```
[icon] Library
> What I'm reading, what I've read, what's next.
---
View tabs: [To Read] [Reading] [Finished] [All by rating]

(gallery view, cards show: cover, title, author, rating)
```

Properties: Title, Author, Status (To read / Reading / Finished), Rating (select: 1-5 stars as emoji), Date finished, Tags (genre).

### 2.10 Personal Home Dashboard

```
[cover] [icon] Home
> Good [morning/afternoon] - {today's date}

[Quick Links bar]
---
| ## Today                    | ## Upcoming Events       |
| (Tasks DB, filter: today)   | (Calendar DB, next 7d)   |
---
## Quick Capture
(Inbox DB, new-row block - one click adds a task)

## This Week
(Tasks DB, board by status, filter: week)
```

### 2.11 Spec / Doc Page (long-form)

```
[icon] Spec Title
> Status, owner, last updated, link to PR/ticket

## Context
## Goals / Non-goals
## Proposal
  ### Approach A
  ### Approach B (preferred)
## Open Questions (toggle list)
## Appendix (toggle: research notes)
```

Single-column, full-width off. Reads top-to-bottom like an RFC.

### 2.12 Sprint Board

```
[icon] Sprint 23 (May 13 - May 27)
> Goal: ship the onboarding redesign.

| Capacity: 40 pts | Committed: 36 pts | At risk: 0 |
---
(Tasks DB, board view, group by Status, filter: Sprint = current)
[Backlog] [To Do] [In Progress] [Review] [Done]
```

---

## Part 3: Database View Design

Pick the view first, then design backwards from what it needs to show.

### 3.1 Table view

- **Columns: show 4-7 max.** Title + Status + Owner + Date + one or two domain-specific properties. Anything else gets hidden but kept on the page.
- **Order: title -> status -> owner -> dates -> tags -> meta.** This is the conventional reading order.
- The title column is implicitly frozen; freeze additional columns only when scrolling horizontally is the primary action.
- Turn on **Wrap cells** when titles are sentences. Leave off when titles are short.
- Hide vertical lines and page icons when the table feels noisy.

### 3.2 Board view

- Group by **Status** by default. Other useful groupings: Owner (workload view), Priority (triage view), Sprint (planning view).
- Best when the database has <100 active items and items move between groups. If items rarely change status, a table is better.
- Card preview: hide. Show 2-3 properties on the card (priority, due date, owner avatar). More than that and cards become unscannable.

### 3.3 Gallery view

- Card preview source, ranked by feel:
  1. **Page cover** - most premium. Requires that every page actually has a cover, so commit to that as a workflow.
  2. **File property** - good for resource libraries where the file is the artifact (PDFs, images).
  3. **Page content** - first image inside the page. Inconsistent; only use if the others don't fit.
- Card size: medium is the default. Small for dense libraries (100+ items), large for showcases (<20 items).
- Always hide page icons on gallery cards if you're using cover images - they double up visually.

### 3.4 Calendar view

- Date property: pick **the date the thing happens**, not the date it was created. For tasks, this is Due Date. For meetings, this is Meeting Date.
- Use the date-range version (start + end) only if events span multiple days. Single-day events get a date-only property; the calendar handles this fine.
- Show 2-3 properties on calendar cards: title, owner, status indicator (color via status).

### 3.5 Timeline view

- Requires a date range property (start + end).
- Show **sub-items** when items have phases or milestones - this is the closest Notion gets to a real Gantt.
- Group by Owner (resourcing view) or Project (portfolio view).
- Keep a Table view alongside the Timeline for editing; Timeline is read-mostly.

### 3.6 List view

- The minimalist's view. No properties shown by default; just title and one or two pieces of meta.
- Use for: meeting notes (date + title is enough), wiki entries, anything where the page is what matters and the metadata is secondary.

### 3.7 Filtering: the workhorse combos

Every mature workspace uses some version of these:

```
"Mine, this week"
  Assignee = me
  AND Due Date is within next 7 days
  AND Status is not Done

"Triage queue"
  Status = To Do
  AND Priority is empty
  AND Created date is older than 3 days

"At risk"
  Due Date is within next 3 days
  AND Status is not In Review and not Done

"Active projects"
  Status is In Progress
  AND Archived is unchecked

"Inbox"
  Status is empty
  AND Created date is today
```

### 3.8 Sorting

The default sort for almost every task list is **Priority descending, Due Date ascending.** This puts P0/P1 work at the top, and within each priority, the most urgent first.

For meeting notes: **Date descending** (most recent first).
For projects: **Status, then Due Date ascending.**
For libraries: **Date Added descending** or **Rating descending.**

### 3.9 Linked database views

The rule: one source-of-truth database, many linked views in many contexts.

- Use **linked views** to embed the same data on a project page (filtered to that project), on a sprint page (filtered to that sprint), and on a personal home (filtered to "mine").
- Name views clearly inside each context: "My tasks - this week," "All open tasks," "Done this quarter."
- Sync filters across views only when it makes sense - typically each context has its own filter logic.

---

## Part 4: Color and Emoji Discipline

Notion gives you ten text colors and ten background colors. They are the same hues. Mature workspaces use them with restraint and **semantic consistency** - a color always means the same thing.

### 4.1 Notion's color palette (semantic conventions)

| Color | Common meaning |
|---|---|
| Default (no color) | Neutral, body text |
| Gray | Muted, deprioritized, metadata |
| Brown | Reference, archive |
| Orange | In progress, warning |
| Yellow | Attention, note, "thinking about" |
| Green | Done, success, on-track |
| Blue | Information, link, "for review" |
| Purple | Strategic, planning, ideas |
| Pink | Personal, soft priority |
| Red | Urgent, blocked, at-risk |

The standard task status palette is:

```
To Do          -> Gray
In Progress    -> Blue (or Orange)
In Review      -> Yellow
Blocked        -> Red
Done           -> Green
```

The standard priority palette is:

```
P0 / Urgent   -> Red
P1 / High     -> Orange
P2 / Medium   -> Yellow (or Default)
P3 / Low      -> Gray
```

### 4.2 Cohesive emoji families

A theme is more memorable than a random set. Pick a family for a workspace and stay in it.

| Family | Examples |
|---|---|
| Plants | seedling, herb, deciduous tree, palm, cactus, mushroom |
| Minerals | crystal ball, gem, prayer beads, hourglass |
| Tools | wrench, hammer, toolbox, gear, screwdriver |
| Weather | sun, cloud, rain, snowflake, rainbow |
| Office | clipboard, calendar, file folder, paperclip, chart |
| Animals (geometric) | fox, owl, whale, deer, bear |
| Travel | compass, map, mountain, tent, plane |

Mixing families is fine within a single workspace if each *area* has its own family ("Eng = tools, Marketing = office, Personal = plants"). Mixing within a single sibling group (one project is a hammer, the next is a strawberry) reads as random.

### 4.3 When too many colors becomes noise

The threshold: if a page has more than three colored elements above the fold, it's already loud. Rules of thumb:

- One callout color per section, not per paragraph.
- Highlight selectively. If everything is highlighted, nothing is.
- Status pills and priority pills already carry color. Don't add a colored heading on top - the eye now has two competing signals.
- Backgrounds (filled callouts) are heavier than text colors. Prefer text-color highlights unless the block is a true callout.

### 4.4 Cover image sources, again

- **Notion-better-covers**, **htmlcsscolor**, **coolors.co gradient generator** - for consistent gradients across many pages. Pick a palette and reuse.
- **Unsplash** (built-in) - personal pages, casual workspaces. Search for abstract shapes ("gradient," "texture," "minimal") rather than literal subjects to avoid the photo-stock cliche.
- **Pattern generators** (Hero Patterns, MagicPattern) - SVG patterns exported as PNG. Great for product/team workspaces.
- **Brand assets** - if the workspace represents a brand, use the brand. One photo or one gradient strip is more memorable than a stock image.

---

## Part 5: Property Design for Databases

### 5.1 Naming conventions

- Title-case property names: `Due Date`, not `due date` or `due_date`.
- Single words when possible: `Status`, `Owner`, `Priority`. Two words max.
- **Never** leave the auto-named `Date`, `Tags`, `Text` etc. that Notion adds. These read as "I didn't bother."
- **Never** number duplicates (`Date 2`, `Status 1`). If you have two date properties, name them what they actually are: `Due Date` and `Created`.
- Consistent terminology across databases. If "owner" means assignee in one DB, don't call it "lead" in another.

### 5.2 Property order

The default order (left to right in a table, top to bottom in a card / page):

```
1. Title          - what is it
2. Status         - where is it
3. Owner / Assignee - who has it
4. Priority       - how urgent
5. Dates (Due, Start, End) - when
6. Tags / Type    - what kind
7. Relations      - what it connects to
8. Meta (Created, Created By, Last Edited) - history
9. Formulas / Rollups - derived
```

Hide properties from views aggressively. The full set lives on the page; the view shows what's needed for that context.

### 5.3 Status property

Notion's `Status` type (distinct from `Select`) has built-in groups: To-do, In progress, Complete. Use it instead of Select for anything that moves through a workflow - it gets board view grouping and progress indicators automatically.

Typical option set:
```
To-do group:        Backlog, To Do, Up Next
In-progress group:  In Progress, In Review, Blocked
Complete group:     Done, Archived, Cancelled
```

### 5.4 Priority

- **P0/P1/P2/P3** when the team is engineering-cultured or there's a real ops cadence (incidents, sprints).
- **High/Medium/Low** when the audience is non-technical or the database is personal.
- **Critical/High/Medium/Low** if you need four levels but P-notation feels too dev.

Never mix systems in one workspace. Pick once.

### 5.5 Select vs multi-select

- **Select** when an item belongs to exactly one option. Status, Priority, Type.
- **Multi-select** when an item can have multiple tags. Topics, Categories, People (if not using the People property).

If you find yourself making 12+ select options, you probably want a related database instead - selects are for short, stable lists. Long select lists are an early sign that you've outgrown a flat tag system.

### 5.6 Date vs datetime

- **Date only** for: due dates, finished dates, deadlines, milestones.
- **Date + time** for: meetings, events, anything calendar-bound.
- **Date range (start + end)** for: timeline view items, multi-day events, projects with a span.

Never use a date+time for a deadline that's actually "end of day" - it creates false precision and timezone bugs.

---

## Part 6: Information Architecture

### 6.1 Page hierarchy depth

```
Workspace
  > Top-level page (Home, Wiki, Personal)        depth 1
    > Major section (Engineering, Projects)       depth 2
      > Specific page (Project Atlas)             depth 3
        > Sub-detail (Atlas - Spec)               depth 4 (borderline)
          > ...                                   depth 5+ (smell)
```

- Three levels is right for most things.
- Four levels is fine when there's a clear reason (project -> spec).
- Five+ levels is almost always a sign that something should be a database row instead of a nested page.

### 6.2 Database vs page

| Make it a database when... | Keep it a page when... |
|---|---|
| You have multiple instances of the same shape (tasks, projects, books) | It's a one-off (a doc, a runbook, the company handbook intro) |
| You need to filter, sort, group, or roll up | The content is the value, not the structure |
| You want different views of the same data | Linear reading is the access pattern |

The common mistake: making a database of one. If you only ever have one of something, it's a page.

### 6.3 Nesting databases vs relating them

- **Nest** (database is a sub-page) when the parent fully owns the child and you'd never look at the child outside the parent's context. Rare in practice.
- **Relate** (databases are siblings linked by a relation property) for almost everything else. Tasks should be siblings of Projects, related to each other - not nested inside Projects.

Relations are how Notion stops being a folder system and starts being a graph. Every mature workspace has 4-8 core databases with a relation web between them.

### 6.4 Index pages

A top-level navigation page that exists solely to point to other things. Hub-and-spoke pattern. Use one per major area (Personal, Work, Team).

### 6.5 Inbox pattern

One database called **Inbox** (or one row block on Home) where everything captured-in-haste lands without classification. Then a daily/weekly routine moves items from Inbox to their proper databases. The inbox is *meant* to be messy; the rest of the workspace stays clean because of it.

---

## Part 7: Template Archetypes

Eight templates in detail. Each one: purpose, databases, page structures, view configurations.

### 7.1 Personal CRM

**Purpose:** keep track of people - context, last contact, follow-ups.

**Databases:**
- `People` (the contacts).
- `Interactions` (each conversation, call, email, meeting).
- `Companies` (optional, related to People).

**People properties:** Name, Photo (files), Company (relation), Role, Email, Phone, Last Contact (rollup: max of Interaction date), Next Touch (date), Tags (multi-select: friend, prospect, mentor, etc.), Notes.

**Page structure:** each person's page has a callout intro ("how I know them"), a 2-column meta block, an inline view of their Interactions, and a Notes section.

**Views:**
- Table: all people, sorted by Last Contact ascending (oldest = most overdue).
- Board grouped by Tags or by Relationship Health.
- Calendar of Next Touch dates.
- Filtered view: "overdue for a touch" (Last Contact > 90 days ago).

### 7.2 Project Management with Sprints

**Databases:** `Projects`, `Tasks`, `Sprints`, `Meeting Notes`.

**Relations:** Task -> Project, Task -> Sprint, Meeting Notes -> Project.

**Sprints database properties:** Name, Date Range, Goal, Status, Tasks (relation, rollup count by status).

**Projects page:** cover, callout intro, meta row (status, owner, dates, health), linked Tasks board, linked Meeting Notes list, Resources section.

**Sprint page:** sprint goal callout, capacity stats, board of tasks grouped by status.

**Views on Tasks:**
- "My active" - assigned to me, status != Done.
- "This sprint" - filtered to current sprint, board by status.
- "Backlog" - status = Backlog, sorted by priority.
- "Timeline" - all tasks on a Gantt-style timeline.

### 7.3 Content Calendar

**Databases:** `Content` (the pieces), `Channels` (optional), `Campaigns`.

**Content properties:** Title, Status (Idea / Drafting / In Review / Scheduled / Published), Channel (select: blog, twitter, newsletter, etc.), Publish Date, Author (people), Campaign (relation), Hook, Cover.

**Page structure:** cover, callout with goal of the piece, 2-column (left = draft body, right = metadata + checklist).

**Views:**
- Calendar by Publish Date - the planning view.
- Board by Status - the production view.
- Gallery by cover - the visual portfolio.
- Filtered "Up next" - scheduled in next 14 days.

### 7.4 OKR Tracker

**Databases:** `Objectives`, `Key Results`, `Initiatives` (related to KRs).

**Objectives properties:** Title, Owner, Quarter, Status, KRs (relation), Avg KR Progress (rollup: average of related KR Progress %).

**KR properties:** Title, Objective (relation), Target, Current, Progress % (formula: Current / Target), Status, Initiatives (relation).

**Page structure:** Q2 2026 OKRs page, each Objective as an H2, KRs as bulleted relations or as a filtered inline list, Progress bars (Notion's number-as-bar format).

**Views:**
- Table of all Objectives sorted by Avg Progress ascending (most at-risk first).
- Board grouped by Quarter.
- Gallery (one card per Objective with the rollup % big).

### 7.5 Personal Task Manager (GTD-style)

**Databases:** `Tasks`, `Projects`, `Areas` (life domains: health, work, learning), `Someday`.

**Tasks properties:** Title, Status, Priority, Due Date, Project (relation), Area (relation), Context (select: @computer, @errand, @phone, @home), Energy (select: low / med / high).

**Home page:** today callout, inbox capture block, 3-col (Today / This Week / Waiting On), inline "Quick Capture" new-row block.

**Views:**
- Today - due today OR due before today AND not done.
- Next 7 days - calendar view.
- By Context - board grouped by Context.
- By Energy - useful for "I have 30 minutes and low energy, what can I knock out?"
- Someday/Maybe - filtered view, status = Someday.

### 7.6 Meeting Notes Hub

**Databases:** `Meeting Notes`, optionally `Action Items` (or just keep them as checkboxes on the note).

**Meeting Notes properties:** Title, Date (date+time), Type (select: 1:1, team standup, customer call, planning), Attendees (people), Project (relation), Action Items (related DB or count formula).

**Page template:** Date + Attendees in meta row, Agenda (bulleted), Notes, Action Items (checkboxes assigned to people with due dates), Decisions.

**Views:**
- List sorted by Date descending - default.
- By Type - filter tabs at the top.
- Calendar by Date.
- "My action items" - linked Action Items DB filtered to me, unchecked.

### 7.7 Reading & Resource Library

**Databases:** `Library` (books, articles, videos, podcasts, all in one).

**Properties:** Title, Type (select: book / article / video / podcast / course), Author, Status (To read / Reading / Finished / Abandoned), Started, Finished, Rating (1-5), Tags, Source URL, Notes (long text), Cover.

**Page template:** cover = book cover, callout with one-line takeaway, full notes below, related items (other books on same topic via relation or tag).

**Views:**
- Gallery by cover, grouped by Status - the bookshelf view.
- Table sorted by Rating descending - the "best of" view.
- Filtered "Currently reading" - status = Reading.
- Board grouped by Type.

### 7.8 Engineering Wiki

**Databases:** `Docs` (specs, design docs, RFCs), `Runbooks`, `Postmortems`, `Decisions` (ADRs).

**Top-level page:** Wiki home with hub-and-spoke to each database, plus a search callout and a "recently updated" linked view.

**Doc properties:** Title, Status (Draft / In Review / Approved / Deprecated), Author, Reviewers (people), Date, Tags, Related Docs (self-relation), Project (relation).

**Page template:** Spec / Doc pattern from Part 2. Notion's Wiki feature gives you the "Verified" badge - use it for approved docs.

**Views:**
- All docs by status.
- "Needs my review" - filter: Reviewers contains me, Status = In Review.
- "Approved this quarter" - status = Approved, date this quarter.

### 7.9 Product Roadmap (bonus)

**Databases:** `Initiatives` (the big bets), `Features` (the work), `Releases`.

**Properties:** Title, Status, Quarter, Initiative (relation), Team (select), Target Release (relation), RICE score (formula), Linked Spec (URL or page mention).

**Views:**
- Now / Next / Later board (group by a "Horizon" select property).
- Timeline by Quarter.
- Gallery for executive readouts.

### 7.10 Customer Feedback Tracker (bonus)

**Databases:** `Feedback` (one row per piece of feedback), `Themes` (clusters), `Customers` (or relation to CRM).

**Properties:** Title, Source (select: support, sales call, NPS, interview), Customer (relation), Theme (relation), Severity, Status (Triaged / Considering / Planned / Done / Won't Do), Linked Feature (relation to roadmap).

**Views:**
- Inbox: status is empty, sorted by created date.
- By Theme - board.
- "What's most asked" - grouped by Theme, count rollup, sorted descending.

---

## Part 8: Things That Look Amateurish

Anti-patterns. Each one is a quick fail-mode that signals "this workspace was built without taste."

1. **Walls of text without breaks.** Five paragraphs in a row with no headings, callouts, or whitespace. Fix: every 2-3 paragraphs gets a heading or a divider.

2. **Mixed icon styles in the same database.** Some rows have emoji, some have custom icons, some are blank. Fix: pick one style for the database and apply it everywhere (or apply nothing).

3. **Table view with 15+ visible columns.** Properties get truncated to "..." and nothing is readable. Fix: show 4-7 columns per view; keep the rest on the page.

4. **Random capitalization in property names.** `Due date`, `Owner`, `priority`, `STATUS`. Fix: pick Title Case and stay there.

5. **Default "Untitled" pages.** Either rename or delete. Untitled rows in a database are the most visible signal of an unloved workspace.

6. **Inconsistent date formats.** Some entries have full datetime, some have date only, some are written as text in the title. Fix: one date property, one format, enforced by template.

7. **Bullet lists 5 levels deep.** Indentation becomes incomprehensible past 3 levels. Fix: at level 4 it's a sub-page, or restructure into a table.

8. **H1 in the body.** The page title is already H1. Adding H1s in the body makes the page look like it has multiple beginnings. Fix: start at H2.

9. **Empty databases with no description.** A user lands on a database with zero rows and no callout explaining what it's for. Fix: every database has an intro callout describing what goes in it and a template button.

10. **Status property with one option ("Active").** A status with no states isn't a status. Fix: either use a checkbox or commit to real workflow states.

11. **Cover image, no icon (or vice versa).** Asymmetric branding feels half-done. Fix: both or neither.

12. **Colored backgrounds on every other block.** Rainbow stripes. Fix: at most one callout color per section.

13. **Names like "Database," "Page," "Untitled Page (1)."** Build-time leftovers that never got renamed. Fix: rename or delete during cleanup pass.

14. **Inline databases scattered across pages with no source of truth.** Each new page creates its own tasks DB. Fix: one canonical database, linked views everywhere else.

15. **Toggle-only pages.** Every block is collapsed. The page loads as a wall of triangles. Fix: roughly 1/3 visible, 2/3 toggled.

16. **Pages with cover images but no padding/breathing room.** Cover ends, title starts, body starts immediately, dense paragraph immediately after. Fix: empty paragraph after the intro callout; one divider before body.

17. **Tag/select options with duplicates.** "marketing," "Marketing," "Mktg" all exist as separate tags because of typos. Fix: clean up regularly, keep option lists short.

18. **Relations that aren't bidirectional or aren't named.** Notion lets you hide the inverse - don't, unless there's a real reason. The reverse relation is often more useful than the forward one.

---

## Part 9: Quick Reference - The "Beautiful by Default" Checklist

When building any new Notion page, an agent should run through this:

- [ ] Cover image at 1500x600, calm on the left third.
- [ ] Icon (emoji or custom) consistent with siblings.
- [ ] One callout under the title with the purpose in 1-2 sentences.
- [ ] Divider between intro and body.
- [ ] H2 as the highest body heading (never H1 in body).
- [ ] Maximum 3 levels of heading depth.
- [ ] Whitespace: empty paragraphs between sections.
- [ ] If it's a dashboard: 3 columns, not 4+.
- [ ] If it has a database: 4-7 visible columns max in the default view.
- [ ] Property order: title -> status -> owner -> dates -> tags -> meta.
- [ ] Status uses Notion's Status type, not Select.
- [ ] Colors used semantically (red = urgent, green = done, etc.).
- [ ] No mixed icon styles.
- [ ] No "Untitled" or "Date 2" leftover names.
- [ ] One source-of-truth database, linked views elsewhere.
- [ ] If it's a wiki: synced nav block at the top.
- [ ] If it's a long page: toggle headings where the content is optional.

---

## Part 10: A Final Heuristic

When you cannot decide between two options, ask: **"Which one looks like it took less effort to use?"** Pick that one. Beautiful Notion is not about adding ornament - it is about removing friction. Marie Poulin's neurofriendly framing, Easlo's minimalism, William Nutt's spacing principle, and August Bradley's "show only what matters in this context" all point to the same place: the best Notion page is the one where the user immediately knows where to look and what to do.

The aesthetic follows from the clarity. Not the other way around.

---

## Sources

- [Notion VIP: Design Usable, Delightful Notion Pages (William Nutt)](https://www.notion.vip/insights/design-usable-delightful-notion-pages)
- [Marie Poulin - Workflow Design with Notion](https://mariepoulin.com/blog/)
- [Marie Poulin - Neurofriendly Notion Workspaces](https://mariepoulin.com/blog/a-helpful-guide-to-designing-neurofriendly-notion-workspaces/)
- [Thomas Frank - Build a Personal Dashboard in Notion](https://thomasjfrank.com/how-to-build-a-personal-dashboard-in-notion/)
- [Thomas Frank - 17 Tips for Building Your Perfect Notion Aesthetic](https://thomasjfrank.com/17-tips-for-building-your-perfect-notion-aesthetic/)
- [Easlo - Notion Templates](https://www.easlo.co/templates)
- [Easlo Interview - Crafting Engaging Notion Templates](https://deltahub.io/blogs/news/easlo-s-secrets-to-crafting-engaging-notion-templates)
- [Red Gregory - Notion Articles](https://www.redgregory.com/)
- [August Bradley - PPV (Pillars, Pipelines & Vaults)](https://www.yearzero.io/notion)
- [Notion Help - When to use each database view](https://www.notion.com/help/guides/when-to-use-each-type-of-database-view)
- [Notion Help - Page icons & covers](https://www.notion.com/help/guides/page-icons-and-covers)
- [Notion Help - Style and customize your page](https://www.notion.com/help/customize-and-style-your-content)
- [Notion VIP - Compare and Configure Database Formats](https://www.notion.vip/insights/compare-and-configure-notion-s-database-formats-tables-lists-galleries-boards-and-timelines)
- [Notion Mastery - Naming and Nomenclature](https://notionmastery.com/naming-and-nomenclature-in-notion/)
- [Notion Marketplace](https://www.notion.com/templates)
