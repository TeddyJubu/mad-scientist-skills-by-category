# Troubleshooting

Symptom → diagnosis → fix lookup for common Notion API failures. When you hit an error, search this file first.

## Authentication and permission errors

### 401 `unauthorized` / "API token is invalid"
- **Cause:** Bearer token missing, malformed, or revoked.
- **Fix:** Verify the `Authorization: Bearer <token>` header. Internal integration tokens start with `secret_` (older) or `ntn_` (newer). OAuth tokens have their own prefix.

### 403 `restricted_resource`
- **Cause:** Integration doesn't have access to this resource — usually because the page/database wasn't explicitly shared with the integration.
- **Fix:** In Notion UI, open the page → click `...` → "Add connections" → select your integration. Or for an entire workspace, configure connection at the workspace level. The integration owner must do this; you can't grant access via API.

### 404 `object_not_found`
- **Cause:** Often misleading. The ID exists, but the integration can't see it (same as 403 in many cases). Or the ID is wrong.
- **Fix:** Verify the UUID is correct. Then check whether the page is shared with the integration. Notion returns 404 to avoid leaking existence to unauthorized callers.

## Validation errors

### 400 `validation_error: body failed validation`
Read the `message` field — it usually tells you exactly which path failed. Common variants:

**"... should be a non-empty string"** → You sent `""` or `null` where a string was required.

**"... should be defined"** → You omitted a required field. Common offenders:
- Page create: missing `parent`
- Block create: missing the type-keyed sub-object (e.g., you sent `{ "type": "heading_2" }` without `"heading_2": {...}`)
- Property: missing the type-keyed sub-object (e.g., `{ "Tags": { "multi_select": [...] } }` not `{ "Tags": [...] }`)

**"`property` (Status) is expected to be of type ..."** → Property name doesn't match schema, or you're sending the wrong value shape. Fetch the schema to verify exact names (case-sensitive).

**"`children` must be a list of block objects"** → You're sending a single block instead of an array, or you're sending raw text/markdown where a block JSON array is expected.

### 400 "Invalid request URL"
- **Cause:** Usually a typo in the path or a missing/extra `/v1/`.
- **Fix:** Base URL is `https://api.notion.com/v1`. Common endpoints:
  - `/v1/pages` (POST create, GET/PATCH by ID)
  - `/v1/databases/{id}` (GET, PATCH)
  - `/v1/databases/{id}/query` (POST)
  - `/v1/blocks/{id}` (GET, PATCH, DELETE)
  - `/v1/blocks/{id}/children` (GET, PATCH = append)
  - `/v1/search` (POST)
  - `/v1/users` (GET list, GET `/me`)

### 400 `missing_version`
- **Cause:** `Notion-Version` header missing.
- **Fix:** Always include `Notion-Version: 2025-09-03` (or whichever version your integration targets).

## Rate limits

### 429 `rate_limited`
- **Cause:** Exceeded 3 requests/sec average.
- **Fix:** Read the `Retry-After` header (seconds) and sleep. Backoff strategy: respect Retry-After first, then exponential (1s, 2s, 4s, 8s) for retries on 5xx.
- **Prevention:** Batch where possible. One `PATCH /blocks/{id}/children` with 100 children is much better than 100 separate calls.

## Block / page issues

### Page created but body content is missing
- **Cause:** `children` was empty, malformed, or sent as a separate update that failed.
- **Fix:** Verify the children array in your create call has the expected blocks. Confirm each block has the `{ "type": "...", "<type>": {...} }` shape.

### "First-level children exceeded the maximum of 100"
- **Cause:** You sent > 100 blocks in a single create or append.
- **Fix:** Split into batches of ≤ 100. Use `scripts/batch_append.py`.

### "Nesting too deep"
- **Cause:** Trying to create > 2 levels of nesting in one call (e.g., a column_list containing a column containing a toggle containing children).
- **Fix:** Create the outer structure first, then append the deeper children in a follow-up call.

### Rich text content rejected as too long
- **Cause:** Each rich_text element's `content` > 2000 chars.
- **Fix:** Chunk the string into multiple text elements within the same rich_text array. `scripts/chunk_rich_text.py` does this.

### Headings I made toggleable have no children even though I provided them
- **Cause:** Heading children only persist when `is_toggleable: true` was set at create time. If you create a heading then later set `is_toggleable: true` and append children, behavior varies by version.
- **Fix:** Set `is_toggleable: true` in the same call that creates the heading, and include `children` in that call. Don't try to mutate it later.

## Database issues

### Property name mismatch in update
- **Cause:** Property name on the page payload doesn't match the schema exactly (case-sensitive, whitespace-sensitive).
- **Fix:** Fetch `GET /v1/databases/{id}` and use the exact `properties` keys. "Due Date" ≠ "due date" ≠ "DueDate".

### "Option does not exist" when setting a select value
- **Cause:** The option name you're sending isn't in the property's schema.
- **Fix:** Either (a) PATCH the database first to add the option, or (b) verify the schema's `options` and pick an existing one. Note: in some cases Notion will auto-create the option, but this behavior is fragile — prefer explicit option management.

### Relation field set but the related page doesn't show the reverse
- **Cause:** Single-property relations don't auto-create a reverse. Only `dual_property` relations do.
- **Fix:** If you need bidirectional visibility, recreate the relation as `dual_property` with a `synced_property_name`.

### Rollup value is `null` or missing
- **Cause:** The underlying relation has no linked pages, or the rollup property is misconfigured.
- **Fix:** Verify the relation is populated, then verify `relation_property_name` and `rollup_property_name` in the rollup schema match exactly.

### Status property created but I can't add custom options
- **Cause:** Status options can only be configured in the UI or via the Views/Status API on `2026-04-01+`.
- **Fix:** On older versions, accept the defaults ("Not started", "In progress", "Done") and tell the user to customize via UI. On `2026-04-01+`, use the new endpoints.

## Search and query issues

### Newly-created page doesn't appear in search results
- **Cause:** Notion's search index is eventually consistent; freshly-created content takes seconds to minutes to index.
- **Fix:** Don't rely on search for "find what I just created". Use the IDs returned from creation. For "find recent", `POST /v1/databases/{id}/query` with `sort: [{"timestamp": "created_time", "direction": "descending"}]` is more reliable.

### Database query returns empty even though I know rows exist
- **Cause:** Filter mismatch (wrong property name, wrong type-wrapper). Or the integration doesn't have access to the database.
- **Fix:** Try the query with no filter — if rows return, your filter is wrong. If no rows return, it's a permissions issue.

### Pagination loop never terminates
- **Cause:** Not threading `start_cursor` correctly, or assuming `has_more: false` happens on the last call but it can take an additional call to return empty.
- **Fix:** Standard pattern:
  ```python
  cursor = None
  while True:
      resp = notion.databases.query(database_id=id, start_cursor=cursor, page_size=100)
      yield from resp["results"]
      if not resp.get("has_more"):
          break
      cursor = resp["next_cursor"]
  ```

## Webhook issues

### Webhook events not arriving
- **Cause:** Subscription verification failed, endpoint returns non-2xx, or Notion is in the middle of its 24h retry backoff.
- **Fix:** Verify subscription on Notion's integration settings page — there's a verification challenge that your endpoint must respond to. Once verified, check the integration's "Recent deliveries" log.

### Webhook signature verification failing
- **Cause:** Wrong secret, wrong hash algorithm, or signed-payload not exactly matching what you're verifying.
- **Fix:** Notion uses HMAC-SHA256 of the raw request body with the subscription's verification secret. Verify the raw bytes — don't re-serialize JSON first.

## Versioning

### "field X not recognized" on a new version's endpoint
- **Cause:** You're on an older `Notion-Version` that doesn't know about the field.
- **Fix:** Either upgrade the `Notion-Version` header or omit the field. Note that upgrading versions can break existing code — read the migration guides at developers.notion.com/docs/upgrade-guide-* before bumping.

### `data_source_id` not found on database
- **Cause:** Pre-`2025-09-03` databases have a single data source that's implicit. The new model exposes data sources explicitly.
- **Fix:** On `2025-09-03+`, fetch the database, read `data_sources[0].id`. Older code paths that assumed one-to-one still work for backward compatibility but newer endpoints want the data source ID.

## When to give up and ask the user

If you've retried, verified the payload, and the error message doesn't match anything here:

1. Confirm the integration has access to the affected page/database in the Notion UI.
2. Check developers.notion.com for the endpoint — version-specific behaviors sometimes change subtly.
3. Search the Notion Developers Slack or recent r/Notion posts for the exact error message.
4. As a last resort, log the full request/response and ask the user to share with their admin.

## Diagnostic checklist for any failure

When something's wrong, run through this in order:

1. **Headers**: `Authorization`, `Notion-Version`, `Content-Type: application/json` all present?
2. **Parent**: is `parent.page_id` or `parent.database_id` correct for the operation?
3. **Property names**: do they match the schema exactly (case + whitespace)?
4. **Property shapes**: each property value wrapped in `{ "<type>": {...} }`?
5. **Block shapes**: each block has `{ "type": "<t>", "<t>": {...} }`?
6. **Rich text length**: any single text element > 2000 chars?
7. **Children count**: ≤ 100?
8. **Nesting depth**: ≤ 2 from the root of this call?
9. **Integration access**: is this page/database actually shared with the integration?
10. **Version**: is the endpoint/feature available at the version you're sending?

Nine out of ten failures are in this list.
