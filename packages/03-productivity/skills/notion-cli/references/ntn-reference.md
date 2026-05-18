## Known Limitations (2026-05)

| Issue | Workaround |
|---|---|
| `ntn api PATCH` to `blocks/…/children` returns exit 0 but writes **zero** blocks | Use `curl` or Python `urllib.request` directly against `https://api.notion.com/v1/blocks/<id>/children` |
| `icon: null` in block payload causes **400 validation_error** | Omit the `icon` field entirely; never set it to `null` |
| `ntn pages` has no `delete` subcommand | PATCH `https://api.notion.com/v1/pages/<id>` with `{"archived": true}` |
| `ntn doctor` warns Workers unavailable but worker commands work | Trust successful `ntn workers` commands; ignore stale doctor warnings |
| Token from env not picked up reliably for all subcommands | Read token explicitly: `grep NOTION_TOKEN /root/.hermes/notion.env | cut -d= -f2` |
| `rich_text` array has mixed annotation states (plain + bold in one array) | **400 validation_error** — "annotations should be not present" | Use helper functions `t()` / `ta()` that build one `rich_text` dict at a time with consistent structure; never put plain text and annotated text in the same `rich_text` list |
| `table` / `table_row` block type | **400 validation_error** | Not supported by the 2022-06-28 API. Use bulleted lists with pipe-separated values or a grid layout instead |
| Callout block with `icon` field set | **400 "embed should be defined"** validation error | Omit `icon` entirely from callout blocks; use `color` (blue/yellow/red/green/gray) only |
| Publishing via API (`{"public": true}` in PATCH) | **400 "should be not present"** | Notion Site publishing is a UI action. Read `public_url` from the page object after creation and share that directly. The URL resolves even without explicit publishing. |