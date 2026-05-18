# Notion Ecosystem Reference

A curated reference of third-party tools, libraries, templates, blogs, and authoritative resources for working with Notion. Designed so an AI agent can immediately answer "what should I read to learn X about Notion" or "what library should I use to do Y".

---

## 1. Official Notion Resources

### 1.1 Notion Developer Platform (`developers.notion.com`)

The Notion Developer Docs were rebuilt in 2026 with a built-in AI assistant. The documentation is the canonical reference for the Notion API and developer platform.

| URL | What's there |
| --- | --- |
| `https://developers.notion.com/` | Home, navigation, search, AI doc assistant. |
| `https://developers.notion.com/reference/intro` | API reference root — authentication, base URL, conventions. |
| `https://developers.notion.com/reference/versioning` | API versions (`2022-06-28`, `2025-09-03`, `2026-03-11`, etc.) and how to pin the `Notion-Version` header. |
| `https://developers.notion.com/reference/request-limits` | Rate limits, payload caps, pagination limits. |
| `https://developers.notion.com/reference/block` | Block object schema (the JSON representation of every block type). |
| `https://developers.notion.com/reference/page` | Page object. |
| `https://developers.notion.com/reference/database` | Database object and the 2025-09-03 split of database vs data source. |
| `https://developers.notion.com/reference/post-search` | Search endpoint. |
| `https://developers.notion.com/reference/webhooks` | Integration webhook subscriptions — endpoint setup, signing, events. |
| `https://developers.notion.com/reference/webhooks-events-delivery` | Event types, retry behavior (8 retries, exponential backoff up to ~24 h). |
| `https://developers.notion.com/guides/data-apis/working-with-markdown-content` | Official guidance for sending and receiving markdown via the API. Lets you `POST /v1/pages` with a `markdown` field instead of `children`. |
| `https://developers.notion.com/docs/upgrade-guide-2025-09-03` | Migration guide for the data-source split. |
| `https://www.postman.com/notionhq/notion-s-api-workspace` | Notion's official Postman workspace. |

### 1.2 Developer platform components (2026)

- **Notion Workers** — hosted runtime for custom code with 10-second time limit and 128 MB memory cap; deployed via the Notion CLI.
- **External Agents API** — bring in-house agents into Notion with triggers, tools, and permissions.
- **Notion CLI** — sign into a workspace, read/take action, build and deploy Workers.
- **Custom Agents** — admin controls at *Settings → Notion AI → Agents* (per-agent and workspace-level credit limits, usage dashboard).

### 1.3 Templates Gallery / Marketplace

- `https://www.notion.com/templates` — 30,000+ official and creator-submitted templates.
- `https://www.notion.com/templates/creators` — browse by creator.
- `https://www.notion.com/templates/category/...` — categorical browse (e.g. `/projects`, `/crm`, `/okr-tracker`, `/personal-dashboards`, `/knowledge-base`, `/sprint-planning`, `/api-documentation`).
- `https://www.notion.com/help/guides/getting-started-as-a-template-creator-on-marketplace` — creator onboarding.
- `https://www.notion.com/help/selling-on-marketplace` — Stripe integration; Notion takes 10% + $0.40 per transaction. Supports access locking.
- Creator profile setup happens at `https://www.notion.so/profile`.

### 1.4 Notion Academy and Help Center

- `https://www.notion.so/help/notion-academy` — structured courses (e.g., "Putting structure and order in your workspace", a 6-lesson sequence).
- `https://www.notion.com/help` — top-level help.
- `https://www.notion.com/help/guides/` — feature deep-dives (the most useful long-form help content):
  - `/intro-to-databases`, `/full-page-vs-inline-databases`, `/simple-tables-vs-databases`, `/when-to-use-each-type-of-database-view`
  - `/getting-started-with-projects-and-tasks`, `/product-engineering-notion-sprint-planning`
  - `/three-key-databases-for-teams-and-how-to-use-them`
  - `/teamspaces-give-teams-home-for-important-work`, `/how-workspace-owners-can-set-up-teamspaces-for-their-organization`
  - `/automate-work-repeating-database-templates`, `/create-streamlined-project-management-workflow-using-database-automations`
  - `/unleashing-productivity-with-notions-slack-integration`
  - `/bring-your-codebase-into-context-with-notions-github-integration`
  - `/preserve-perfect-meeting-memory-with-ai-meeting-notes`
  - `/page-icons-and-covers`
  - `/types-of-content-blocks`
  - `/how-to-build-a-help-center-in-notion`
- `https://www.notion.com/help/notion-academy/lesson/organized-workspace-best-practices` — official "don't let your workspace become a mess" lesson.

### 1.5 Releases / changelog

- `https://www.notion.com/releases` — chronological product release notes.
- `https://developers.notion.com/changelog` — API changelog.
- Recent significant 2026 releases (all under `https://www.notion.com/releases/YYYY-MM-DD`):
  - `2026-05-13` — Notion 3.5: Developer Platform GA (Workers, External Agents, CLI).
  - `2026-05-05` — Custom Agent admin controls and credit limits.
  - `2026-04-17` — Mail & Calendar settings consolidation.
  - `2026-04-14` — Notion 3.4 part 2.
  - `2026-02-24` — Notion 3.3: Custom Agents launched.
  - `2025-04-15` — Notion 2.50: Notion Mail launched.

### 1.6 Broader product surface

- **Notion Calendar** — full timezone support, scheduling tool, embeds Notion databases. Notion Agents can find slots, create events, and render a live calendar grid in chat. Use `/schedule` from Notion Mail to share availability.
- **Notion Mail** — AI-organized inbox; auto-labels and custom views; can draft replies and schedule meetings using Notion AI; integrates with Calendar.
- **Notion Sites** — publish any page as a website. Launched June 2024. Free `*.notion.site` URLs; custom domain add-on is +$10/mo (or $8/mo annual) per domain; up to 25 domains. SEO meta tags, Google Analytics support.
  - `https://www.notion.com/help/public-pages-and-web-publishing`
  - `https://www.notion.com/help/connect-a-custom-domain-with-notion-sites`
  - `https://www.notion.com/help/notion-sites-availability-and-pricing`
- **Notion AI** — context window expanded to 50 pages in early 2026 (up from 20). Custom Agents on Business/Enterprise; credits are $10 per 1,000 monthly credits (paid since May 2026).
- **Notion Community** — `https://www.notion.so/community` lists official global groups, Reddit, and Ambassadors.

---

## 2. SDKs and Libraries

### 2.1 Official SDKs

| Name | Lang | Repo | What it adds | Maturity |
| --- | --- | --- | --- | --- |
| `@notionhq/client` | Node.js / TypeScript | `https://github.com/makenotion/notion-sdk-js` | Typed wrapper for all endpoints. Auto-retry on 429/500/503 with exponential backoff. Typed errors (`APIResponseError`, `RequestTimeoutError`). Built-in pagination helpers. Defaults configurable via named constants. Supports API versions `2025-09-03` (default) and `2026-03-11`. Current release `v5.20.0` (Apr 2026). | Official, actively maintained. |
| `notion-agents-sdk-js` | JS / TS | `https://github.com/makenotion/notion-agents-sdk-js` | Notion Agents SDK — build and deploy custom agents, integrate with the External Agents API. | Official, new (2026). |
| Notion CLI | Cross-platform | distributed via Notion Developer Platform | Sign in, deploy Workers, read/take action on a workspace. | Official, new. |

### 2.2 Community SDKs

| Name | Lang | Repo | Notes |
| --- | --- | --- | --- |
| `notion-sdk-py` (Ramnes) | Python | `https://github.com/ramnes/notion-sdk-py` (docs `https://ramnes.github.io/notion-sdk-py/`) | The de-facto Python client. Sync + async. Mirrors the JS SDK's interface; retries on rate limit and transient server errors. The most-cited Python SDK in tutorials. |
| `jomei/notionapi` | Go | `https://github.com/jomei/notionapi` (`pkg.go.dev/github.com/jomei/notionapi`) | Covers all endpoints of Notion API `2022-06-28`. |
| `kjk/notionapi` | Go | `https://github.com/kjk/notionapi` | Unofficial older client; mostly read-focused. Used by `notion-tools` and `notion-export`. |
| `notion-sdk` | Rust | `https://docs.rs/notion-sdk` | Async Rust client. |
| `notion-sdk` (PyPI) | Python | `https://pypi.org/project/notion-sdk/` | Alternative Python client; smaller community than Ramnes's. |

### 2.3 Conversion / publishing libraries

| Name | Lang | Repo | What it does |
| --- | --- | --- | --- |
| `notion-to-md` | Node/TS | `https://github.com/souvikinator/notion-to-md` (npm `notion-to-md`) | Convert Notion pages/blocks/lists into Markdown, MDX, JSX, HTML, LaTeX. v4 is a full redesign with a plugin/renderer architecture (`https://notionconvert.com/notion-to-md/`). The most popular Notion→Markdown library. |
| `@tryfabric/martian` | Node/TS | `https://github.com/tryfabric/martian` | Markdown → Notion API blocks and RichText. Uses `unified` for the AST. Supports inline elements, lists, code blocks with language, tables, equations, images. Exposes `markdownToBlocks` and `markdownToRichText`. |
| `tryfabric/markdown-to-notion` | GitHub Action | `https://github.com/tryfabric/markdown-to-notion` | GitHub Action wrapping Martian to publish a Markdown file to a Notion page. |
| `notion2md` (echo724) | Python | `https://github.com/echo724/notion2md` (PyPI `notion2md`) | CLI + library. Built on `notion-sdk-py`. Downloads inline files/images. ~550 stars. |
| `notion2markdown` (alvinwan) | Python | `https://github.com/alvinwan/notion2markdown` (PyPI `notion2markdown`) | Alternative Python exporter. |
| `notion4ever` | Python | `https://github.com/MerkulovDaniil/notion4ever` | Export a Notion page (with all nested subpages) as Markdown and static HTML. |
| `notionmd` (Britton Hayes) | Go | `https://github.com/brittonhayes/notionmd` | Go: Markdown → Notion blocks. |
| `markdown-to-notion-blocks` (Roel Magdaleno) | PHP | `https://github.com/roelmagdaleno/markdown-to-notion-blocks` | PHP package outputting Notion block JSON. |
| `md_to_notion` | Ruby | `https://github.com/rieg-ec/md_to_notion` | Pure Ruby Markdown → Notion blocks. |
| `mcp-mdnotion` | TS | `https://github.com/aia-ops/mcp-mdnotion` | MCP server that converts Markdown to Notion blocks (for agent tooling). |
| `notion-export-markdown` (Dwarves) | Go | `https://github.com/dwarvesf/notion-export-markdown` | Export Notion → Markdown for use in Obsidian. |
| `notion-exporter` (Yann Bolliger) | TS | `https://github.com/yannbolliger/notion-exporter` | CLI/library for exporting Markdown and CSV. |

### 2.4 Renderers and site frameworks

| Name | Lang | Repo / URL | Notes |
| --- | --- | --- | --- |
| `react-notion-x` | React/TS | `https://github.com/NotionX/react-notion-x` | Fast, accurate React renderer for Notion. ~28 KB gzipped main bundle. Powers many Notion-as-CMS blogs. Includes a Markdown export helper that is "very useful for LLMs". |
| `nextjs-notion-starter-kit` | Next.js | `https://github.com/transitive-bullshit/nextjs-notion-starter-kit` (demo `https://transitivebullsh.it/nextjs-notion-starter-kit`) | Deploy a Notion-powered website on Vercel. Generates social/OG images automatically. Open-source equivalent of Super/Potion. Maintainer: `@transitive-bullshit` (Travis Fischer). |
| `notion-client` | npm | `https://www.npmjs.com/package/notion-client` | The unofficial Notion API client that `react-notion-x` uses to fetch private page data. |
| **Super.so** | hosted | `https://super.so/` | Commercial Notion-to-website (~$12/mo). SEO, custom domains, themes. |
| **Potion** | hosted | `https://potion.so/` | Commercial alternative to Super. |
| **HostNotion** | hosted | `https://hostnotion.co/` | Lightweight custom-domain proxy for Notion pages. |
| **Simple.ink** | hosted | `https://www.simple.ink/` | Notion → site, focused on simplicity. |
| **HelpKit** | hosted | `https://www.helpkit.so/` | Specialized Notion-as-help-center service. |
| **Notiondesk** | hosted | `https://notiondesk.so/` | Another Notion-as-help-center option. |
| **Feather** | hosted | `https://feather.so/` | Notion-as-blog with SEO emphasis. |
| **Bullet.so** | hosted | `https://bullet.so/` | Notion-as-website builder. |
| **Embednotionpages** | hosted | `https://www.embednotionpages.com/` | Embed Notion content into existing sites. |

### 2.5 AI / agent integrations

- **LangChain `NotionDBLoader`** — `https://python.langchain.com/docs/integrations/document_loaders/notion/` — loads pages from a Notion database into Document objects for retrieval/RAG.
- **LlamaIndex / LlamaHub Notion connector** — provides a similar Notion data loader for ingestion pipelines.
- **Model Context Protocol (MCP) servers** — `mcp-mdnotion` (above) and several community MCP servers expose Notion as a tool surface for Claude, ChatGPT, etc.
- **Make / n8n / Zapier nodes** — Notion is a first-class connector on all three (see Section 6).

---

## 3. Markdown ↔ Notion Conversion (Critical for Agents)

Many agents accept markdown input and need to translate it into Notion's block JSON. Three approaches.

### 3.1 Approach A — Let Notion do it

The **2025-09-03+ API supports a `markdown` field directly on `POST /v1/pages`** and on block creation. From `https://developers.notion.com/guides/data-apis/working-with-markdown-content`:

- Send Notion-flavored Markdown as a string in the `markdown` field (use actual `\n` newlines in JSON).
- Notion parses it into its internal block representation server-side.
- For unsupported block types in the markdown output, fall back to the block-based API to retrieve structured data.

This is the recommended path for agents — fewer round trips, no client-side AST work, and Notion handles dialect quirks.

### 3.2 Approach B — Client-side conversion to block JSON

Use a library that parses markdown into the Notion block schema and then POST `/v1/blocks/{id}/children` with the resulting array.

- **JS / TS**: `@tryfabric/martian` (`markdownToBlocks(md)` → `Block[]`).
- **Python**: `mistune` / `markdown-it-py` + a custom transformer, or use `notion2md` patterns in reverse, or use the official `markdown` field via API.
- **Go**: `brittonhayes/notionmd`.
- **PHP**: `roelmagdaleno/markdown-to-notion-blocks`.
- **Ruby**: `rieg-ec/md_to_notion`.

Things to remember when doing this by hand:

- Rich text objects cap at **2,000 characters** per object — split long inline runs.
- A `children` array can have at most **100 elements per request**.
- A request payload is capped at **1,000 block elements** and **500 KB total**.
- A page can hold at most 1,000 blocks for API-created content on free workspaces.
- Common gotchas: tables must be created with a `table` block whose `children` are `table_row` blocks; the row's `cells` is `RichText[][]`. Code blocks need a `language` enum string. Callouts can include `icon` (emoji or external URL).

### 3.3 Approach C — Hybrid (markdown for prose, JSON for structured blocks)

- Use the `markdown` field for body content (paragraphs, lists, headings, code, quotes).
- Use the block-based API only for blocks that don't round-trip cleanly: databases, embeds, synced blocks, columns, toggle headings, child pages, AI/meeting-notes blocks.
- This is the pattern most production agents converge on.

### 3.4 Notion → Markdown (the reverse)

For pulling Notion content out for LLM context, exports, or static sites:

- `notion-to-md` (JS) for general purpose, MDX, etc.
- `notion2md` (Python) for scripting/CLI.
- The API's own markdown output (2025-09-03+) — request markdown on retrieval where supported.
- `react-notion-x`'s built-in markdown helper for client-side rendering.

---

## 4. Template and Design Resources

### 4.1 Top template creators

| Creator | Hub | Specialty |
| --- | --- | --- |
| **Easlo** (Eddy Liang) | `https://www.easlo.co/` (`/templates`, `/free-notion-templates`) | Minimalist, clean, mass-market. 30+ templates. Free templates used 800k+ times. Strong on Second Brain, finance, planners, business ops. |
| **Thomas Frank** | `https://thomasjfrank.com/` (templates at `/templates/`) | "Ultimate Brain" (best-selling all-in-one) and "Creator's Companion" (content creator workflow). Long-form blog and YouTube tutorials. Community at `community.thomasjfrank.com`. |
| **Marie Poulin** | `https://mariepoulin.com/`, `https://notionmastery.com/`, marketplace `https://www.notion.com/@mariepoulin` | Workflow design and the **Notion Mastery** course. Notion Ambassador and Notion Certified Consultant. Strong on client portals, agency systems, teams. |
| **William Nutt** | `https://www.notion.vip/`, `https://www.notion.vip/a-to-z`, `https://bulletproof.notion.vip/` | The **Bulletproof Workspace** framework (Notion's most-cited independent framework). Co-author of Notion's official reference. Hosts *Notion at Work*. Manages the Notion Certified program. |
| **August Bradley** | `https://www.yearzero.io/notion`, course at `https://www.notionlifedesign.com/` | **PPV (Pillars, Pipelines, Vaults)** life-OS methodology. Long-form YouTube. |
| **Red Gregory** | `https://www.redgregory.com/notion`, Substack `https://redgregory.substack.com/`, YouTube `https://www.youtube.com/c/RedGregory` | Best free resource for **formulas, rollups, relations, and the API**. The most-cited blog for "how do I do X in Notion formulas". |
| **Janice Chou** (`@slow_is_better`) | `https://slowisbetter.medium.com/`, Gumroad `https://slowisbetter.gumroad.com/` | "Slow Productivity" systems; pages-vs-databases explainers. |
| **Jennifer Chou** (Vegan Tech Nomad) | `https://vegantechnomad.com/` | ADHD-friendly life tracking; aesthetic dashboards; finance trackers. |
| **Francesco D'Alessio** (Keep Productive / Tool Finder) | YouTube `https://www.youtube.com/channel/UCYyaQsm2HyneP9CsIOdihBw` | Software comparison and "which tool" content. Skillshare Notion course. |
| **Matthias Frank** | `https://matthiasfrank.de/` | Notion update tracker, Zettelkasten for Notion. |
| **Notion Everything** | `https://www.notioneverything.com/` | Template curation, wiki/dashboard roundups. |
| **Gridfiti** | `https://gridfiti.com/` | Aesthetic templates and "best courses" roundups. |
| **The Organized Notebook** | `https://theorganizednotebook.com/` | Templates and update commentary. |
| **Notion Ave / Notion Hub / Notionry** | various | Template directories. |

### 4.2 Reddit / community

- `https://www.reddit.com/r/Notion/` — 200k+ members; official community on Reddit. Primary unofficial Q&A channel.
- `https://www.reddit.com/r/NotionSo/` — smaller, secondary community.
- `https://www.reddit.com/r/FreeNotionTemplates/` — curated free templates.
- `https://www.notion.so/community` — Notion's directory of community groups, Ambassadors, and events.

### 4.3 Aesthetics, icons, covers

- **Notion Icons by Fountn** — `https://fountn.design/resource/notion-icons-4550-notion-style-illustrations-icons-and-wallpapers/`
- **Overflow Design** cover guide — `https://www.overflow.design/notion-cover-size/`
- **Icons8 Notion covers** — `https://blog.icons8.com/articles/notion-covers-with-mega-creator/`
- **2sync covers guide (2026)** — `https://2sync.com/blog/notion-covers`
- Cover dimensions: **1500 × 600 px** desktop (5:2). Mobile crop ≈ 1170 × 445 px. Keep critical artwork inside the central 1170 × 230 region. Keep file under 5 MB. Leave the **left third uncluttered** for icon + title overlay.

---

## 5. Notable Patterns and Methodologies

### 5.1 PARA (Projects, Areas, Resources, Archive)

- Created by **Tiago Forte** — `https://www.buildingasecondbrain.com/para`.
- Official Second Brain Notion template: `https://www.buildingasecondbrain.com/notion-template`.
- Forte's full overview: `https://fortelabs.com/blog/basboverview/`.
- Best Notion-native PARA template: Thomas Frank's `https://thomasjfrank.com/templates/para-method-template-for-notion/`.
- Core principle: **organize by actionability, not subject**. Projects have deadlines and end; Areas are ongoing responsibilities; Resources are reference; Archive is inactive.

### 5.2 Zettelkasten

- Method: atomic, evergreen, densely linked notes; emphasis on links over folders.
- Notion implementations of note: **Matthias Frank's Zettelkasten for Notion** (`https://matthiasfrank.de/en/zettelkasten-for-notion/`), **Zettel-PARA template** (`https://www.notion.com/templates/zettelpara`).
- Linking patterns: use `@` mentions inline, plus a "Connected to" relation property whose inverse ("Has been mentioned in") auto-updates.

### 5.3 PPV (Pillars, Pipelines, Vaults)

- Created by **August Bradley** — `https://www.augustbradley.com/` and `https://www.yearzero.io/notion`.
- **Pillars** — life values and quantifiable goals.
- **Pipelines** — daily action queues prioritized by their connection to Pillars/Goals/Projects.
- **Vaults** — knowledge collection that resurfaces information at the right moment.
- Implemented as a deeply relational Notion system. Course: `https://www.notionlifedesign.com/`.

### 5.4 Bulletproof Workspace (William Nutt)

- `https://bulletproof.notion.vip/`
- "Centralize content in databases; access it through contextual views."
- Synthesizes GTD, PARA, time blocking, the Eisenhower Matrix, the Pareto Principle, MoSCoW, and Eat the Frog into one task system.
- The Bulletproof template is sold via Gumroad (`https://williamnutt.gumroad.com/l/PKGYu`) and is reportedly Notion's top-selling third-party template.

### 5.5 Second Brain / BASB (Tiago Forte)

- Companion methodology to PARA. CODE = Capture, Organize, Distill, Express.
- Officially Notion-compatible but tool-agnostic.
- `https://www.notionsecondbrain.com/` — Forte's Notion-specific template.

### 5.6 Wiki / verified pages (native Notion pattern)

- Convert any page → Wiki (kebab menu → "Turn into Wiki").
- Adds **owner** and **verified** properties; enables verification expiration.
- Standard wiki taxonomies seen across teams: *HR Policies, Engineering Best Practices, Sales Playbooks, Marketing & Brand, Onboarding*.
- Reference: `https://www.notion.com/help/guides/category/wiki` and `https://www.notioneverything.com/blog/notion-wiki-verified-pages`.

---

## 6. Automation and Integrations

### 6.1 Notion Database Automations (native)

Docs: `https://www.notion.com/help/database-automations`, guide `https://thomasjfrank.com/notion-database-automations-the-complete-guide/`.

**Triggers**:

- *Page added* — when a row is added to the database.
- *Property edited* — when a chosen property changes value.

**Actions**:

- Update/edit properties on the same page.
- Add a page to another database.
- Edit pages/properties in another database.
- Send a Slack notification to a channel.
- Send a webhook (HTTP POST to arbitrary URL — the gateway for Zapier/Make/n8n/custom code).
- Send an in-product notification to specific people.

**Buttons** (`https://www.notion.com/help/buttons` and `/database-buttons`):
- Page-level buttons and a **Button property** on a database row. Each click runs a defined sequence of actions; can trigger database automations.

Database automations require a **paid plan**.

### 6.2 Webhook actions (out → external)

Docs: `https://www.notion.com/help/webhook-actions`. Available from buttons, database buttons, and database automations. Sends an HTTP POST to a URL with the row context as payload — ideal for triggering Make/Zapier/n8n flows or custom services.

### 6.3 Webhook subscriptions (in — Integration Webhooks API)

Docs: `https://developers.notion.com/reference/webhooks`, events at `/reference/webhooks-events-delivery`.

- Subscribe via an integration's Webhooks tab; verify endpoint ownership; choose events.
- Event types include `page.created`, `page.updated`, `page.deleted`, `database.schema_updated`, `data_source.schema_updated` (added in API `2025-09-03`), `comment.created`.
- **Delivery semantics**: secure HTTP POST; signed; up to **8 retries**, exponential backoff, final attempt ~24 h after the event.
- **Caveat**: no built-in dashboard for delivery status/logs. Use Hookdeck / Svix / your own logging.

### 6.4 No-code automation platforms

| Tool | Notes |
| --- | --- |
| **Zapier** | Largest connector ecosystem (6000+ apps). Best for cross-app flows where Notion is one node. `https://zapier.com/apps/notion/integrations`. |
| **Make** (formerly Integromat) | Visual scenario builder. Strong for branching/looping multi-step flows; popular in RevOps. `https://www.make.com/en/integrations/notion`. |
| **n8n** | Self-hostable, low-code; pricing per workflow execution rather than per step, so cheap for high-volume Notion workflows. Notion node docs: `https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.notion/`. |
| **Bardeen, Albato, Pipedream, Activepieces** | Other notable alternatives with Notion nodes. |

**Common workflow patterns**:
- Form submission (Tally/Typeform) → create Notion DB row.
- New row with status="Ready to Publish" → publish to Webflow/WordPress.
- Notion task "Done" → mark Linear/ClickUp issue closed.
- Slack message reaction → create Notion meeting note.
- Calendly booking → create CRM contact + meeting page.
- New PR/issue → create Notion tracking row.
- Recurring schedule → archive stale pages.

### 6.5 Native integrations (built into Notion)

| Integration | Help URL | What it does |
| --- | --- | --- |
| Slack | `https://www.notion.com/help/slack`, `https://www.notion.com/integrations/slack` | Link unfurls with AI summaries, share-to-channel from Notion, in-Slack permission prompts, database notifications to channels. Two notification modes: personal mentions and database-driven channel alerts. |
| GitHub | `https://www.notion.com/help/github`, `https://www.notion.com/integrations/github` | Paste a GitHub URL as a database to **sync repo issues/PRs**. PR-linked property, comment sync, status updates. One-way sync (GitHub → Notion). |
| Linear | `https://linear.app/integrations/notion` | Live previews for Linear issues/projects/views. Notion AI Connector for Linear lets you query a Linear workspace from Notion AI. |
| Figma | `https://www.notion.com/integrations/figma` | Inline preview/embed of Figma and FigJam files; updates automatically when designs change. |
| Google Drive, Microsoft 365, Jira, Asana, Salesforce, HubSpot, Zoom, Loom, Tableau, Amplitude, Mixpanel, Confluence, Dropbox, Box, ClickUp, monday.com, Intercom, Zendesk | `https://www.notion.com/integrations` | Connect Sync (search across third-party data from within Notion AI) plus per-tool embeds. Connect Sync is a 2024+ feature that lets Notion AI surface answers from connected SaaS tools. |

### 6.6 Notion AI capabilities and limits

- Reads up to **50 pages per query context** (raised from 20 in Jan 2026).
- Can search connected SaaS apps (Connect Sync).
- **Custom Agents** (Notion 3.3, Feb 2026): admins can build agents with system prompts, tool permissions, and triggers; Notion 3.5 (May 2026) added an external developer platform around this with the Agents SDK and Workers.
- **Pricing (May 2026+)**: Custom Agent credits are no longer free; $10 per 1,000 monthly credits on Business/Enterprise. Per-agent and workspace-level limits configurable.
- **Notion AI Meeting Notes** — record meetings; auto-transcribe and summarize into a database. `https://www.notion.com/help/guides/preserve-perfect-meeting-memory-with-ai-meeting-notes`.

---

## 7. Authoritative Content Creators and Blogs

Ranked roughly by how often their content is cited as canonical.

1. **Thomas Frank** — `https://thomasjfrank.com/`. The go-to long-form blog. Especially strong: databases, formulas, automations, building a personal dashboard. Templates: Ultimate Brain, Creator's Companion, PARA. YouTube: `https://www.youtube.com/c/Thomasfrank`.
2. **William Nutt / Notion VIP** — `https://www.notion.vip/`. The most-referenced independent reference. Notion A-to-Z subscription wraps tutorials and the Bulletproof template; Notion uses it to train support staff.
3. **Marie Poulin** — `https://mariepoulin.com/`, `https://notionmastery.com/`. The deepest resource for teams and agencies. Ivan Zhao (Notion CEO): "Marie is one of the most knowledgeable Notion users in the world."
4. **August Bradley** — YouTube + `https://www.yearzero.io/notion`. PPV methodology.
5. **Red Gregory** — `https://www.redgregory.com/notion`. Best free deep-dives on formulas, rollups, relations, and API tutorials.
6. **Easlo** — `https://www.easlo.co/`. The dominant template store for "clean, minimal, just works".
7. **Notion Mastery community** (Marie Poulin's program members publish under their own names — e.g. Ben Borowski, Frances Odera Matthews).
8. **Janice CK / `@slow_is_better`** — `https://slowisbetter.medium.com/`. Pages-vs-databases, intentional workspace design.
9. **Jennifer Chou / Vegan Tech Nomad** — life tracking, ADHD-friendly dashboards.
10. **Francesco D'Alessio (Keep Productive / Tool Finder)** — YouTube tool comparisons; longest-running productivity-tool channel.
11. **Matthias Frank** — `https://matthiasfrank.de/`. Update tracker plus Zettelkasten implementation.
12. **Simone Smerilli** — `https://www.simonesmerilli.com/`. Pragmatic walkthroughs of Notion product changes.
13. **Notion Everything** — `https://www.notioneverything.com/`. Curation and roundups.
14. **Gridfiti** — `https://gridfiti.com/`. Aesthetic templates and courses roundups.
15. **2sync, Super.so blog, ClickUp blog, Whalesync blog, Bullet.so blog** — solid SEO-driven roundups; useful for "best of" link discovery.
16. **Anh-Thu Bui** — `https://anhthubui.com/` + YouTube. Aesthetic, journaling-oriented Notion content.
17. **The Productive Engineer** — `https://theproductiveengineer.net/`. Tutorial-heavy, beginner-friendly.
18. **An Otioneer (substack)** — `https://anotioneer.substack.com/`. Formula and rollup recipes.

---

## 8. High-Quality Articles by Topic

### 8.1 Wiki / knowledge base

- `https://www.notion.com/help/guides/how-to-build-a-help-center-in-notion` — Notion's own guide.
- `https://www.notion.com/help/guides/category/wiki` — wiki feature deep dive.
- `https://www.notioneverything.com/blog/notion-wiki-verified-pages` — comprehensive guide to verified pages.
- `https://nira.com/notion-wiki/` — Nira's "Complete Guide to the Notion Wiki" (long-form, evergreen).
- `https://www.eesel.ai/blog/notion` — AI-powered knowledge base patterns.
- `https://bullet.so/blog/how-to-use-notion-as-knowledge-base/` — Notion as knowledge base.

### 8.2 Project management / sprints / tasks

- `https://www.notion.com/help/guides/getting-started-with-projects-and-tasks` — Notion's canonical projects + tasks setup.
- `https://www.notion.com/help/guides/product-engineering-notion-sprint-planning` — sprint planning for product/engineering.
- `https://www.notion.vip/insights/notion-projects-explained-with-crucial-recommendations` — William Nutt on Projects.
- `https://www.notion.com/help/guides/three-key-databases-for-teams-and-how-to-use-them` — the canonical Projects / Tasks / Docs trio for teams.
- `https://thomasjfrank.com/notion-database-automations-the-complete-guide/` — automating project workflows.

### 8.3 CRM

- `https://www.notion.com/templates/sales-crm` — Notion's first-party CRM template.
- `https://www.notion.com/templates/sales-pipeline-with-automations` — pipeline with Database Automations.
- `https://www.osdashboardhq.com/blog/best-notion-sales-pipeline-dashboards-crm-templates/` — roundup.
- `https://www.notioneverything.com/blog/notion-crm-templates` — 2026 roundup.

### 8.4 OKRs and goals

- `https://mooncamp.com/blog/okrs-in-notion` — comprehensive 2026 guide.
- `https://super.so/blog/how-to-create-and-manage-okrs-in-notion` — Super.so guide.
- `https://www.easlo.co/templates/okrs` — Easlo OKR template.
- `https://www.notion.com/templates/category/okr-tracker` — Notion's OKR template category.

### 8.5 Meeting notes

- `https://www.notion.com/help/guides/automate-work-repeating-database-templates` — repeating database templates.
- `https://www.notion.com/help/guides/preserve-perfect-meeting-memory-with-ai-meeting-notes` — AI Meeting Notes.
- `https://www.notion.vip/insights/supercharge-your-meetings-with-notion` — Notion VIP's meeting system.
- `https://www.notion.com/templates/essentials-recurring-meeting-notes` — Seyi Towolawi's recurring template.

### 8.6 Personal dashboards

- `https://thomasjfrank.com/how-to-build-a-personal-dashboard-in-notion/` — Thomas Frank's free dashboard guide.
- `https://gridfiti.com/notion-dashboard-templates/` — 40+ dashboard roundup.
- `https://www.notioneverything.com/blog/notion-dashboard-templates` — 2026 roundup.
- `https://www.notion.com/templates/category/personal-dashboards` — official category.

### 8.7 Databases / formulas / rollups

- `https://thomasjfrank.com/notion-databases-the-ultimate-beginners-guide/` — beginner database guide.
- `https://www.notion.com/help/guides/new-formulas-whats-changed` — Notion's Formulas 2.0 changes.
- `https://www.notion.vip/insights/notion-formulas-2-0-the-definitive-introduction` — definitive intro.
- `https://www.driveway.app/blog/the-ultimate-guide-to-notion-formulas-2-0` — long-form 2.0 guide.
- `https://anotioneer.substack.com/p/how-to-create-every-type-of-rollup` — every rollup type via formulas.
- `https://thomasjfrank.com/formulas/reference-properties-in-formulas/` — referencing properties.
- `https://notionmastery.com/everything-new-in-notion-formulas-2-0/` — Marie Poulin walkthrough.

### 8.8 Automations, webhooks, API

- `https://developers.notion.com/guides/data-apis/working-with-markdown-content` — official markdown ↔ blocks.
- `https://thomasjfrank.com/how-to-handle-notion-api-request-limits/` — handling rate limits.
- `https://hookdeck.com/webhooks/platforms/guide-to-notion-webhooks-features-and-best-practices` — webhooks best practices.
- `https://softwareengineeringstandard.com/2025/08/31/notion-webhooks/` — developer guide to Notion webhooks (2025).

---

## 9. Power-User Rules of Thumb

### 9.1 Page vs database

- **Page first**: new users should start with a single page and write everything down before reaching for databases. Use simple **tables** (not databases) when you just need a grid that doesn't need filtering, views, or relations.
- **Database when**: you'll want multiple views, filters, sorts, relations, or rollups; you have a *collection of like things*; you need automations.
- **Page when**: it's a unique document, a hub, or content that lives once.
- **William Nutt's framing**: *"Think like an app developer — organize all information in master databases at the bottom of a page; surface contextual filtered views above."* (Bulletproof / Notion VIP, `https://www.notion.vip/insights/golden-rules-of-notion`.)
- **Janice CK**: a database is overkill if you'd never sort, filter, or change view. The "screwdriver vs power drill" rule.

### 9.2 Nest databases vs link them

- **Linked databases** are the default — one source of truth, infinite filtered views. Do this 95% of the time.
- **Don't put a database inside a synced block**. Performance and behavior degrade. Instead, use a linked-database view on each destination page.
- **Sub-pages (children) inside database rows** are fine — every database row is itself a page and can hold its own content.

### 9.3 Avoid workspace mess

- **One master DB per concept** (Projects, Tasks, Docs/Notes, People/CRM, Meetings, Resources). Resist creating a new database every time you have a new use case — make a new *view* instead.
- **Prune properties**: *"If you don't filter or sort by a property at least once a week, delete it."* Power users keep ~6 useful properties, not 12 inconsistent ones.
- **Use teamspaces**, not deeply nested pages — keep 1–3 default teamspaces only.
- **Only workspace owners create teamspaces** (avoid sprawl).
- **Treat the home dashboard as the front door**. Star/favorite it. Use it to surface inboxes, today's tasks, this week's meetings.
- **Permission hygiene**: prefer "Can view" over "Can edit"; disable share-to-web on sensitive pages; disable cross-workspace duplication if you have lots of contributors.
- **Iterate**: a workspace is never "done"; review quarterly and prune.

### 9.4 Icons, covers, color

- Cover image: **1500 × 600** desktop, 5:2 aspect. Keep critical artwork inside the central **1170 × 230** region. <5 MB.
- Keep the **left third of the cover quiet** so the icon + title overlay reads cleanly.
- **One icon family** per workspace (all emoji, or all custom SVGs from a single set like Fountn) — mixing styles is the fastest way to look amateur.
- **Color discipline**: pick 2–3 *property* colors (status, priority) and keep them consistent across databases. Notion's "use colors for meaning, not decoration" is a common refrain.

### 9.5 Toggle vs callout vs quote vs synced block

| Pattern | Use when |
| --- | --- |
| **Heading (H1/H2/H3)** | Document structure; navigable in the outline view. Toggle headings exist if you want to fold a whole section. |
| **Toggle** | Collapsible details — FAQs, "click to expand", reducing visual noise on long pages. *Shortcut: `>` + space.* |
| **Callout** | Highlight a tip, warning, or important fact with an emoji and background tint. Best for "read this once". Supports child blocks since 2023. |
| **Quote** | Pulled quotes, testimonials, marker for verbatim text. *Shortcut: `"` + space.* |
| **Synced block** | Truly mirrored content — a banner, a status note, a footer — that must update everywhere when changed in one place. Don't put databases inside. |
| **Linked database view** | Show a filtered slice of an existing database on another page. The right tool 95% of the time when you want "the same data here too". |
| **Columns** | Side-by-side layout. Avoid more than 3 columns; mobile collapses them anyway. |
| **Divider / Heading separators** | Sparingly, for visual rhythm on long pages. Don't replace good heading structure. |

### 9.6 Database design

- **Three properties everyone needs**: a Status (single-select with explicit lifecycle), a Date (created vs due — keep them distinct), an Assignee (Person property, not text).
- **Use relations, not duplication**. If "Project" appears as a property on Tasks and again on Meetings, both should *relate* to the Projects database — never store as text.
- **Rollups + Formulas 2.0**: in modern Notion you rarely need raw rollups — `prop()` on a relation reaches into the related database directly. Use `let`/`lets` to factor complex formulas.
- **Templates inside databases**: define one per archetype (e.g. weekly review, 1:1, brief). Use *repeating* templates for recurring meetings.

### 9.7 API design rules for agents

- **Always set `Notion-Version` explicitly** — don't rely on the default; pin to the version your code was written against.
- **Always handle 429**: respect `Retry-After`. Three requests/sec average is the soft limit.
- **Chunk children**: max 100 per call, 1,000 per page, payload ≤ 500 KB, rich text ≤ 2,000 chars.
- **Prefer the `markdown` field** on `POST /v1/pages` for prose-heavy creation; fall back to block JSON for structured content.
- **Webhooks** are now (2024+) the right way to react to changes — replaces polling. But add your own delivery logging; Notion doesn't show webhook delivery state.
- **Idempotency**: Notion has no idempotency keys; client must dedupe by checking for an existing page with a known external ID property before creating.
- **The 2025-09-03 data-source split**: databases now have one or more data sources. New code should query data sources directly; old code targeting the database ID still works in compatibility mode.

---

## 10. Quick-Reference Index

**Need to point a user to ONE link for...**

| Topic | Link |
| --- | --- |
| Notion API docs (top) | `https://developers.notion.com/` |
| Markdown ↔ Notion blocks (API) | `https://developers.notion.com/guides/data-apis/working-with-markdown-content` |
| API rate limits | `https://developers.notion.com/reference/request-limits` |
| Notion JS SDK | `https://github.com/makenotion/notion-sdk-js` |
| Notion Python SDK | `https://github.com/ramnes/notion-sdk-py` |
| Markdown → Notion blocks (Node) | `https://github.com/tryfabric/martian` |
| Notion → Markdown (Node) | `https://github.com/souvikinator/notion-to-md` |
| Notion → Markdown (Python) | `https://github.com/echo724/notion2md` |
| React renderer | `https://github.com/NotionX/react-notion-x` |
| Next.js Notion site | `https://github.com/transitive-bullshit/nextjs-notion-starter-kit` |
| Templates marketplace | `https://www.notion.com/templates` |
| Help center | `https://www.notion.com/help` |
| Notion Academy | `https://www.notion.so/help/notion-academy` |
| Database automations | `https://www.notion.com/help/database-automations` |
| Webhooks (integration) | `https://developers.notion.com/reference/webhooks` |
| Best free formulas / API tutorials | `https://www.redgregory.com/notion` |
| Power-user golden rules | `https://www.notion.vip/insights/golden-rules-of-notion` |
| Team workflow course | `https://notionmastery.com/` |
| Best-selling all-in-one template | `https://thomasjfrank.com/brain/` |
| Life-OS methodology | `https://www.yearzero.io/notion` (PPV) |
| PARA method (Notion-flavored) | `https://www.buildingasecondbrain.com/notion-template` |
| Bulletproof workspace framework | `https://bulletproof.notion.vip/` |
| Reddit community | `https://www.reddit.com/r/Notion/` |
| Subreddit for free templates | `https://www.reddit.com/r/FreeNotionTemplates/` |

---

## 11. Sources

- [Notion Developer Platform](https://developers.notion.com/)
- [Notion API request limits](https://developers.notion.com/reference/request-limits)
- [Working with markdown content (Notion Docs)](https://developers.notion.com/guides/data-apis/working-with-markdown-content)
- [Notion Webhooks reference](https://developers.notion.com/reference/webhooks)
- [Webhooks event types & delivery](https://developers.notion.com/reference/webhooks-events-delivery)
- [Notion 3.5: Developer Platform release notes](https://www.notion.com/releases/2026-05-13)
- [Notion 3.3: Custom Agents](https://www.notion.com/releases/2026-02-24)
- [Custom Agent controls for admins](https://www.notion.com/releases/2026-05-05)
- [Mail & Calendar in settings](https://www.notion.com/releases/2026-04-17)
- [makenotion/notion-sdk-js (GitHub)](https://github.com/makenotion/notion-sdk-js)
- [makenotion/notion-agents-sdk-js (GitHub)](https://github.com/makenotion/notion-agents-sdk-js)
- [@notionhq/client on npm](https://www.npmjs.com/package/@notionhq/client)
- [ramnes/notion-sdk-py (GitHub)](https://github.com/ramnes/notion-sdk-py)
- [notion-sdk-py docs](https://ramnes.github.io/notion-sdk-py/)
- [jomei/notionapi (Go)](https://github.com/jomei/notionapi)
- [kjk/notionapi (Go)](https://pkg.go.dev/github.com/kjk/notionapi)
- [notion-sdk Rust crate](https://docs.rs/notion-sdk)
- [souvikinator/notion-to-md](https://github.com/souvikinator/notion-to-md)
- [tryfabric/martian](https://github.com/tryfabric/martian)
- [tryfabric/markdown-to-notion (GitHub Action)](https://github.com/tryfabric/markdown-to-notion)
- [echo724/notion2md](https://github.com/echo724/notion2md)
- [alvinwan/notion2markdown](https://github.com/alvinwan/notion2markdown)
- [brittonhayes/notionmd](https://github.com/brittonhayes/notionmd)
- [roelmagdaleno/markdown-to-notion-blocks](https://github.com/roelmagdaleno/markdown-to-notion-blocks)
- [rieg-ec/md_to_notion](https://github.com/rieg-ec/md_to_notion)
- [aia-ops/mcp-mdnotion](https://github.com/aia-ops/mcp-mdnotion)
- [MerkulovDaniil/notion4ever](https://github.com/MerkulovDaniil/notion4ever)
- [yannbolliger/notion-exporter](https://github.com/yannbolliger/notion-exporter)
- [dwarvesf/notion-export-markdown](https://github.com/dwarvesf/notion-export-markdown)
- [NotionX/react-notion-x](https://github.com/NotionX/react-notion-x)
- [transitive-bullshit/nextjs-notion-starter-kit](https://github.com/transitive-bullshit/nextjs-notion-starter-kit)
- [Super.so](https://super.so/)
- [Potion](https://potion.so/)
- [HostNotion](https://hostnotion.co/)
- [Simple.ink](https://www.simple.ink/)
- [HelpKit](https://www.helpkit.so/)
- [LangChain Notion DB loader](https://python.langchain.com/docs/integrations/document_loaders/notion/)
- [Notion Templates Marketplace](https://www.notion.com/templates)
- [Getting started as a template creator on Marketplace](https://www.notion.com/help/guides/getting-started-as-a-template-creator-on-marketplace)
- [Selling templates on Marketplace](https://www.notion.com/help/selling-on-marketplace)
- [Notion Academy](https://www.notion.so/help/notion-academy)
- [Notion Help Center home](https://www.notion.com/help)
- [Database automations](https://www.notion.com/help/database-automations)
- [Webhook actions](https://www.notion.com/help/webhook-actions)
- [Slack integration help](https://www.notion.com/help/slack)
- [GitHub integration help](https://www.notion.com/help/github)
- [Notion + Linear](https://linear.app/integrations/notion)
- [Notion + Figma](https://www.notion.com/integrations/figma)
- [Notion Sites pricing](https://www.notion.com/help/notion-sites-availability-and-pricing)
- [Connect a custom domain with Notion Sites](https://www.notion.com/help/connect-a-custom-domain-with-notion-sites)
- [Teamspaces overview](https://www.notion.com/help/intro-to-teamspaces)
- [Three key databases for teams](https://www.notion.com/help/guides/three-key-databases-for-teams-and-how-to-use-them)
- [Wiki help guides](https://www.notion.com/help/guides/category/wiki)
- [Page icons & covers](https://www.notion.com/help/guides/page-icons-and-covers)
- [Repeating database templates](https://www.notion.com/help/guides/automate-work-repeating-database-templates)
- [AI Meeting Notes](https://www.notion.com/help/guides/preserve-perfect-meeting-memory-with-ai-meeting-notes)
- [Thomas Frank — Ultimate Brain](https://thomasjfrank.com/brain/)
- [Thomas Frank — Personal dashboard guide](https://thomasjfrank.com/how-to-build-a-personal-dashboard-in-notion/)
- [Thomas Frank — Database automations guide](https://thomasjfrank.com/notion-database-automations-the-complete-guide/)
- [Thomas Frank — Rate limits guide](https://thomasjfrank.com/how-to-handle-notion-api-request-limits/)
- [Marie Poulin — Notion Mastery](https://notionmastery.com/)
- [Marie Poulin — Workflow design](https://mariepoulin.com/)
- [Notion VIP — Golden Rules](https://www.notion.vip/insights/golden-rules-of-notion)
- [Notion VIP — Formulas 2.0 intro](https://www.notion.vip/insights/notion-formulas-2-0-the-definitive-introduction)
- [Notion VIP — Synced blocks explained](https://www.notion.vip/insights/notion-explained-synced-blocks)
- [Notion VIP — Supercharge meetings](https://www.notion.vip/insights/supercharge-your-meetings-with-notion)
- [The Bulletproof Workspace](https://bulletproof.notion.vip/)
- [Notion A-to-Z](https://www.notion.vip/a-to-z)
- [August Bradley — Year Zero / Notion](https://www.yearzero.io/notion)
- [August Bradley — Notion Life Design course](https://www.notionlifedesign.com/)
- [Red Gregory — Notion articles](https://www.redgregory.com/notion)
- [Red Gregory — Substack](https://redgregory.substack.com/)
- [Easlo — templates](https://www.easlo.co/templates)
- [Easlo — free templates](https://www.easlo.co/free-notion-templates)
- [Building a Second Brain — PARA](https://www.buildingasecondbrain.com/para)
- [Building a Second Brain — Notion template](https://www.buildingasecondbrain.com/notion-template)
- [Thomas Frank — PARA template](https://thomasjfrank.com/templates/para-method-template-for-notion/)
- [Matthias Frank — Zettelkasten for Notion](https://matthiasfrank.de/en/zettelkasten-for-notion/)
- [Notion Community](https://www.notion.so/community)
- [Hookdeck — Guide to Notion Webhooks](https://hookdeck.com/webhooks/platforms/guide-to-notion-webhooks-features-and-best-practices)
- [Notion Webhooks: A Complete Guide for Developers (2025)](https://softwareengineeringstandard.com/2025/08/31/notion-webhooks/)
- [n8n Notion node docs](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.notion/)
- [Make + Notion](https://www.make.com/en/integrations/notion)
- [Zapier Notion integrations](https://zapier.com/apps/notion/integrations)
- [Notion API Updates 2026 (Fazm)](https://fazm.ai/blog/notion-api-updates-2026)
- [Notion AI Features 2026 (Fazm)](https://fazm.ai/blog/notion-ai-features-2026)
- [Notion API Rate Limits 2026 (Fazm)](https://fazm.ai/blog/notion-api-rate-limits-2026)
- [Mooncamp — OKRs in Notion 2026](https://mooncamp.com/blog/okrs-in-notion)
- [Super.so — OKRs in Notion](https://super.so/blog/how-to-create-and-manage-okrs-in-notion)
- [Notion Everything — Wiki / verified pages](https://www.notioneverything.com/blog/notion-wiki-verified-pages)
- [Nira — Complete Guide to the Notion Wiki](https://nira.com/notion-wiki/)
- [eesel — AI-powered Notion knowledge base](https://www.eesel.ai/blog/notion)
- [Overflow Design — Notion cover size](https://www.overflow.design/notion-cover-size/)
- [2sync — Notion covers (2026)](https://2sync.com/blog/notion-covers)
- [Fountn — Notion icons](https://fountn.design/resource/notion-icons-4550-notion-style-illustrations-icons-and-wallpapers/)
- [Notion-VIP — Pushing Notion to the Limits](https://notionmastery.com/pushing-notion-to-the-limits/)
- [An Otioneer — Every Type of Rollup](https://anotioneer.substack.com/p/how-to-create-every-type-of-rollup)
