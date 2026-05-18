# Markdown to Notion Blocks

Most agents receive prose as markdown and need to send it to Notion as block JSON. There are three reasonable ways to do this. Choose based on which Notion-Version you're on and how much control you need over the output.

## Option 1: Use the native `markdown` field (recommended)

As of `Notion-Version: 2025-09-03`, `POST /v1/pages` accepts a `markdown` field directly. Notion's server converts it to block JSON on your behalf, handling most of CommonMark plus a few Notion extensions.

```json
{
  "parent": { "page_id": "uuid" },
  "properties": { "title": { "title": [ { "text": { "content": "My Page" } } ] } },
  "markdown": "# Hello\n\nThis is **bold** text.\n\n- A bullet\n- Another bullet\n\n```python\nprint('hi')\n```\n"
}
```

**When to use:** prose-heavy pages where you don't need fine-grained control over which block types are produced. The conversion is mostly what you'd expect:

| Markdown | Notion block |
|---|---|
| `# H1` | NOT emitted (the page title is implicitly H1). Use `## H2` for top-level body sections. |
| `## H2`, `### H3`, `#### H4` | `heading_2`, `heading_3`, `heading_4` |
| Paragraph | `paragraph` |
| `- item` | `bulleted_list_item` |
| `1. item` | `numbered_list_item` |
| `- [ ] todo` | `to_do` |
| `> quote` | `quote` |
| ` ``` ` fenced code | `code` (language inferred from the fence info string) |
| `---` | `divider` |
| `![alt](url)` | `image` |
| `[text](url)` inline | rich_text with `link` |
| `**bold**`, `*italic*`, `~~strike~~`, `` `code` `` | rich_text annotations |
| Table (GFM) | `table` + `table_row` |

**When NOT to use:** when you need callouts, toggles, columns, synced blocks, or any non-Markdown block type. Markdown has no syntax for those. For that, use Option 2 or 3.

**Gotchas:**
- Headings in markdown are 1-indexed but the page title is implicitly the H1 — so your markdown should start at `##`.
- Notion's flavor handles GFM tables but doesn't handle GFM task lists ambiguously when they're inside numbered lists. Stick with simple bullets at the top level.
- The 100-blocks-per-call limit still applies. If your markdown produces > 100 blocks, you'll get a validation error. Split the markdown into chunks and post the page first with the first 100, then append the rest with `PATCH /v1/blocks/{page_id}/children`.

## Option 2: Use a converter library

If your runtime is on an older Notion-Version, or if you want client-side control, use one of these:

- **Python:** [`md2notion`](https://github.com/Cobertos/md2notion), [`notion-md`](https://pypi.org/project/notion-md/), or the wrapper inside `notion-sdk-py` ecosystem
- **Node:** [`@tryfabric/martian`](https://github.com/tryfabric/martian) — most-popular, handles GFM
- **Go:** [`notionapi`](https://github.com/dstotijn/go-notion) ships a converter

These produce the same kind of JSON output as Option 3 (a list of block objects). Use Martian as the default Node choice and md2notion / notion-md as the default Python choice.

## Option 3: Write the conversion yourself

The bundled `scripts/md_to_notion_blocks.py` does this. It's a small but reasonably complete CommonMark → Notion-blocks converter, useful when:
- You're not allowed to call npm/pip
- You need to extend the conversion (e.g., turning specific markdown shapes into callouts)
- You want zero external dependencies

See the script for the implementation. The key shape it produces:

```python
[
    {
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "My Section"}}]
      }
    },
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [
          {"type": "text", "text": {"content": "Some "}},
          {"type": "text", "text": {"content": "bold", "link": null}, "annotations": {"bold": True}},
          {"type": "text", "text": {"content": " text."}}
        ]
      }
    }
]
```

## Extension patterns (markdown → richer blocks)

Plain markdown has no syntax for callouts, toggles, or columns. If you control the input format, you can use conventions:

### Callouts from blockquote with emoji prefix
```markdown
> 💡 Tip: turn this into a callout.
```
A reasonable converter rule: any blockquote whose first character is an emoji → callout with that emoji and the rest as content. (Don't apply this rule for blockquotes that don't start with an emoji.)

### Toggles from `<details>` HTML
```markdown
<details>
<summary>Click to expand</summary>
Hidden content here.
</details>
```
Convert `<details><summary>X</summary>...</details>` → toggle block with X as the rich_text and the body as children.

### Columns from a custom fence
```markdown
::: columns
::: col
content for column 1
:::
::: col
content for column 2
:::
:::
```
Pandoc-style fenced divs. Useful if you need columns and control the source.

These are conventions, not standards. If you adopt them, document them somewhere the user can read.

## Chunking long content

When the converted markdown produces more than 100 blocks, post in chunks:

```python
def post_long_markdown(notion, parent_id, all_blocks):
    # First 100 go with the page create
    first = all_blocks[:100]
    rest = all_blocks[100:]
    page = notion.pages.create(parent={"page_id": parent_id}, children=first)
    # Remaining 100 at a time
    for i in range(0, len(rest), 100):
        notion.blocks.children.append(block_id=page["id"], children=rest[i:i+100])
    return page
```

`scripts/batch_append.py` is a reusable helper for this pattern.

## Going the other way: Notion → markdown

For exports, summaries, or feeding Notion content back to an LLM:

- **Node:** [`notion-to-md`](https://github.com/souvikinator/notion-to-md) — the canonical library
- **Python:** the `notion-sdk-py` ecosystem has several wrappers; `notion2md` is the most popular
- **Hosted services:** Super, Potion, HelpKit all consume Notion and render markdown/HTML

The round-trip (markdown → Notion → markdown) is not lossless. Callouts, toggles, columns, synced blocks, and database embeds either degrade or get dropped. If round-trip fidelity matters, store the canonical markdown separately and treat Notion as a presentation layer.

## A note on agent workflows

Most agents calling this skill will follow one of two patterns:

**Pattern A: User asks for a one-shot page.** Convert the prompt content to markdown, then use Option 1 (native markdown field). Simple, fast, correct for 90% of cases.

**Pattern B: User wants a structured page (dashboard, template, multi-section).** Don't go through markdown. Compose block JSON directly from the templates in `templates.md` and the patterns in `design-patterns.md`. Markdown is a lossy intermediary when you want columns, callouts, and dashboards.

When in doubt, ask the user: "Do you want a clean prose page, or do you want a dashboard-style layout with callouts and columns?" Their answer tells you which option to take.
