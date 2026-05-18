# Template Archetypes

Ten ready-to-build patterns for the most common Notion workspaces. Each archetype gives you: the high-level structure, the databases involved (with schemas), and a build sequence.

When a user says "build me a CRM" or "set up project management", pick the closest archetype, adapt it to their context, and confirm before generating JSON. Don't blindly produce the canonical version — the user's team size, industry, and existing workflow matter.

For visual design considerations on top of these archetypes (covers, icons, layouts), see `design-patterns.md`.

---

## 1. Personal CRM

**Use when:** the user manages a personal or small-team network of contacts and wants more structure than a contacts app.

**Structure:**
```
🤝 CRM (parent page)
├── 👥 People (database)
├── 🏢 Companies (database)
└── 📞 Interactions (database)
```

**`People` database:**
- `Name` (title)
- `Company` (relation → Companies)
- `Role` (rich_text)
- `Email` (email)
- `Phone` (phone_number)
- `LinkedIn` (url)
- `Last Contact` (date)
- `Relationship` (select: Close, Warm, Cold, Acquaintance)
- `Notes` (rich_text)
- `Latest Interaction` (rollup → Interactions, `latest_date` of date)

**`Companies` database:**
- `Company Name` (title)
- `Domain` (url)
- `Industry` (select)
- `People` (relation → People, dual)
- `Status` (status: Active, Lapsed, Target)
- `Notes` (rich_text)

**`Interactions` database:**
- `Subject` (title)
- `Date` (date)
- `Type` (select: Meeting, Call, Email, DM, Coffee, Other)
- `People` (relation → People)
- `Notes` (rich_text)
- `Follow-up` (date)
- `Follow-up Action` (rich_text)

**Build order:** Companies → People (link to Companies) → Interactions (link to People). Then add rollups.

**Views:**
- People: "Warm Network" filter `Relationship = Close OR Warm`, sort `Last Contact asc`.
- Interactions: "This Week" filter `Date this_week`, group by `Type`.

---

## 2. Project Management with Sprints

**Use when:** team manages discrete projects broken into tasks, with sprint cadence.

**Structure:**
```
🚀 Engineering (parent page)
├── 📋 Projects (database)
├── ✅ Tasks (database)
├── 🏃 Sprints (database)
└── 📝 Specs (subpage with linked database views)
```

**`Projects`:**
- `Project` (title)
- `Status` (status)
- `Owner` (people)
- `Priority` (select: P0, P1, P2, P3)
- `Start Date` / `Target Date` (date)
- `Tasks` (relation → Tasks, dual)
- `Open Tasks` (rollup → Tasks: count where Status ≠ Done)
- `% Complete` (formula)

**`Tasks`:**
- `Task` (title)
- `Project` (relation → Projects)
- `Sprint` (relation → Sprints)
- `Status` (status: Backlog, To Do, In Progress, In Review, Done)
- `Assignee` (people)
- `Priority` (select)
- `Estimate` (number, format: number) — story points or hours
- `Due Date` (date)
- `Type` (select: Feature, Bug, Chore, Spike)

**`Sprints`:**
- `Sprint Name` (title) — e.g., "S15: May 16-30"
- `Start` / `End` (date)
- `Tasks` (relation → Tasks)
- `Goal` (rich_text)
- `Total Points` (rollup → Tasks: sum of Estimate)
- `Completed Points` (rollup → Tasks: sum of Estimate where Status = Done)

**Views:**
- Tasks: Board grouped by Status, filtered to current Sprint.
- Tasks: "My Tasks" filtered to assignee = current user.
- Sprints: Timeline view.
- Projects: Gallery with cover, sorted by Priority then Target Date.

**Formula example for `% Complete`:**
```
round(prop("Completed Points") / prop("Total Points") * 100)
```

---

## 3. Content Calendar

**Use when:** editorial planning across blog/social/email/video.

**Structure:**
```
📅 Content (parent)
├── 📰 Content Pieces (database)
├── 💡 Ideas (database — inbox)
└── 📚 Channels (database — small lookup table)
```

**`Content Pieces`:**
- `Title` (title)
- `Status` (status: Idea, Drafting, In Review, Scheduled, Published)
- `Channel` (relation → Channels OR select: Blog, Twitter, LinkedIn, YouTube, Newsletter)
- `Author` (people)
- `Publish Date` (date)
- `Tags` (multi_select)
- `Hook` (rich_text)
- `Outline` (rich_text)
- `Final URL` (url)

**Views:**
- Calendar view by `Publish Date`.
- Board grouped by `Status`.
- Gallery for finished pieces ("Published" filter).

**Tip:** The page body of each content piece becomes the actual draft. This lets writers compose in Notion and the row stores the metadata.

---

## 4. OKR Tracker

**Use when:** the user wants to track Objectives and Key Results across a quarter or year.

**Structure:**
```
🎯 OKRs (parent)
├── 🎯 Objectives (database)
└── 📊 Key Results (database)
```

**`Objectives`:**
- `Objective` (title) — "Increase activated users by 30%"
- `Owner` (people)
- `Quarter` (select: Q1 2026, Q2 2026, ...)
- `Status` (status: Not Started, On Track, At Risk, Done)
- `Key Results` (relation → Key Results, dual)
- `Progress` (rollup → Key Results: avg of % Complete)

**`Key Results`:**
- `Key Result` (title)
- `Objective` (relation → Objectives)
- `Owner` (people)
- `Start Value` (number)
- `Current Value` (number)
- `Target Value` (number)
- `% Complete` (formula): `(prop("Current Value") - prop("Start Value")) / (prop("Target Value") - prop("Start Value")) * 100`
- `Update Cadence` (select: Weekly, Biweekly, Monthly)

**Views:**
- Objectives gallery, grouped by Quarter.
- Key Results table, filter by Current Quarter, sort by % Complete asc (worst-first).

---

## 5. Personal Task Manager (GTD-style)

**Use when:** the user wants their own task system, not a team one.

**Structure:**
```
📥 Tasks (parent dashboard)
├── ✅ Tasks (database)
├── 📁 Projects (database)
└── 🎯 Areas (database — long-running responsibility areas)
```

**`Tasks`:**
- `Task` (title)
- `Status` (status: Inbox, Next, Today, Waiting, Someday, Done)
- `Project` (relation → Projects)
- `Area` (relation → Areas)
- `Context` (select: @home, @office, @errands, @computer, @phone, @waiting)
- `Energy` (select: 🔋 High, 🪫 Low)
- `Time` (select: < 15min, < 1hr, > 1hr)
- `Due` (date)
- `Defer Until` (date)

**Views:**
- "Today": filter `Status = Today OR Due ≤ today`.
- "Next": filter `Status = Next`, group by `Context`.
- "Inbox": filter `Status = Inbox`.
- "Waiting": filter `Status = Waiting`, sort by oldest first.
- "Someday/Maybe": filter `Status = Someday`.

GTD purists will object to mixing contexts and projects in one DB. That's fine for personal use; teams should split contexts out into a separate database with a relation.

---

## 6. Meeting Notes Hub

**Use when:** team needs a single place for all meeting notes with searchability.

**Structure:**
```
📝 Meetings (parent)
└── 📝 Meeting Notes (database)
```

**`Meeting Notes` database:**
- `Meeting` (title) — e.g., "Eng weekly — 2026-05-16"
- `Date` (date with time)
- `Type` (select: 1:1, Standup, Weekly, Retro, Planning, Customer)
- `Attendees` (people)
- `Project` (relation → Projects, if PM archetype exists)
- `Recording` (url)
- `Action Items` (rich_text — or relation → Tasks)

**Page body template (set when creating each note):**
```
## Agenda
- [ ]

## Discussion

## Action items
- [ ] (owner)

## Parking lot
```

**Views:**
- Table sorted by `Date desc`.
- Calendar by `Date`.
- "My meetings" filter where current user in `Attendees`.

**Tip:** Use a database template so every new row starts with the agenda/discussion/action items structure.

---

## 7. Reading & Resource Library

**Use when:** the user wants to capture books, articles, podcasts, videos with searchability and notes.

**Structure:**
```
📚 Library (parent)
└── 📖 Resources (database)
```

**`Resources`:**
- `Title` (title)
- `Type` (select: Book, Article, Podcast, Video, Course, Paper)
- `Status` (status: Want to Read, Reading, Read, Abandoned)
- `Rating` (select: ⭐, ⭐⭐, ⭐⭐⭐, ⭐⭐⭐⭐, ⭐⭐⭐⭐⭐)
- `Author` (rich_text)
- `URL` (url)
- `Cover` (files — for gallery view)
- `Topics` (multi_select)
- `Started` / `Finished` (date)
- `Notes` (rich_text — short summary)

**Views:**
- Gallery sorted by `Status` then `Rating desc` — cover image as the card.
- Table for power-edits.
- "To Read" filter `Status = Want to Read`, sort by added date.
- "Best of" filter `Rating = 5 stars`.

Page body: long-form notes, quotes, takeaways.

---

## 8. Engineering Wiki

**Use when:** a team needs a knowledge base for processes, runbooks, decisions.

**Structure:**
```
🛠 Engineering Wiki (parent)
├── 📐 Architecture
│   ├── 🧭 Decisions (database)
│   └── 🗺 System Overviews (subpages)
├── 🔧 Runbooks (database)
├── 🎓 Onboarding (subpages)
├── 📝 Coding Standards (subpages)
└── 🏷 Glossary (database)
```

**`Decisions` (ADR database):**
- `Title` (title) — "ADR-014: Adopt event sourcing for billing"
- `Status` (status: Proposed, Accepted, Superseded, Deprecated)
- `Date` (date)
- `Authors` (people)
- `Tags` (multi_select)
- `Supersedes` (relation → self)
- `Superseded By` (relation → self, dual of Supersedes)

ADR body template: Context / Decision / Consequences / Alternatives Considered.

**`Runbooks`:**
- `Title` (title) — "Database failover procedure"
- `Service` (select)
- `Severity` (select)
- `Last Reviewed` (date)
- `Owner` (people)

**`Glossary`:**
- `Term` (title)
- `Definition` (rich_text)
- `Category` (select)
- `Related` (relation → self)

---

## 9. Product Roadmap

**Use when:** product team wants a public-or-internal view of what's coming.

**Structure:**
```
🗺 Roadmap (parent)
├── 🎯 Themes (database)
├── 🚢 Initiatives (database)
└── 📦 Features (database)
```

**`Themes`:** broad strategic bets ("Performance", "Onboarding", "Enterprise"). Simple — just title, owner, status, description.

**`Initiatives`:**
- `Initiative` (title)
- `Theme` (relation → Themes)
- `Status` (status: Discovery, Building, Beta, GA, Sunset)
- `Quarter` (select)
- `Owner` (people)
- `Description` (rich_text)
- `Features` (relation → Features)

**`Features`:**
- `Feature` (title)
- `Initiative` (relation → Initiatives)
- `Status` (status: Idea, Spec, Designing, Building, Done)
- `T-Shirt` (select: XS, S, M, L, XL)
- `Target Date` (date)
- `Customer Requests` (number)

**Views:**
- Initiatives timeline by `Quarter`.
- Features board by `Status`.
- "Now / Next / Later" view: Initiatives grouped by Quarter, current quarter visible.

---

## 10. Customer Feedback Tracker

**Use when:** PM/support team wants to aggregate signals across sources.

**Structure:**
```
🗣 Feedback (parent)
├── 💬 Feedback (database — every signal)
├── 🧩 Themes (database — clusters)
└── 🏢 Customers (database — who said it)
```

**`Feedback`:**
- `Summary` (title)
- `Quote` (rich_text — the customer's actual words)
- `Source` (select: Sales call, Support ticket, NPS, Interview, Slack, Twitter, Internal)
- `Date` (date)
- `Customer` (relation → Customers)
- `Theme` (relation → Themes)
- `Sentiment` (select: 👍 Positive, 👎 Negative, 😐 Neutral)
- `Urgency` (select: Low, Medium, High)
- `Linked Feature` (relation → Features, if Roadmap archetype exists)

**`Themes`:**
- `Theme` (title)
- `Description` (rich_text)
- `Feedback Count` (rollup → Feedback: count)
- `Last Mentioned` (rollup → Feedback: latest_date)

**`Customers`:**
- `Name` (title)
- `ARR` (number, dollar)
- `Tier` (select: Free, Pro, Enterprise)
- `Feedback Count` (rollup)

**Views:**
- Feedback: Board by Theme.
- Themes: gallery, sorted by Feedback Count desc.
- "Hot themes": filter Last Mentioned `this_week`.

---

## Universal build sequence

For any archetype with multiple databases:

1. **Create the parent page** with a hero callout describing the workspace.
2. **Create each database in dependency order** (databases that don't depend on others first, then the ones with relations).
3. **Add relation properties last** — both sides of a dual relation need both databases to exist.
4. **Add rollup properties last of all** — they depend on relations.
5. **Add 2-3 sample rows per database**, clearly marked as examples (e.g., title prefixed with "[Example]"). An empty database looks broken.
6. **Tell the user which views need UI configuration** (because views can't be fully created via API on most versions). Provide the exact recipe: "Open the Tasks database, click + New view, choose Board, group by Status."
7. **Set up the dashboard.** The parent page should pull in linked views of the key databases — typically a board or filtered table for "Active" or "This Week".

## Customization heuristics

- **Team of 1-3:** strip half the properties out. They'll add what they need.
- **Team of 10+:** add owner, last-edited-by, and views per role.
- **Has existing data to migrate:** ask before changing the schema. Copy-paste from CSV via Notion's import for first-row population, not API.
- **Will be used by non-technical users:** add a "How to use this" toggle at the top of each database with screenshots.
- **Will be public/shareable:** delete sample rows before sharing; add a real intro.
