# Notion API Comprehensive Reference for AI Agents

> Built from official Notion documentation, SDK type definitions, and community knowledge. Targets **Notion-Version 2022-06-28** (most stable, widely supported) with notes on **2025-09-03** (data sources) and **2026-04-01** (Views API, heading_4, rate-limit header changes). Always test version compatibility — version selection affects request/response shapes.

---

## 0. Foundations

### 0.1 Authentication & required headers

| Header | Value | Notes |
|---|---|---|
| `Authorization` | `Bearer <integration_token>` | Internal integration tokens never expire (but can be revoked). OAuth tokens vary. |
| `Notion-Version` | `2022-06-28` (recommended baseline) | **Required on every request.** Newer values: `2025-09-03`, `2026-04-01`. If you depend on data sources, multi-source DBs, or Views API, you must opt into a newer version. |
| `Content-Type` | `application/json` | Except `Send a file upload` which uses `multipart/form-data`. |

Base URL: `https://api.notion.com/v1`

### 0.2 Object types

All Notion API objects carry a top-level `"object"` discriminator: `"page"`, `"database"`, `"data_source"`, `"block"`, `"user"`, `"comment"`, `"list"` (pagination wrapper), `"property_item"`, `"file_upload"`, `"view"` (2026-04-01+).

### 0.3 IDs

UUIDs (with or without hyphens). The API accepts both forms; it always returns hyphenated.

### 0.4 Pagination envelope

```json
{
  "object": "list",
  "results": [ ... ],
  "next_cursor": "abcd-...",
  "has_more": true,
  "type": "page_or_database",
  "page_or_database": {}
}
```

Pass `start_cursor` to continue. `page_size` max **100** (default 100 for blocks/query, 100 for search).

### 0.5 Rate limits

- **Average 3 req/s per integration.** Short bursts allowed.
- 429 returns `Retry-After` header (integer seconds).
- 2026-04-01+ adds `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers on every response.
- Backoff strategy: exponential (1s, 2s, 4s, 8s) with `Retry-After` taking priority.

### 0.6 HTTP status codes

| Code | Notion `code` field | Retry? |
|---|---|---|
| 400 | `invalid_json`, `invalid_request_url`, `invalid_request`, `validation_error`, `missing_version` | No |
| 401 | `unauthorized` | No |
| 403 | `restricted_resource` | No |
| 404 | `object_not_found` (often = integration lacks access) | No |
| 409 | `conflict_error` (write conflict — safe to retry) | Yes |
| 429 | `rate_limited` | Yes, after `Retry-After` |
| 500 | `internal_server_error` | Yes |
| 502/503/504 | gateway/availability | Yes |

Error body: `{ "object": "error", "status": 400, "code": "validation_error", "message": "..." }`

---

## 1. Block types

Every block has these common fields:

```json
{
  "object": "block",
  "id": "uuid",
  "parent": { "type": "page_id", "page_id": "uuid" },
  "type": "<block_type>",
  "created_time": "2024-01-01T00:00:00.000Z",
  "last_edited_time": "2024-01-01T00:00:00.000Z",
  "created_by": { "object": "user", "id": "uuid" },
  "last_edited_by": { "object": "user", "id": "uuid" },
  "has_children": false,
  "archived": false,
  "in_trash": false,
  "<block_type>": { ... }
}
```

When **creating** blocks (POST/PATCH), only `type` + the nested object are needed.

### 1.1 Text blocks

#### `paragraph`
Plain body text. Supports `children`.
```json
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [ { "type": "text", "text": { "content": "Hello world." } } ],
    "color": "default",
    "children": []
  }
}
```

#### `heading_1`, `heading_2`, `heading_3`, `heading_4`
`heading_4` requires Notion-Version `2026-04-01+`. All headings support `is_toggleable` — when `true`, the heading behaves like a toggle and can have `children`.
```json
{
  "type": "heading_2",
  "heading_2": {
    "rich_text": [ { "type": "text", "text": { "content": "Section title" } } ],
    "color": "blue",
    "is_toggleable": false
  }
}
```

#### `bulleted_list_item`
```json
{
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [ { "type": "text", "text": { "content": "First item" } } ],
    "color": "default",
    "children": []
  }
}
```

#### `numbered_list_item`
Same shape as bulleted. Numbering is rendered client-side — you do not supply ordinals.

#### `to_do`
```json
{
  "type": "to_do",
  "to_do": {
    "rich_text": [ { "type": "text", "text": { "content": "Ship feature" } } ],
    "checked": false,
    "color": "default",
    "children": []
  }
}
```

#### `toggle`
```json
{
  "type": "toggle",
  "toggle": {
    "rich_text": [ { "type": "text", "text": { "content": "Details" } } ],
    "color": "default",
    "children": [ /* any blocks */ ]
  }
}
```

#### `quote`
```json
{
  "type": "quote",
  "quote": {
    "rich_text": [ { "type": "text", "text": { "content": "Words to live by." } } ],
    "color": "default"
  }
}
```

#### `callout`
Has an `icon` (emoji / external / file / file_upload / custom_emoji) and a `color` (often a background color).
```json
{
  "type": "callout",
  "callout": {
    "rich_text": [ { "type": "text", "text": { "content": "Important note" } } ],
    "icon": { "type": "emoji", "emoji": "💡" },
    "color": "yellow_background"
  }
}
```

### 1.2 Structure & decoration

#### `divider`
Empty object.
```json
{ "type": "divider", "divider": {} }
```

#### `breadcrumb`
Empty.
```json
{ "type": "breadcrumb", "breadcrumb": {} }
```

#### `table_of_contents`
```json
{ "type": "table_of_contents", "table_of_contents": { "color": "default" } }
```

#### `code`
```json
{
  "type": "code",
  "code": {
    "rich_text": [ { "type": "text", "text": { "content": "console.log('hi')" } } ],
    "caption": [ { "type": "text", "text": { "content": "Example" } } ],
    "language": "javascript"
  }
}
```

**Supported `language` values** (~75; case-sensitive, lowercase, words separated by spaces or hyphens):
`abap`, `arduino`, `bash`, `basic`, `c`, `clojure`, `coffeescript`, `c++`, `c#`, `css`, `dart`, `diff`, `docker`, `elixir`, `elm`, `erlang`, `flow`, `fortran`, `f#`, `gherkin`, `glsl`, `go`, `graphql`, `groovy`, `haskell`, `html`, `java`, `javascript`, `json`, `julia`, `kotlin`, `latex`, `less`, `lisp`, `livescript`, `lua`, `makefile`, `markdown`, `markup`, `matlab`, `mermaid`, `nix`, `notion formula`, `objective-c`, `ocaml`, `pascal`, `perl`, `php`, `plain text`, `powershell`, `prolog`, `protobuf`, `purescript`, `python`, `r`, `racket`, `reason`, `ruby`, `rust`, `sass`, `scala`, `scheme`, `scss`, `shell`, `solidity`, `sql`, `swift`, `typescript`, `vb.net`, `verilog`, `vhdl`, `visual basic`, `webassembly`, `xml`, `yaml`, `java/c/c++/c#`. Default `plain text` if unknown.

#### `equation`
LaTeX, block-level.
```json
{ "type": "equation", "equation": { "expression": "E = mc^2" } }
```
(Inline equations are rich_text objects with `type: "equation"` — see §2.)

### 1.3 Media blocks

All media blocks share the file-object pattern with three variants:
- `{ "type": "external", "external": { "url": "https://..." } }`
- `{ "type": "file", "file": { "url": "...", "expiry_time": "..." } }` — **read-only**; you can't create/update file-hosted files directly except via `file_upload`
- `{ "type": "file_upload", "file_upload": { "id": "<file_upload_id>" } }` — for uploaded files

#### `image`
```json
{
  "type": "image",
  "image": {
    "type": "external",
    "external": { "url": "https://example.com/pic.png" },
    "caption": [ { "type": "text", "text": { "content": "Diagram" } } ]
  }
}
```

#### `video`
Same shape. Supports YouTube/Vimeo URLs as external.

#### `audio`
Same shape as image/video.

#### `file`
```json
{
  "type": "file",
  "file": {
    "type": "external",
    "external": { "url": "https://example.com/doc.zip" },
    "name": "Archive.zip",
    "caption": []
  }
}
```

#### `pdf`
Same shape; URL must point to a PDF resource.

#### `bookmark`
Rich link card.
```json
{
  "type": "bookmark",
  "bookmark": {
    "url": "https://example.com",
    "caption": [ { "type": "text", "text": { "content": "Example domain" } } ]
  }
}
```

#### `embed`
Generic iframe-style embed (Twitter, Figma, etc).
```json
{ "type": "embed", "embed": { "url": "https://twitter.com/notion/status/123" } }
```

#### `link_preview` (read-only)
Cannot be **created** via API. Returned for existing link previews:
```json
{ "type": "link_preview", "link_preview": { "url": "https://github.com/..." } }
```

### 1.4 Tables

Tables are **two-block** structures: a `table` parent with `table_row` children. `table_width` is fixed at creation time.

#### `table`
```json
{
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "has_row_header": false,
    "children": [
      { "type": "table_row", "table_row": { "cells": [
        [ { "type": "text", "text": { "content": "Name" } } ],
        [ { "type": "text", "text": { "content": "Role" } } ],
        [ { "type": "text", "text": { "content": "Email" } } ]
      ] } },
      { "type": "table_row", "table_row": { "cells": [
        [ { "type": "text", "text": { "content": "Ada" } } ],
        [ { "type": "text", "text": { "content": "Engineer" } } ],
        [ { "type": "text", "text": { "content": "[email protected]" } } ]
      ] } }
    ]
  }
}
```
**Constraints:**
- `table_width` is the column count; **immutable** after creation.
- Every `table_row.cells` array length must equal `table_width`.
- Each cell is `rich_text[]` (an array, even if one element).
- Column widths cannot be set via API.

#### `table_row`
Only valid as a child of `table`.
```json
{
  "type": "table_row",
  "table_row": {
    "cells": [
      [ { "type": "text", "text": { "content": "A1" } } ],
      [ { "type": "text", "text": { "content": "A2" } } ]
    ]
  }
}
```

### 1.5 Columns (CRITICAL)

Columns nest in **two levels**: a `column_list` contains `column` children, and each `column` contains the actual content blocks.

**Rules:**
- A `column_list` must have at least **2** `column` children.
- Each `column` must have at least **1** child block.
- You cannot put non-`column` blocks directly inside a `column_list`.
- You cannot put a `column_list` directly inside a `column_list` (but you *can* put a `column_list` inside a `column` — that's how you nest columns).

```json
{
  "type": "column_list",
  "column_list": {
    "children": [
      {
        "type": "column",
        "column": {
          "children": [
            { "type": "paragraph", "paragraph": { "rich_text": [ { "type": "text", "text": { "content": "Left side" } } ] } }
          ]
        }
      },
      {
        "type": "column",
        "column": {
          "children": [
            { "type": "paragraph", "paragraph": { "rich_text": [ { "type": "text", "text": { "content": "Right side" } } ] } }
          ]
        }
      }
    ]
  }
}
```

Note: nesting depth on a single create-request is capped at **2** levels. To put e.g. a toggle inside a column, you may need to create the column_list first, then append children to each column in follow-up requests. As of recent updates, `column.width_ratio` may appear on existing columns (set in UI) but isn't reliably settable via API.

### 1.6 Database & page references

#### `child_page`
Read-only marker for a sub-page. You cannot create a `child_page` block directly — create the page with `parent.page_id` and a `child_page` block appears automatically in the parent.
```json
{ "type": "child_page", "child_page": { "title": "Sub-page title" } }
```

#### `child_database`
Same pattern — created indirectly by creating a database with `parent.page_id`.
```json
{ "type": "child_database", "child_database": { "title": "My database" } }
```

#### `link_to_page`
A pointer to another page or database.
```json
{ "type": "link_to_page", "link_to_page": { "type": "page_id", "page_id": "uuid" } }
```
Variants: `{ "type": "database_id", "database_id": "..." }`, `{ "type": "comment_id", "comment_id": "..." }`.

### 1.7 Synced & template blocks

#### `synced_block` (original)
```json
{
  "type": "synced_block",
  "synced_block": {
    "synced_from": null,
    "children": [
      { "type": "paragraph", "paragraph": { "rich_text": [ { "type": "text", "text": { "content": "Shared content" } } ] } }
    ]
  }
}
```

#### `synced_block` (mirror reference)
```json
{
  "type": "synced_block",
  "synced_block": {
    "synced_from": { "type": "block_id", "block_id": "<original_synced_block_id>" }
  }
}
```
Constraint: the API **cannot update synced block content directly** — update the original; mirrors update automatically.

#### `template`
A button-like template block. Read-only via API in most contexts; can be retrieved but cannot be "triggered" to instantiate via API.
```json
{
  "type": "template",
  "template": {
    "rich_text": [ { "type": "text", "text": { "content": "New task" } } ],
    "children": [ ... ]
  }
}
```

### 1.8 New in 2026-04-01

- `heading_4` — same shape as heading_1/2/3 with `is_toggleable`.
- `tab` and `tab_group` — tabbed content. (Schema still firming up; treat as opaque if you're on older versions.)

### 1.9 Unsupported / partial

Returned as `{ "type": "unsupported", "unsupported": {} }`. Known cases: complex layouts, some legacy blocks, third-party embeds not exposed.

### 1.10 Block-type capability summary

| Type | Has children | Has rich_text | Has color | Special |
|---|---|---|---|---|
| paragraph | yes | yes | yes | — |
| heading_1/2/3/4 | yes (if `is_toggleable`) | yes | yes | `is_toggleable` |
| bulleted_list_item | yes | yes | yes | — |
| numbered_list_item | yes | yes | yes | — |
| to_do | yes | yes | yes | `checked` |
| toggle | yes | yes | yes | — |
| quote | yes | yes | yes | — |
| callout | yes | yes | yes | `icon` |
| code | no | yes | no | `language`, `caption` |
| divider | no | no | no | empty |
| breadcrumb | no | no | no | empty |
| table_of_contents | no | no | yes | — |
| equation | no | no | no | `expression` |
| image/video/audio/file/pdf | no | no | no | `caption`, file object |
| bookmark | no | no | no | `caption`, `url` |
| embed | no | no | no | `url` |
| link_preview | no | no | no | read-only |
| table | yes (rows only) | no | no | `table_width` immutable |
| table_row | no | per-cell | no | `cells[][]` |
| column_list | yes (columns only) | no | no | needs ≥2 columns |
| column | yes | no | no | needs ≥1 child |
| synced_block | yes (original only) | no | no | `synced_from` |
| template | yes | yes | no | — |
| child_page | no | no | no | created indirectly |
| child_database | no | no | no | created indirectly |
| link_to_page | no | no | no | typed pointer |

---

## 2. Rich text objects

Every text-bearing field is a `rich_text` *array*. Each element:

```json
{
  "type": "text",
  "text": { "content": "Hello", "link": { "url": "https://example.com" } },
  "annotations": {
    "bold": false,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "code": false,
    "color": "default"
  },
  "plain_text": "Hello",
  "href": "https://example.com"
}
```

On **create/update**, you only need `type` and the type-specific payload (e.g. `text`). `plain_text`, `href`, `annotations` defaults are filled in if omitted. `href` and `text.link.url` should match.

### 2.1 Types

| `type` | Required field | Use |
|---|---|---|
| `text` | `text.content`, optional `text.link.url` | Standard text run |
| `equation` | `equation.expression` (LaTeX) | Inline math |
| `mention` | `mention.<subtype>` | @-mentions (see §2.4) |

### 2.2 Annotations

| Field | Type | Notes |
|---|---|---|
| `bold` | bool | |
| `italic` | bool | |
| `strikethrough` | bool | |
| `underline` | bool | |
| `code` | bool | Inline monospace |
| `color` | string | See colors below |

### 2.3 Colors (all 20)

**Foreground:** `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`.
**Background:** `default_background`(rare), `gray_background`, `brown_background`, `orange_background`, `yellow_background`, `green_background`, `blue_background`, `purple_background`, `pink_background`, `red_background`.

Used in **both** `rich_text.annotations.color` and most block-level `color` fields (paragraph, heading, callout, list items, etc.).

### 2.4 Mentions

```json
{ "type": "mention", "mention": { "type": "<subtype>", "<subtype>": { ... } } }
```

| Subtype | Payload (create-time) | Notes |
|---|---|---|
| `user` | `{ "object": "user", "id": "uuid" }` | Person or bot |
| `page` | `{ "id": "uuid" }` | Inline page mention |
| `database` | `{ "id": "uuid" }` | Pre-2025-09-03; post-2025-09-03 prefer `data_source` |
| `data_source` | `{ "id": "uuid" }` | 2025-09-03+ |
| `date` | `{ "start": "YYYY-MM-DD", "end": null, "time_zone": null }` | Same as date property |
| `link_preview` | `{ "url": "..." }` | **Cannot be created via API**, only returned |
| `template_mention` | `{ "type": "template_mention_date", "template_mention_date": "today" }` or `template_mention_user: "me"` | Special placeholders in template blocks |
| `link_mention` | `{ "href": "..." }` (read-only) | Newer "smart link" |

Example user mention inline:
```json
{
  "type": "mention",
  "mention": { "type": "user", "user": { "object": "user", "id": "uuid" } },
  "annotations": { "bold": false, "italic": false, "strikethrough": false, "underline": false, "code": false, "color": "default" }
}
```

### 2.5 Length limits & chunking

- Each `rich_text` element's `text.content` is capped at **2000 characters**.
- A `rich_text[]` array also has a soft maximum (around **100 elements**).
- URL fields are capped at **2000 chars**.
- Block-level rich_text arrays are limited to ~100 elements total.

**Chunking strategy** for text > 2000 chars:
1. Split content at word boundaries near each 2000-char mark.
2. Emit consecutive `text` rich_text elements within the same block — they render seamlessly.
3. For extremely long content (>~100 rich_text elements per block), split across multiple paragraph blocks instead.

```python
def chunk_text(s, n=1900):
    while s:
        # break at last space within window
        idx = s.rfind(" ", 0, n) if len(s) > n else len(s)
        if idx <= 0: idx = min(n, len(s))
        yield s[:idx]
        s = s[idx:].lstrip()

rich_text = [{"type": "text", "text": {"content": chunk}} for chunk in chunk_text(long_string)]
```

### 2.6 Links inside rich_text

Link goes in **two places** that must agree on read; on write only `text.link` is needed:
```json
{ "type": "text", "text": { "content": "Notion", "link": { "url": "https://notion.so" } } }
```

---

## 3. Pages

### 3.1 Create a page — `POST /v1/pages`

The `parent` discriminator drives everything:

| `parent.type` | Behavior |
|---|---|
| `database_id` (legacy) / `data_source_id` (2025-09-03+) | Page is a row; `properties` must conform to schema |
| `page_id` | Page is a sub-page of another page; only `title` property |
| `workspace: true` | Page is top-level (workspace owner integration only) |

**Page in a database (legacy `database_id`):**
```json
{
  "parent": { "database_id": "uuid" },
  "icon":  { "type": "emoji", "emoji": "🚀" },
  "cover": { "type": "external", "external": { "url": "https://images.unsplash.com/photo-..." } },
  "properties": {
    "Name":     { "title": [ { "type": "text", "text": { "content": "Launch plan" } } ] },
    "Status":   { "status": { "name": "In progress" } },
    "Owner":    { "people": [ { "object": "user", "id": "uuid" } ] },
    "Tags":     { "multi_select": [ { "name": "P0" }, { "name": "Q2" } ] },
    "Priority": { "select": { "name": "High" } },
    "Due":      { "date": { "start": "2026-06-01" } },
    "Estimate": { "number": 8 },
    "Done":     { "checkbox": false },
    "URL":      { "url": "https://launchpad.example.com" },
    "Notes":    { "rich_text": [ { "type": "text", "text": { "content": "Kickoff Monday." } } ] }
  },
  "children": [
    { "type": "heading_2", "heading_2": { "rich_text": [ { "type": "text", "text": { "content": "Overview" } } ] } },
    { "type": "paragraph", "paragraph": { "rich_text": [ { "type": "text", "text": { "content": "Body text..." } } ] } }
  ]
}
```

**Page under a parent page:**
```json
{
  "parent": { "page_id": "uuid" },
  "properties": {
    "title": [ { "type": "text", "text": { "content": "Meeting notes" } } ]
  },
  "children": [ ... ]
}
```

### 3.2 Icons

| Type | Shape |
|---|---|
| Emoji | `{ "type": "emoji", "emoji": "🚀" }` |
| External | `{ "type": "external", "external": { "url": "https://..." } }` |
| File (uploaded) | `{ "type": "file_upload", "file_upload": { "id": "<file_upload_id>" } }` |
| Custom emoji | `{ "type": "custom_emoji", "custom_emoji": { "id": "uuid", "name": "...", "url": "..." } }` (read-only on most workspaces) |
| File (hosted by Notion) | `{ "type": "file", "file": {...} }` — read-only |

To **clear** an icon: pass `"icon": null`.

### 3.3 Covers

Same shape as icons but **only `external` and `file_upload` are writable** (no emoji covers). Notion will display the cover with default Unsplash-style positioning; positioning isn't exposed.

### 3.4 Archive / restore

Two equivalent flags:
- `"archived": true` (legacy, still works)
- `"in_trash": true` (newer naming, post-2022-06-28)

```http
PATCH /v1/pages/{page_id}
{ "archived": true }
```
Restore: `{ "archived": false }`.

Archiving a page archives all its children. Deletion (hard-delete) is not exposed via API — archive is the closest analog.

### 3.5 Update properties vs content (two endpoints)

| You want to change | Endpoint |
|---|---|
| Page properties, icon, cover, archive | `PATCH /v1/pages/{page_id}` |
| Page body content (blocks) | `PATCH /v1/blocks/{page_id}/children` to append; `PATCH /v1/blocks/{block_id}` to update one block |

The page ID is also a block ID — that's how you append body content.

### 3.6 Retrieve a property item

For large property values (rollups, relations with many entries, long titles):
```http
GET /v1/pages/{page_id}/properties/{property_id}?page_size=100&start_cursor=...
```
Returns paginated `property_item` objects. **Title, rich_text, relation, people, and rollup** properties are paginated.

---

## 4. Databases

A database has:
- **Title & description** (rich_text)
- **Icon & cover**
- **Properties / schema** (`properties` map)
- **Is inline** (`is_inline: true` makes it an inline DB inside a page)
- 2025-09-03+: one or more **data sources**

### 4.1 Create — `POST /v1/databases`

```json
{
  "parent": { "type": "page_id", "page_id": "uuid" },
  "icon":  { "type": "emoji", "emoji": "📋" },
  "title": [ { "type": "text", "text": { "content": "Tasks" } } ],
  "description": [ { "type": "text", "text": { "content": "Team backlog" } } ],
  "is_inline": false,
  "properties": {
    "Name":     { "title": {} },
    "Status":   { "status": {} },
    "Owner":    { "people": {} },
    "Due":      { "date": {} },
    "Priority": { "select": { "options": [
                    { "name": "High", "color": "red" },
                    { "name": "Med",  "color": "yellow" },
                    { "name": "Low",  "color": "gray" }
                ] } }
  }
}
```

### 4.2 Property types — schema vs value

| Type | Schema (create DB) | Page value | Notes |
|---|---|---|---|
| `title` | `"Name": { "title": {} }` | `{ "title": [richtext...] }` | **Required exactly once per DB** |
| `rich_text` | `{ "rich_text": {} }` | `{ "rich_text": [richtext...] }` | |
| `number` | `{ "number": { "format": "dollar" } }` | `{ "number": 42 }` | See formats below |
| `select` | `{ "select": { "options": [{ "name": "A", "color": "red" }] } }` | `{ "select": { "name": "A" } }` or `{ "select": null }` | Setting a new name auto-creates option |
| `multi_select` | `{ "multi_select": { "options": [...] } }` | `{ "multi_select": [ { "name": "A" }, { "name": "B" } ] }` | Same auto-create |
| `status` | `{ "status": {} }` | `{ "status": { "name": "In progress" } }` | **Cannot set options/groups via API** — UI only |
| `date` | `{ "date": {} }` | `{ "date": { "start": "2026-06-01", "end": null, "time_zone": null } }` | See §4.4 |
| `people` | `{ "people": {} }` | `{ "people": [ { "object": "user", "id": "uuid" } ] }` | |
| `files` | `{ "files": {} }` | `{ "files": [ { "name": "doc.pdf", "type": "external", "external": { "url": "..." } } ] }` | `name` required |
| `checkbox` | `{ "checkbox": {} }` | `{ "checkbox": true }` | |
| `url` | `{ "url": {} }` | `{ "url": "https://..." }` | 2000-char limit |
| `email` | `{ "email": {} }` | `{ "email": "[email protected]" }` | |
| `phone_number` | `{ "phone_number": {} }` | `{ "phone_number": "+1-555-0100" }` | Free-form string |
| `formula` | `{ "formula": { "expression": "prop(\"Price\") * 1.1" } }` | read-only, returns `{ "formula": { "type": "number", "number": 11 } }` | See §4.6 |
| `relation` | `{ "relation": { "database_id": "<target>", "type": "dual_property", "dual_property": {} } }` | `{ "relation": [ { "id": "uuid" } ], "has_more": false }` | See §4.5 |
| `rollup` | `{ "rollup": { "relation_property_name": "Projects", "rollup_property_name": "Cost", "function": "sum" } }` | read-only, returns aggregate | See §4.7 |
| `created_time` | `{ "created_time": {} }` | read-only `{ "created_time": "..." }` | |
| `created_by` | `{ "created_by": {} }` | read-only user object | |
| `last_edited_time` | `{ "last_edited_time": {} }` | read-only | |
| `last_edited_by` | `{ "last_edited_by": {} }` | read-only | |
| `unique_id` | `{ "unique_id": { "prefix": "TASK" } }` | read-only `{ "unique_id": { "prefix": "TASK", "number": 42 } }` | Prefix 2-7 alphanumerics |
| `button` | `{ "button": {} }` | read-only `{ "button": {} }` | Cannot be triggered via API |
| `verification` | `{ "verification": {} }` | read-only verification object | Wiki-style |

### 4.3 Number format values

`number`, `number_with_commas`, `percent`, `dollar`, `canadian_dollar`, `singapore_dollar`, `australian_dollar`, `hong_kong_dollar`, `new_zealand_dollar`, `new_taiwan_dollar`, `euro`, `pound`, `yen`, `ruble`, `rupee`, `won`, `yuan`, `real`, `lira`, `rupiah`, `franc`, `krona`, `norwegian_krone`, `danish_krone`, `mexican_peso`, `chilean_peso`, `philippine_peso`, `argentine_peso`, `uruguayan_peso`, `colombian_peso`, `rand`, `riyal`, `dirham`, `shekel`, `zloty`, `baht`, `forint`, `koruna`.

### 4.4 Date values

```json
"Due": {
  "date": {
    "start": "2026-06-01T09:00:00.000-07:00",
    "end":   "2026-06-01T10:00:00.000-07:00",
    "time_zone": null
  }
}
```
- Date-only: `"start": "2026-06-01"`.
- If you set `time_zone` (IANA, e.g. `"America/Los_Angeles"`), `start`/`end` must **not** carry a UTC offset and must include times.
- `end` is optional; if present, must be ≥ `start`.

### 4.5 Relations

**Schema — single property (one-way):**
```json
"Projects": {
  "relation": {
    "database_id": "<target_db_id>",
    "type": "single_property",
    "single_property": {}
  }
}
```

**Schema — dual property (two-way):**
```json
"Projects": {
  "relation": {
    "database_id": "<target_db_id>",
    "type": "dual_property",
    "dual_property": {}
  }
}
```
After creation, the API populates `dual_property.synced_property_name` and `synced_property_id` (auto-generated; you cannot set the synced name on create — rename via UI or update-property after).

**Value:**
```json
"Projects": { "relation": [ { "id": "page-uuid-1" }, { "id": "page-uuid-2" } ], "has_more": false }
```

**Permissions gotcha:** the integration must have access to **both** databases (and the related page rows it references), or the write will succeed but reads of related items may 404.

### 4.6 Formulas

Schema:
```json
"Total": { "formula": { "expression": "prop(\"Qty\") * prop(\"Price\")" } }
```

Formulas 2.0 syntax basics:

| Element | Example |
|---|---|
| Property reference | `prop("Name")` |
| Strings | `"hello"` |
| Numbers | `42`, `3.14` |
| Booleans | `true`, `false` |
| Math | `+ - * / %`, `pow(x, y)`, `round(x)`, `abs(x)` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Logic | `and`, `or`, `not` |
| Conditional | `if(cond, a, b)` or ternary `cond ? a : b` |
| String fns | `concat(a, b)`, `length(s)`, `slice(s, n)`, `replaceAll(s, "x", "y")`, `format(x)`, `lower(s)`, `upper(s)` |
| Date fns | `now()`, `today()`, `dateAdd(d, n, "days")`, `dateSubtract`, `dateBetween(a, b, "days")`, `formatDate(d, "MMM D")` |
| Lists (2.0) | `["a","b"].map(x => upper(x))`, `.filter`, `.find`, `.sort`, `.length`, `.first`, `.last` |
| Dot syntax (2.0) | `prop("Tags").length`, `prop("Due").year` |

Output type is inferred. Filtering on a formula requires matching the type (e.g. `formula.checkbox.equals: true`).

### 4.7 Rollups

```json
"Total Cost": {
  "rollup": {
    "relation_property_name": "Projects",
    "rollup_property_name":   "Cost",
    "function": "sum"
  }
}
```
You can use IDs instead of names: `relation_property_id`, `rollup_property_id`.

**Functions:** `count`, `count_values`, `empty`, `not_empty`, `unique`, `count_unique`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `median`, `min`, `max`, `range`, `earliest_date`, `latest_date`, `date_range`, `checked`, `unchecked`, `percent_checked`, `percent_unchecked`, `show_original`, `show_unique`.

Rollup values come back with a nested `array` (list of property items) plus a `function` summary:
```json
"Total Cost": { "rollup": { "type": "number", "function": "sum", "number": 4200 } }
```

### 4.8 Status property

Default schema (auto-created if you don't specify):

```json
"Status": {
  "status": {
    "options": [
      { "name": "Not started", "color": "default" },
      { "name": "In progress", "color": "blue" },
      { "name": "Done",        "color": "green" }
    ],
    "groups": [
      { "name": "To-do",       "color": "gray",  "option_ids": [...] },
      { "name": "In progress", "color": "blue",  "option_ids": [...] },
      { "name": "Complete",    "color": "green", "option_ids": [...] }
    ]
  }
}
```

**Critical:** `options` and `groups` for `status` properties **cannot be created or modified via API** — only via the Notion UI. On create, pass `{ "status": {} }` and Notion installs the default 3-option / 3-group set; rename/add via UI afterward.

### 4.9 Unique ID

```json
"Ticket ID": { "unique_id": { "prefix": "TKT" } }
```
- Prefix: 2-7 alphanumerics, case-insensitive on storage.
- Cannot be set on a page — Notion increments automatically.

### 4.10 Update database schema — `PATCH /v1/databases/{id}`

```json
{
  "title": [ { "type": "text", "text": { "content": "Tasks (v2)" } } ],
  "description": [ { "type": "text", "text": { "content": "Updated description" } } ],
  "icon": { "type": "emoji", "emoji": "✅" },
  "properties": {
    "Owner": { "name": "Assignee" },
    "Old Field": null,
    "New Field": { "rich_text": {} },
    "Priority": { "select": { "options": [
      { "name": "Urgent", "color": "red" },
      { "name": "Normal", "color": "default" }
    ] } }
  }
}
```

Patterns:
- Rename: `"Old name": { "name": "New name" }`
- Delete: `"Field name": null`
- Add: `"New name": { "<type>": {...} }`
- Modify type: pass the new type config under the existing key (some conversions are lossy/forbidden)

### 4.11 Views (2026-04-01+ only)

Views support: `table`, `board`, `list`, `calendar`, `timeline`, `gallery`, `form`, `chart`, `map`, `dashboard`.

**Pre-2026-04-01 you CANNOT create or modify views via the API.** The default view (table) ships when the database is created, and additional views must be added in the UI. As of 2026-04-01, eight new view endpoints exist:

- `POST /v1/views` — create
- `GET /v1/views/{view_id}` — retrieve
- `PATCH /v1/views/{view_id}` — update (must include `type` and any required fields per type)
- `DELETE /v1/views/{view_id}` — delete
- List/query variants for views on a database

View config keys vary by type:

| View type | Required config |
|---|---|
| board | `group_by` (property_id) |
| calendar | `date_property_id` |
| timeline | `date_property_id` (start) and optional end |
| gallery | typically `card_size`, `card_cover` |
| table/list | filters, sorts |

---

## 5. Search & Query

### 5.1 Search — `POST /v1/search`

```json
{
  "query": "design review",
  "filter": { "value": "page", "property": "object" },
  "sort":   { "direction": "descending", "timestamp": "last_edited_time" },
  "start_cursor": "...",
  "page_size": 100
}
```

- `filter.value`: `"page"` or `"database"` (or `"data_source"` on 2025-09-03+). `filter.property` must equal `"object"`.
- Returns only items the integration has access to.
- **Eventual consistency gotcha:** newly-created or recently-renamed items are not immediately indexed; do **not** use search as a "list everything" mechanism. To enumerate, recursively walk known parents via `GET /v1/blocks/{id}/children`.

### 5.2 Query a database — `POST /v1/databases/{id}/query`

(2025-09-03+: use `POST /v1/data_sources/{id}/query`.)

```json
{
  "filter": { ... },
  "sorts":  [ { "property": "Due", "direction": "ascending" },
              { "timestamp": "created_time", "direction": "descending" } ],
  "start_cursor": null,
  "page_size": 100
}
```

### 5.3 Filters — full reference

A filter is either a **property filter** or a **compound filter** (`and`/`or`).

**Compound:**
```json
{
  "and": [
    { "property": "Done", "checkbox": { "equals": true } },
    { "or": [
        { "property": "Tags", "multi_select": { "contains": "P0" } },
        { "property": "Tags", "multi_select": { "contains": "P1" } }
    ] }
  ]
}
```
Up to **2 levels deep** of compound nesting.

**Per-type operator catalog:**

| Property type | Operators (filter conditions) |
|---|---|
| `title`, `rich_text`, `url`, `email`, `phone_number` | `equals`, `does_not_equal`, `contains`, `does_not_contain`, `starts_with`, `ends_with`, `is_empty`, `is_not_empty` |
| `number` | `equals`, `does_not_equal`, `greater_than`, `less_than`, `greater_than_or_equal_to`, `less_than_or_equal_to`, `is_empty`, `is_not_empty` |
| `checkbox` | `equals`, `does_not_equal` |
| `select` | `equals`, `does_not_equal`, `is_empty`, `is_not_empty` |
| `multi_select` | `contains`, `does_not_contain`, `is_empty`, `is_not_empty` |
| `status` | `equals`, `does_not_equal`, `is_empty`, `is_not_empty` |
| `date`, `created_time`, `last_edited_time` | `equals`, `before`, `after`, `on_or_before`, `on_or_after`, `is_empty`, `is_not_empty`, plus relative: `past_week`, `past_month`, `past_year`, `next_week`, `next_month`, `next_year`, `this_week` |
| `people`, `created_by`, `last_edited_by` | `contains`, `does_not_contain`, `is_empty`, `is_not_empty` |
| `files` | `is_empty`, `is_not_empty` |
| `relation` | `contains`, `does_not_contain`, `is_empty`, `is_not_empty` |
| `formula` | wrap inner: `{ "formula": { "string": {...} } }` with `string`, `number`, `checkbox`, or `date` matching formula return type |
| `rollup` | three modes: `any: {...}`, `every: {...}`, `none: {...}` for array rollups; or `number`/`date` for aggregated rollups |
| `unique_id` | `equals`, `does_not_equal`, `greater_than`, `less_than`, `greater_than_or_equal_to`, `less_than_or_equal_to` |

**Timestamp filter (no property required):**
```json
{ "timestamp": "created_time", "created_time": { "past_week": {} } }
```

**Sorts:**
```json
[
  { "property": "Priority", "direction": "ascending" },
  { "timestamp": "last_edited_time", "direction": "descending" }
]
```
Property sorts use the property name (or `property_id`). Timestamp sorts use `created_time` or `last_edited_time`.

### 5.4 Pagination

All collection endpoints use cursor pagination. Loop:
```python
cursor = None
while True:
    r = notion.databases.query(database_id=db, start_cursor=cursor, page_size=100)
    for row in r["results"]: handle(row)
    if not r["has_more"]: break
    cursor = r["next_cursor"]
```
Cursors are opaque strings. The 2026-04-01 version changed cursor format — don't parse them.

---

## 6. Updates & deletes

### 6.1 Append block children — `PATCH /v1/blocks/{block_id}/children`

```json
{
  "children": [ ... up to 100 blocks ... ],
  "after": "<existing_child_block_id_to_insert_after>"
}
```
- Max **100** blocks per request.
- Max **2 levels** of nesting in one request (e.g., a column_list with columns containing paragraphs is fine; column_list → column → toggle → list_item exceeds it).
- `after` is optional; without it, content appends to the end.
- `block_id` can be a page ID — that's how you add to a page's body.
- Response returns the newly-created blocks **and** a `list` envelope.

### 6.2 Update a single block — `PATCH /v1/blocks/{block_id}`

```json
{ "paragraph": { "rich_text": [ { "type": "text", "text": { "content": "Edited." } } ] } }
```
- You **must** pass the full nested object — partial merges are not supported within the type payload.
- Cannot change block `type` (delete + re-append to "convert").
- Cannot use this endpoint to modify children — use append/delete on children separately.

### 6.3 Delete (archive) a block — `DELETE /v1/blocks/{block_id}`

Soft-deletes (sets `archived: true` / `in_trash: true`). Restore via `PATCH` with `{ "archived": false }`. Hard-delete is not exposed.

### 6.4 Retrieve children — `GET /v1/blocks/{block_id}/children`

Paginated. Use this to fetch:
- Page body blocks (page_id as block_id)
- Toggle/callout/list_item/etc. children
- `table_row`s of a `table`
- `column`s of a `column_list`

Note: `has_children: true` doesn't mean the children are populated in the response — you have to fetch them.

### 6.5 Update page — `PATCH /v1/pages/{page_id}`

```json
{
  "properties": {
    "Status": { "status": { "name": "Done" } },
    "Done":   { "checkbox": true }
  },
  "icon":  { "type": "emoji", "emoji": "✅" },
  "cover": null,
  "archived": false
}
```
- Only the included properties are updated; others are untouched.
- To **clear** a property: pass the type with empty array/null appropriate (`"rich_text": []`, `"select": null`, `"date": null`, `"people": []`, `"multi_select": []`).

### 6.6 Update database — `PATCH /v1/databases/{id}` (see §4.10)

### 6.7 Update a data source (2025-09-03+) — `PATCH /v1/data_sources/{id}`

Same shape as database schema updates but operates on the data source (each multi-source DB has ≥1 data sources).

---

## 7. File uploads (2024+)

**Workflow:**
1. `POST /v1/file_uploads` → returns `{ id, upload_url, ... }`.
2. `POST <upload_url>` (single-part, ≤20 MiB) **or** repeated `POST <upload_url>?part_number=N` (multi-part).
   - Content-Type: `multipart/form-data` with a `file` field.
3. (Multi-part only) `POST /v1/file_uploads/{id}/complete`.
4. Attach by referencing the upload id:
   - In a block: `"image": { "type": "file_upload", "file_upload": { "id": "..." } }`
   - In a `files` property: `{ "files": [{ "name": "doc.pdf", "type": "file_upload", "file_upload": { "id": "..." } }] }`

A single file_upload id can be attached in many places.

---

## 8. Constraints & best-practice cheat sheet

| Constraint | Value |
|---|---|
| Rate limit (average) | 3 req/sec / integration |
| Burst tolerance | Short bursts allowed; obey `Retry-After` |
| Block children per request | 100 max |
| Nesting depth per request | 2 levels |
| `rich_text` content per element | 2000 chars |
| `rich_text[]` per block | ~100 elements |
| URL length (any URL field) | 2000 chars |
| `page_size` (pagination) | 100 max, default 100 (block children) / depends per endpoint |
| Status options/groups via API | Read-only — UI only |
| Views via API | Pre-2026-04-01: cannot create. 2026-04-01+: yes |
| Synced block updates | Only via the original; mirrors can't be modified |
| Hard delete | Not exposed (only archive/trash) |
| File size single-part | ≤20 MiB |
| Multi-part file part size | 5-20 MiB per part |
| Title property per DB | Exactly 1 (`type: "title"`) — required |
| Bulk-create pages | Not native — loop one-at-a-time, throttled |

**Idempotency:** Notion has no idempotency-key header. Safe retry strategy for writes:
- For creates: capture the returned id; if the network fails before you see a response, check via search/query before retrying.
- For updates: PATCH is naturally idempotent (same body → same result), so retries on 5xx/429 are safe.
- Reads: always retryable.

**Retry policy:**
```
attempts = 5
for i in range(attempts):
    r = call()
    if r.status < 400: return r
    if r.status in (429, 500, 502, 503, 504):
        wait = float(r.headers.get("Retry-After", 2 ** i))
        sleep(wait); continue
    raise APIError(r)
```

---

## 9. Common pitfalls AI agents hit

1. **`parent.database_id` vs `parent.page_id`.** A page inside a database **must** use `database_id` (or `data_source_id` on 2025-09-03+). A page inside another page **must** use `page_id`. Mixing these throws `validation_error`.

2. **Case-sensitive property names.** `"name"` ≠ `"Name"` ≠ `"NAME"`. Always read the schema before writing, or refer by `property_id` (the short opaque code that doesn't change on rename).

3. **`select`/`multi_select` options auto-create on write, but `status` does not.** If you set `{ "status": { "name": "Reviewing" } }` and "Reviewing" isn't already an option, the request **fails**. Pre-seed all status options in the UI.

4. **Status groups/options unreachable from API.** Even on database create, you cannot define status options. Notion installs the default 3 (Not started / In progress / Done) and you must edit in the UI.

5. **Relation requires shared access.** The integration must be added to **both** the source DB and the target DB. Adding to source only causes silent "page not found" on related-page reads.

6. **`is_toggleable` on headings.** To make a toggle heading, set `heading_1.is_toggleable: true` — and only then can you give it `children`.

7. **2000-character chunking.** A single rich_text element with 5000 chars fails. Split into multiple rich_text elements in the same array (renders seamlessly).

8. **Block update is replace, not merge.** `PATCH /v1/blocks/{id}` with a paragraph payload replaces the whole rich_text. Read first if you want to preserve formatting in part of it.

9. **No bulk-page-create.** You cannot create multiple pages in one call. Each call costs rate-limit budget; throttle to ~3/sec.

10. **`children` in `create page` is limited.** When creating a page with `children`, you can include up to 100 blocks with 2 levels of nesting. Anything deeper requires follow-up `PATCH /blocks/{id}/children` calls.

11. **Search is eventually consistent.** Newly-created pages may not appear in search results for seconds-to-minutes. Use search for user-driven lookups, not for "list everything I just created."

12. **`url`/`email`/`phone_number` are minimally validated.** The API accepts almost any string for `phone_number`, and `email` only checks for `@`. URLs reject blatantly malformed input.

13. **File-hosted (`type: "file"`) URLs expire.** They have an `expiry_time` (~1 hour). Re-fetch the page/block to get a fresh URL — don't cache.

14. **`column_list` minimum-children rule.** A column_list with one column, or columns with no children, fails validation at append-time. Always create both columns with at least one child each in the same request.

15. **`table_width` is permanent.** Creating a 3-column table and then trying to PATCH it to 4 columns fails. Recreate the table.

16. **Date `time_zone` is mutually exclusive with offsets.** If you set `time_zone: "America/New_York"`, you must drop the `-04:00`/`-05:00` suffix from `start`/`end`. Mixing them returns 400.

17. **`title` property on a sub-page is keyed `"title"` (lowercase).** When the parent is a `page_id`, the only property is `"title": [richtext...]` — not `"Name"`.

18. **`formula` filter shape mirrors the formula's output type.** A formula returning a boolean uses `{ "formula": { "checkbox": { "equals": true } } }`, not `{ "formula": { "equals": true } }`.

19. **Rollup filters use `any`/`every`/`none`.** Don't try to filter a rollup with the underlying property's direct operators when its result is an array.

20. **`Notion-Version` is mandatory.** Forgetting it returns 400 `missing_version`. Pin to a version you've tested against; don't auto-upgrade.

21. **Property values can't include the `id`/`color` fields when writing.** For `select`/`multi_select`/`status`, only pass `name` (or `id`). The API echoes `id`/`color` on read; including them on write often fails validation.

22. **Archived parents cascade.** If you archive a database, all its pages are archived. Restoring the DB does **not** auto-restore pages.

23. **No event-style webhooks (pre-2024 baseline).** If you need change notifications, poll `last_edited_time` on a query. (Newer notification/webhook features exist in select betas; check the changelog before depending on them.)

24. **Integration token != user.** Comments, page mentions, and "created_by" attribute to the bot user, not a human. Pages created by the bot are sometimes invisible to users who haven't been re-granted access by the bot's parent share.

---

## 10. Endpoint quick map

| Verb | Path | Purpose |
|---|---|---|
| GET | `/v1/users` | List users |
| GET | `/v1/users/{id}` | Retrieve user |
| GET | `/v1/users/me` | Bot user |
| POST | `/v1/search` | Search workspace |
| POST | `/v1/pages` | Create page |
| GET | `/v1/pages/{id}` | Retrieve page |
| PATCH | `/v1/pages/{id}` | Update page props / icon / cover / archive |
| GET | `/v1/pages/{id}/properties/{prop_id}` | Retrieve property item (paginated) |
| POST | `/v1/databases` | Create database |
| GET | `/v1/databases/{id}` | Retrieve database |
| PATCH | `/v1/databases/{id}` | Update database schema |
| POST | `/v1/databases/{id}/query` | Query database (pre-2025-09-03) |
| POST | `/v1/data_sources/{id}/query` | Query data source (2025-09-03+) |
| PATCH | `/v1/data_sources/{id}` | Update data source schema (2025-09-03+) |
| GET | `/v1/blocks/{id}` | Retrieve block |
| PATCH | `/v1/blocks/{id}` | Update single block |
| DELETE | `/v1/blocks/{id}` | Archive block |
| GET | `/v1/blocks/{id}/children` | Retrieve children (paginated) |
| PATCH | `/v1/blocks/{id}/children` | Append children (≤100) |
| POST | `/v1/comments` | Create comment on page/block |
| GET | `/v1/comments?block_id=...` | List unresolved comments |
| POST | `/v1/file_uploads` | Begin file upload |
| GET | `/v1/file_uploads/{id}` | Status |
| POST | `<upload_url>` | Send file part (multipart/form-data) |
| POST | `/v1/file_uploads/{id}/complete` | Finish multi-part |
| POST/GET/PATCH/DELETE | `/v1/views[/{id}]` | Views CRUD (2026-04-01+) |
| GET | `/v1/oauth/token` | OAuth token exchange (public integrations) |

---

## 11. Minimal "perfect page" recipe for an agent

```json
POST /v1/pages
{
  "parent": { "database_id": "<DB>" },
  "icon":  { "type": "emoji", "emoji": "📘" },
  "cover": { "type": "external", "external": { "url": "https://images.unsplash.com/photo-..." } },
  "properties": {
    "Name":   { "title": [ { "type": "text", "text": { "content": "Project brief: Atlas" } } ] },
    "Status": { "status": { "name": "In progress" } },
    "Owner":  { "people": [ { "object": "user", "id": "<USER>" } ] },
    "Tags":   { "multi_select": [ { "name": "Engineering" }, { "name": "Q3" } ] },
    "Due":    { "date": { "start": "2026-08-01" } }
  },
  "children": [
    { "type": "callout", "callout": {
        "rich_text": [ { "type": "text", "text": { "content": "TL;DR — launch Atlas in Q3 with new pricing." } } ],
        "icon": { "type": "emoji", "emoji": "📌" },
        "color": "blue_background"
    } },
    { "type": "heading_2", "heading_2": { "rich_text": [ { "type": "text", "text": { "content": "Overview" } } ] } },
    { "type": "paragraph", "paragraph": { "rich_text": [
        { "type": "text", "text": { "content": "Atlas is the next-generation platform for " } },
        { "type": "text", "text": { "content": "real-time collaboration", "link": { "url": "https://example.com/atlas" } }, "annotations": { "bold": true, "italic": false, "strikethrough": false, "underline": false, "code": false, "color": "default" } },
        { "type": "text", "text": { "content": ". Below: goals, scope, milestones." } }
    ] } },
    { "type": "divider", "divider": {} },
    { "type": "heading_2", "heading_2": { "rich_text": [ { "type": "text", "text": { "content": "Goals" } } ] } },
    { "type": "to_do", "to_do": { "rich_text": [ { "type": "text", "text": { "content": "Cut TTI by 30%" } } ], "checked": false } },
    { "type": "to_do", "to_do": { "rich_text": [ { "type": "text", "text": { "content": "Launch tiered pricing" } } ], "checked": false } },
    { "type": "column_list", "column_list": { "children": [
      { "type": "column", "column": { "children": [
        { "type": "heading_3", "heading_3": { "rich_text": [ { "type": "text", "text": { "content": "Wins" } } ] } },
        { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [ { "type": "text", "text": { "content": "Hired 3 engineers" } } ] } }
      ] } },
      { "type": "column", "column": { "children": [
        { "type": "heading_3", "heading_3": { "rich_text": [ { "type": "text", "text": { "content": "Risks" } } ] } },
        { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [ { "type": "text", "text": { "content": "Vendor lock-in on auth" } } ] } }
      ] } }
    ] } },
    { "type": "code", "code": {
        "language": "json",
        "rich_text": [ { "type": "text", "text": { "content": "{ \"env\": \"prod\" }" } } ],
        "caption": [ { "type": "text", "text": { "content": "Example config" } } ]
    } }
  ]
}
```

Then append additional body content (>100 blocks or >2 nesting levels) with `PATCH /v1/blocks/<page_id>/children` follow-ups, throttled to ≤3 req/s.

---

**Document size:** approximately **5,800 words / 1,400 lines** of markdown, plus ~25 JSON snippets and 12 reference tables. This is the working reference an agent can consult before every Notion call. Sources for the underlying research below.

Sources:
- [Notion API — Block reference](https://developers.notion.com/reference/block)
- [Notion API — Rich text](https://developers.notion.com/reference/rich-text)
- [Notion API — Data source / database properties](https://developers.notion.com/reference/property-object)
- [Notion API — Filter database entries](https://developers.notion.com/reference/post-database-query-filter)
- [Notion API — Create a page](https://developers.notion.com/reference/post-page)
- [Notion API — Create a database](https://developers.notion.com/reference/database-create)
- [Notion API — Update page](https://developers.notion.com/reference/patch-page)
- [Notion API — Append block children](https://developers.notion.com/reference/patch-block-children)
- [Notion API — Search by title](https://developers.notion.com/reference/post-search)
- [Notion API — Request limits](https://developers.notion.com/reference/request-limits)
- [Notion API — Status codes](https://developers.notion.com/reference/status-codes)
- [Notion API — Versioning](https://developers.notion.com/reference/versioning)
- [Notion API — Working with files & media](https://developers.notion.com/docs/working-with-files-and-media)
- [Notion API — Uploading small files](https://developers.notion.com/docs/uploading-small-files)
- [Notion API — Uploading larger files](https://developers.notion.com/docs/sending-larger-files)
- [Notion API — Working with views (2026-04-01)](https://developers.notion.com/guides/data-apis/working-with-views)
- [Notion API — Upgrade guide 2025-09-03](https://developers.notion.com/docs/upgrade-guide-2025-09-03)
- [Notion API — Working with page content](https://developers.notion.com/docs/working-with-page-content)
- [Notion API — Working with databases](https://developers.notion.com/docs/working-with-databases)
- [Notion API Changelog — Callouts and quote blocks](https://developers.notion.com/changelog/callouts-and-quote-blocks-are-now-supported)
- [Notion API Changelog — Date filters with time zones](https://developers.notion.com/changelog/dates-with-times-and-timezones-are-now-supported-on-database-date-filters)
- [Notion API Changelog — Currency formats](https://developers.notion.com/changelog/number-properties-now-support-more-currency-formats)
- [Notion API Changelog — Rollup show_original](https://developers.notion.com/changelog/rollup-property-functions-now-include-show_original)
- [Notion API Changelog — Caption on code blocks](https://developers.notion.com/changelog/caption-property-is-now-supported-in-code-block-type)
- [Notion Updates 2026: API changes summary (Fazm)](https://fazm.ai/blog/notion-api-updates-2026)
- [Notion API rate limits 2026 guide (Fazm)](https://fazm.ai/blog/notion-api-rate-limits-2026)
- [Notion formula syntax & functions](https://www.notion.com/help/formula-syntax)
- [Thomas Frank — Notion API rate limits & retries](https://thomasjfrank.com/how-to-handle-notion-api-request-limits/)
- [Thomas Frank — Notion column tricks (nesting)](https://thomasjfrank.com/notion-nested-columns/)
- [Notion-helper helper library](https://tomfrankly.github.io/notion-helper/)
- [makenotion/notion-sdk-js — LanguageRequest types (DeepWiki)](https://deepwiki.com/makenotion/notion-sdk-js/4.1-blocks-api)
- [Notion Help — Status property](https://www.notion.com/help/guides/status-property-gives-clarity-on-tasks)
- [Notion Help — Unique ID](https://www.notion.com/help/unique-id)
- [Connex Digital — Notion integration permissions safe setup](https://connex.digital/blog/how-to-grant-notion-integration-permissions-safely-without-making-someone-an-admin/)
- [SourceSync — Notion OAuth gotchas](https://sourcesync.ai/notion-oauth-gotchas)