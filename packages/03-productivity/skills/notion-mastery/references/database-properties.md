# Database Properties Cheatsheet

Every database property type, with three payloads for each:
- **Schema** — defining the property when creating or updating a database
- **Page value** — setting the property on a page (database row)
- **Filter** — querying for this property in `POST /v1/databases/{id}/query`

For the broader filter grammar and compound filters, see `api-reference.md` §5.

---

## `title` (required — exactly one per database)

**Schema:**
```json
{ "Name": { "title": {} } }
```
The schema key is the property name. There must be exactly one `title` property per database.

**Page value:**
```json
{ "Name": { "title": [ { "type": "text", "text": { "content": "My page" } } ] } }
```
Array of rich_text. Limit 200 chars total.

**Filter:**
```json
{ "property": "Name", "title": { "contains": "search" } }
```
Operators: `equals`, `does_not_equal`, `contains`, `does_not_contain`, `starts_with`, `ends_with`, `is_empty`, `is_not_empty`.

---

## `rich_text`

**Schema:** `{ "Description": { "rich_text": {} } }`

**Page value:**
```json
{ "Description": { "rich_text": [ { "type": "text", "text": { "content": "Notes here" } } ] } }
```

**Filter:** same operators as `title`.

---

## `number`

**Schema:**
```json
{ "Price": { "number": { "format": "dollar" } } }
```
Formats: `number`, `number_with_commas`, `percent`, `dollar`, `canadian_dollar`, `euro`, `pound`, `yen`, `ruble`, `rupee`, `won`, `yuan`, `real`, `lira`, `rupiah`, `franc`, `hong_kong_dollar`, `new_zealand_dollar`, `krona`, `norwegian_krone`, `mexican_peso`, `rand`, `new_taiwan_dollar`, `danish_krone`, `zloty`, `baht`, `forint`, `koruna`, `shekel`, `argentine_peso`, `chilean_peso`, `colombian_peso`, `dirham`, `riyal`, `philippine_peso`.

**Page value:** `{ "Price": { "number": 42.99 } }` — pass `null` to clear.

**Filter:**
```json
{ "property": "Price", "number": { "greater_than": 100 } }
```
Operators: `equals`, `does_not_equal`, `greater_than`, `less_than`, `greater_than_or_equal_to`, `less_than_or_equal_to`, `is_empty`, `is_not_empty`.

---

## `select`

**Schema:**
```json
{ "Category": { "select": { "options": [
  { "name": "Bug", "color": "red" },
  { "name": "Feature", "color": "green" },
  { "name": "Chore", "color": "gray" }
] } } }
```
Colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`.

**Page value:** `{ "Category": { "select": { "name": "Bug" } } }`

**Filter:** `{ "property": "Category", "select": { "equals": "Bug" } }`
Operators: `equals`, `does_not_equal`, `is_empty`, `is_not_empty`.

---

## `multi_select`

**Schema:** like `select` but options can be assigned multiple per row.

**Page value:** `{ "Tags": { "multi_select": [ { "name": "engineering" }, { "name": "Q3" } ] } }`

**Filter:** `{ "property": "Tags", "multi_select": { "contains": "engineering" } }`
Operators: `contains`, `does_not_contain`, `is_empty`, `is_not_empty`.

---

## `status`

**Schema:**
```json
{ "Status": { "status": {} } }
```
**Important:** unlike `select`, you can't define `options` for `status` at create time via the API in versions before 2026-04-01. Notion auto-creates "Not started / In progress / Done" with corresponding groups. To customize: create the property, then either guide the user to do it in the UI, or use the Views API on 2026-04-01+.

**Page value:** `{ "Status": { "status": { "name": "In progress" } } }`

**Filter:** `{ "property": "Status", "status": { "equals": "In progress" } }`
Same operators as `select`.

**Status vs Select:** `status` exposes its grouping (To-do / In progress / Complete) to board views automatically and is the right choice for any workflow state. `select` for orderless tags.

---

## `date`

**Schema:** `{ "Due Date": { "date": {} } }`

**Page value:**
```json
{ "Due Date": { "date": {
  "start": "2026-05-16",
  "end": null,
  "time_zone": null
} } }
```
- Date-only: `"start": "2026-05-16"`.
- Date-time: `"start": "2026-05-16T15:00:00.000Z"`.
- Range: `"end"` is the range end; `"start"` is the start.
- `time_zone`: an IANA tz like `"America/New_York"`.

**Filter:**
```json
{ "property": "Due Date", "date": { "next_week": {} } }
{ "property": "Due Date", "date": { "on_or_after": "2026-05-01" } }
```
Operators: `equals`, `before`, `after`, `on_or_before`, `on_or_after`, `past_week`, `past_month`, `past_year`, `this_week`, `next_week`, `next_month`, `next_year`, `is_empty`, `is_not_empty`.

---

## `people`

**Schema:** `{ "Owner": { "people": {} } }`

**Page value:**
```json
{ "Owner": { "people": [ { "object": "user", "id": "user-uuid" } ] } }
```

**Filter:** `{ "property": "Owner", "people": { "contains": "user-uuid" } }`
Operators: `contains`, `does_not_contain`, `is_empty`, `is_not_empty`.

---

## `files`

**Schema:** `{ "Attachments": { "files": {} } }`

**Page value:**
```json
{ "Attachments": { "files": [
  { "type": "external", "name": "spec.pdf",
    "external": { "url": "https://example.com/spec.pdf" } }
] } }
```
URL capped at 2000 chars. Notion-hosted files require File Upload API.

**Filter:** only `is_empty` and `is_not_empty` are supported.

---

## `checkbox`

**Schema:** `{ "Done": { "checkbox": {} } }`

**Page value:** `{ "Done": { "checkbox": true } }`

**Filter:** `{ "property": "Done", "checkbox": { "equals": true } }`

---

## `url`, `email`, `phone_number`

All share the same shape — string-valued, with type-specific validation hints in Notion's UI but not enforced via API.

**Schema:** `{ "Website": { "url": {} } }`

**Page value:** `{ "Website": { "url": "https://example.com" } }`

**Filter:** same string operators as `rich_text`.

---

## `formula`

**Schema:**
```json
{ "Days Left": { "formula": { "expression": "dateBetween(prop(\"Due Date\"), now(), \"days\")" } } }
```
Formulas use Notion's formula language (separate from JavaScript despite the surface similarity). Common patterns:
- `prop("Property Name")` to reference another property.
- `if(condition, then, else)`
- `dateBetween(date1, date2, "days" | "hours" | ...)`
- `format(number_or_date)` to convert to string.
- `concat(string1, string2)` to join.
- `slice(string, start, end)` to substring.
- `length(string_or_list)` for size.

For non-trivial formulas, point users to Red Gregory's formula reference (`ecosystem-resources.md`).

**Page value:** read-only. Formulas evaluate server-side; you can't set a value.

**Filter:**
```json
{ "property": "Days Left", "formula": { "number": { "less_than": 7 } } }
```
Wraps the underlying type's filter: `string`, `number`, `checkbox`, or `date`.

---

## `relation`

**Schema:**
```json
{ "Project": { "relation": {
  "database_id": "linked-db-uuid",
  "type": "single_property",
  "single_property": {}
} } }
```
For dual properties (creates a reverse property on the linked database):
```json
{ "type": "dual_property",
  "dual_property": { "synced_property_name": "Tasks" } }
```
Both databases must share the integration's access — relations across permission boundaries fail silently.

**Page value:** `{ "Project": { "relation": [ { "id": "related-page-uuid" } ] } }`

**Filter:** `{ "property": "Project", "relation": { "contains": "related-page-uuid" } }`
Operators: `contains`, `does_not_contain`, `is_empty`, `is_not_empty`.

---

## `rollup`

**Schema:**
```json
{ "Total Tasks": { "rollup": {
  "relation_property_name": "Tasks",
  "rollup_property_name": "Status",
  "function": "count"
} } }
```
Functions: `count`, `count_values`, `count_unique_values`, `count_empty`, `count_not_empty`, `percent_empty`, `percent_not_empty`, `sum`, `average`, `median`, `min`, `max`, `range`, `earliest_date`, `latest_date`, `date_range`, `checked`, `unchecked`, `percent_checked`, `percent_unchecked`, `show_original`, `show_unique`.

**Page value:** read-only.

**Filter:** like formula, wraps the underlying type:
```json
{ "property": "Total Tasks", "rollup": { "any": { "number": { "greater_than": 0 } } } }
```
Wrappers: `any`, `every`, `none`, `number`, `date`.

---

## `created_time`, `created_by`, `last_edited_time`, `last_edited_by`

All read-only. Notion fills them automatically.

**Schema:** `{ "Created": { "created_time": {} } }`

**Filter:** time fields use date operators; user fields use people operators.

---

## `unique_id`

**Schema:**
```json
{ "Ticket": { "unique_id": { "prefix": "TASK" } } }
```
Auto-generates incrementing IDs like `TASK-1`, `TASK-2`. Read-only on the page side.

**Filter:** uses number operators on the underlying numeric portion.

---

## `button`

**Schema:** `{ "Quick Action": { "button": {} } }`

Buttons execute UI-side actions (open template, add rows, etc.). Read-only via API; configure their behavior in the Notion UI.

---

## Updating a database schema

`PATCH /v1/databases/{id}` accepts a `properties` object where each key is the property name. Special semantics:

- **Add a property:** include it in the patch with its schema.
- **Rename a property:** set `{ "Old Name": { "name": "New Name" } }`.
- **Change a property's type:** set `{ "Property Name": { "<new_type>": {...} } }`. **Warning:** this can destroy data — Notion attempts to coerce but failures lose the original values.
- **Add a select/status option:** patch the property with the new option in `options`. Existing options must be re-listed (the array is a replacement, not a merge).
- **Delete a property:** set `{ "Property Name": null }`.

Always fetch the current schema before patching — overwriting an options array with a partial list deletes the missing options.

## Property design rules of thumb

- **Title first, always.** It's the only property that's always visible everywhere.
- **8 properties is the sweet spot. 12 is the ceiling.** Beyond that, table views become unscannable.
- **Status is for workflow, select is for taxonomy, multi_select is for tags.** Don't mix these up.
- **Add a relation before a duplicate property.** If two databases share a concept, link them — don't copy the field.
- **Rollups are read-only — they need a relation first.** Plan the relation, then add the rollup.
- **Formulas can reference rollups.** Useful for derived metrics like "is overdue", "weeks until launch".
- **Don't use `created_time` as your primary date.** It's the wrong property — use a real `date` property and let users edit it.
