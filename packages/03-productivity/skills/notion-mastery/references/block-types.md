# Block Types Cheatsheet

Quick-lookup payload shapes for every Notion block type. For deep details (children behavior, version differences, edge cases), see `api-reference.md` §1.

Every block when **creating** needs only `{ "type": "<x>", "<x>": { ...payload... } }`. Color defaults to `"default"` and can be omitted.

## Common building blocks

### Rich text (used by most blocks)

```json
{
  "type": "text",
  "text": { "content": "Hello", "link": null },
  "annotations": {
    "bold": false, "italic": false, "strikethrough": false,
    "underline": false, "code": false, "color": "default"
  }
}
```

Annotations are optional — omit any falsy fields. Colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`, plus the `_background` variants (e.g. `blue_background`).

**Hard rule:** each text element's `content` is capped at 2000 chars. Long strings must be split across multiple text elements in the same rich_text array. Use `scripts/chunk_rich_text.py`.

### Mentions (inside rich_text)

```json
{ "type": "mention", "mention": { "type": "page", "page": { "id": "uuid" } } }
{ "type": "mention", "mention": { "type": "user", "user": { "id": "uuid" } } }
{ "type": "mention", "mention": { "type": "date", "date": { "start": "2026-05-16", "end": null } } }
{ "type": "mention", "mention": { "type": "database", "database": { "id": "uuid" } } }
```

## Text blocks

### `paragraph`
```json
{ "type": "paragraph", "paragraph": {
  "rich_text": [ { "type": "text", "text": { "content": "Body copy." } } ],
  "color": "default"
} }
```
Supports `children`. Use for body content; an empty paragraph is your spacing primitive.

### `heading_1`, `heading_2`, `heading_3` (and `heading_4` on 2026-04-01+)
```json
{ "type": "heading_2", "heading_2": {
  "rich_text": [ { "type": "text", "text": { "content": "Section" } } ],
  "color": "default",
  "is_toggleable": false
} }
```
`is_toggleable: true` makes a collapsible heading. Children only allowed when toggleable.

**Convention:** don't use `heading_1` in body content. The page title is implicitly H1.

### `quote`
Same shape as paragraph but with a left-border treatment. Use sparingly — best for actual quotations or pull-out emphasis.

### `callout`
```json
{ "type": "callout", "callout": {
  "rich_text": [ { "type": "text", "text": { "content": "Heads up." } } ],
  "icon": { "type": "emoji", "emoji": "💡" },
  "color": "gray_background"
} }
```
Supports `children`. `icon` can be `{ "type": "external", "external": { "url": "..." } }` or `{ "type": "emoji", "emoji": "💡" }`. The most useful design block — see `design-patterns.md` §2.

## Lists

### `bulleted_list_item`, `numbered_list_item`
```json
{ "type": "bulleted_list_item", "bulleted_list_item": {
  "rich_text": [ { "type": "text", "text": { "content": "First item" } } ],
  "color": "default"
} }
```
Notion renders consecutive list items as a single list. Supports `children` (nesting).

### `to_do`
```json
{ "type": "to_do", "to_do": {
  "rich_text": [ { "type": "text", "text": { "content": "Buy milk" } } ],
  "checked": false,
  "color": "default"
} }
```
Supports `children` (sub-tasks). For database-tracked tasks, prefer a real database.

### `toggle`
```json
{ "type": "toggle", "toggle": {
  "rich_text": [ { "type": "text", "text": { "content": "Click to expand" } } ],
  "color": "default",
  "children": [ { "type": "paragraph", "paragraph": { "rich_text": [...] } } ]
} }
```
The single best block for progressive disclosure. Use for FAQs, optional context, anything that 80% of readers won't need.

## Structural / layout

### `divider`
```json
{ "type": "divider", "divider": {} }
```
Empty payload. Use sparingly — between major sections only.

### `breadcrumb`
```json
{ "type": "breadcrumb", "breadcrumb": {} }
```
Renders the page's ancestor trail. Useful at the top of deep pages.

### `table_of_contents`
```json
{ "type": "table_of_contents", "table_of_contents": { "color": "default" } }
```
Auto-generated from headings on the page. Place near the top of long pages.

### `column_list` and `column`
```json
{ "type": "column_list", "column_list": { "children": [
  { "type": "column", "column": { "children": [ /* blocks */ ] } },
  { "type": "column", "column": { "children": [ /* blocks */ ] } }
] } }
```
`column` only valid inside `column_list`. Minimum 2 columns; 4 is usually too many. Don't put dense prose in columns — they don't reflow well on mobile.

### `synced_block`
```json
{ "type": "synced_block", "synced_block": {
  "synced_from": null,
  "children": [ /* original content */ ]
} }
```
Original block: `synced_from: null` + children. Sync target: `synced_from: { block_id: "<original-id>" }` + no children. Use for nav bars, repeated callouts, anything you want to update in one place.

## Media and embeds

### `image`, `video`, `audio`, `file`, `pdf`
All have the same shape:
```json
{ "type": "image", "image": {
  "type": "external",
  "external": { "url": "https://example.com/img.png" },
  "caption": [ { "type": "text", "text": { "content": "An image" } } ]
} }
```
For Notion-hosted files use `{ "type": "file", "file": { "url": "...", "expiry_time": "..." } }` — but hosted files require File Upload API; external URLs are simpler.

### `bookmark`, `embed`, `link_preview`
```json
{ "type": "bookmark", "bookmark": {
  "url": "https://example.com",
  "caption": []
} }
```
- `bookmark`: rendered as a card preview.
- `embed`: renders the URL inline (iframe-style). Many domains aren't allowed.
- `link_preview`: read-only; Notion creates these when it can auto-detect a known integration (GitHub, Linear, etc.).

## Code and math

### `code`
```json
{ "type": "code", "code": {
  "rich_text": [ { "type": "text", "text": { "content": "console.log('hi')" } } ],
  "language": "javascript",
  "caption": []
} }
```
Common `language` values: `javascript`, `typescript`, `python`, `bash`, `shell`, `sql`, `json`, `yaml`, `markdown`, `html`, `css`, `go`, `rust`, `java`, `kotlin`, `swift`, `ruby`, `php`, `plain text`, `mermaid`. Full list in `api-reference.md` §1.4.

### `equation`
```json
{ "type": "equation", "equation": { "expression": "E = mc^2" } }
```
LaTeX syntax. Inline equations live inside rich_text as `{ "type": "equation", "equation": { "expression": "..." } }`.

## Tables (simple, not database)

### `table` + `table_row`
```json
{ "type": "table", "table": {
  "table_width": 3,
  "has_column_header": true,
  "has_row_header": false,
  "children": [
    { "type": "table_row", "table_row": { "cells": [
      [ { "type": "text", "text": { "content": "Col 1" } } ],
      [ { "type": "text", "text": { "content": "Col 2" } } ],
      [ { "type": "text", "text": { "content": "Col 3" } } ]
    ] } }
  ]
} }
```
Each cell is a `rich_text` array. Row count = number of `table_row` children. **Use simple tables for static reference data; use databases for anything that needs filtering, sorting, or relations.**

## Page references

### `child_page`, `child_database`
Read-only block types — you don't create these directly. They appear in a parent page's children list when a subpage or inline database exists.

### `link_to_page`
```json
{ "type": "link_to_page", "link_to_page": {
  "type": "page_id",
  "page_id": "uuid"
} }
```
Variants: `page_id`, `database_id`, `comment_id`. Renders as a clickable mention block.

## Block creation patterns

### Pattern 1: A simple page
```json
{
  "parent": { "page_id": "parent-uuid" },
  "icon": { "type": "emoji", "emoji": "📝" },
  "cover": { "type": "external", "external": { "url": "https://images.unsplash.com/..." } },
  "properties": { "title": { "title": [ { "text": { "content": "Page title" } } ] } },
  "children": [
    { "type": "callout", "callout": { "rich_text": [...], "icon": {...}, "color": "gray_background" } },
    { "type": "heading_2", "heading_2": { "rich_text": [{"text":{"content":"Section"}}] } },
    { "type": "paragraph", "paragraph": { "rich_text": [{"text":{"content":"Body."}}] } }
  ]
}
```

### Pattern 2: A page in a database
```json
{
  "parent": { "database_id": "db-uuid" },
  "icon": { "type": "emoji", "emoji": "🚀" },
  "properties": {
    "Title": { "title": [ { "text": { "content": "Q3 planning" } } ] },
    "Status": { "status": { "name": "In Progress" } },
    "Owner": { "people": [ { "id": "user-uuid" } ] },
    "Due Date": { "date": { "start": "2026-06-30" } },
    "Tags": { "multi_select": [ { "name": "engineering" }, { "name": "Q3" } ] }
  },
  "children": [ /* page body blocks */ ]
}
```

### Pattern 3: 2-column dashboard layout
```json
{
  "type": "column_list",
  "column_list": { "children": [
    { "type": "column", "column": { "children": [
      { "type": "heading_3", "heading_3": { "rich_text": [{"text":{"content":"Quick Links"}}] } },
      { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [...] } }
    ] } },
    { "type": "column", "column": { "children": [
      { "type": "heading_3", "heading_3": { "rich_text": [{"text":{"content":"This Week"}}] } },
      { "type": "to_do", "to_do": { "rich_text": [...], "checked": false } }
    ] } }
  ] }
}
```

## What you can't do (block-level)

- **Insert in the middle of a children list.** Notion only supports append. To "insert", delete subsequent blocks and re-append.
- **Move a block to a different parent.** Same workaround: delete and recreate.
- **Set a page-level template via API.** Database templates aren't accessible — you have to construct the equivalent JSON yourself.
- **Programmatically change "wide mode" / full-page layout settings.** No API for layout toggles.
- **Get current user's selection or cursor position.** Not exposed.
- **Listen to real-time edits.** Use webhooks (introduced in late 2024) for change notifications, not real-time presence.
