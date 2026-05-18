# Research Synthesis: Beautiful Notion Systems

This research turns current Notion capabilities and high-quality marketplace
patterns into operating rules for Hermes, OpenClaw, and other agents.

## Current Notion Capability Baseline

Official Notion docs confirm that the API can create and update polished
Notion-native structure, but not arbitrary web design. The API represents page
content as blocks and supports many layout/content primitives, while unsupported
UI-only block types are returned as `unsupported`.

Useful design primitives available through Notion-native construction:

- Page icons and covers as top-level page fields.
- Headings, toggle headings, paragraphs, lists, quotes, callouts, dividers,
  tables, table of contents, images, files, embeds, code, synced blocks, tabs,
  child pages, and child databases.
- Database/data-source schemas with properties, page templates, and views.
- Views including table, board, list, calendar, timeline, gallery, form, chart,
  map, and dashboard in the newer API surface.

Important constraints:

- No arbitrary CSS, custom fonts, pixel spacing, or fully custom components.
- Some Notion UI blocks are not API-creatable.
- Append-block requests must be batched and cannot rearrange existing blocks as a
  layout engine would.
- Publishing and Notion Site customization are largely Notion UI/admin workflows,
  so agents must validate published URLs and use browser/UI help where needed.

Sources:

- Notion block reference: https://developers.notion.com/reference/block
- Notion page property values: https://developers.notion.com/reference/page-property-values
- Working with views: https://developers.notion.com/guides/data-apis/working-with-views
- Notion CLI data sources: https://developers.notion.com/cli/guides/data-sources
- Publish a Notion Site: https://www.notion.com/help/public-pages-and-web-publishing
- Edit and customize Notion Sites: https://www.notion.com/en-gb/help/edit-and-customize-your-notion-sites

## What Premium Notion Systems Have In Common

The strongest Notion systems are not just nice-looking pages. They combine
visual hierarchy, information architecture, and maintainable databases.

Observed patterns from Notion marketplace/client-portal/dashboard research:

- A single home or hub page anchors the system.
- The first viewport gives orientation and a next action.
- Core areas are limited to a small set: Projects, Tasks, Clients, Docs, SOPs,
  Resources, Decisions, Archive.
- Databases are centralized, while pages show filtered linked views for each
  audience or workflow.
- Internal work and client-facing surfaces are separated.
- Gallery cards show only high-signal properties.
- Templates make repeated records look consistent.
- Reference material lives lower on the page or inside toggles, not in the way of
  active work.

Useful sources and inspiration points:

- Client portal templates: https://www.notion.com/templates/category/client-portal
- Dashboard template collection: https://www.notion.com/templates/collections/a-dashboard-for-every-need
- Notion templates marketplace: https://www.notion.com/templates

## Design Principles For Agents

1. Design before filling

Agents should choose the page archetype, audience, and main actions before
generating blocks. A beautiful system starts as a clear skeleton.

2. Make the first viewport excellent

The top of the page should include the title, icon, cover, a concise orientation
callout, and either a command center or table of contents.

3. Structure is the design

In Notion, polish comes from section rhythm, database views, columns, callouts,
and page hierarchy. Avoid trying to mimic a custom website.

4. Color is semantic

Use a small palette and assign colors to meaning. Blue means context, green
means live/approved, yellow means review/caution, red means risk/blocker, gray
means reference/archive.

5. Databases are products

A database must have a job. Properties, views, filters, sorts, and templates are
part of the user experience.

6. Public pages need publishing discipline

For Notion Sites, the published link is the deliverable. Public subpages are
published by default, so agents must inspect what is nested under a public page
before sending.

7. Beauty should make work easier

If a decorative element slows scanning or adds maintenance, remove it.

## Recommended Agent Workflow

1. Classify the deliverable.
2. Pick a page archetype.
3. Define audience, primary action, and publish/publicness.
4. Sketch the first viewport and information architecture.
5. Create the page skeleton.
6. Add databases/views/templates if the page is a system.
7. Add content and media.
8. Run the QA rubric.
9. Publish when expected.
10. Run Publisher Agent validation and return only the published final link.

## Where Agentic Notion Work Can Improve Further

- Create reusable Notion page skeletons for each archetype.
- Maintain a small approved icon and cover-image style library.
- Add a pre-publish crawler that checks public subpage exposure.
- Add screenshot QA using Browser Use for published Notion Sites.
- Store before/after quality scores for agent-created Notion work.
