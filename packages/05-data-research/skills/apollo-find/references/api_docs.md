# Apollo.io API Reference

Base URL: `https://api.apollo.io/api/v1`
Auth header: `x-api-key: YOUR_KEY`

---

## People Search — `/mixed_people/api_search` (POST)

**Does NOT consume credits. Does NOT return emails/phones.**

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `person_titles[]` | array | Job titles (partial match). e.g. `["real estate investor"]` |
| `person_titles_fuzzy_match` | bool | Default true; set false for strict title match |
| `person_locations[]` | array | Where person lives: city, state, country |
| `person_seniorities[]` | array | See seniority levels below |
| `organization_locations[]` | array | Company HQ location |
| `organization_domains[]` | array | Company domains (up to 1,000) |
| `organization_ids[]` | array | Apollo company IDs |
| `organization_num_employees_ranges[]` | array | e.g. `["1,50", "51,200"]` |
| `revenue_range[min]` | number | Min company revenue (no symbols) |
| `revenue_range[max]` | number | Max company revenue (no symbols) |
| `currently_using_any_of_technology_uids[]` | array | Tech stack (use underscores) |
| `currently_using_all_of_technology_uids[]` | array | Must use ALL listed techs |
| `currently_not_using_any_of_technology_uids[]` | array | Exclude by tech |
| `q_keywords` | string | Free-text search |
| `email_statuses[]` | array | verified, unverified, likely to engage, unavailable |
| `page` | int | Page number (1-500) |
| `per_page` | int | Results per page (max 100) |
| `prospected_by_current_team` | string | yes/no — exclude already prospected |

### Seniority Levels
`owner`, `founder`, `c_suite`, `partner`, `vp`, `head`, `director`, `manager`, `senior`, `entry`, `intern`

### Response Schema
```json
{
  "people": [
    {
      "id": "apollo_id",
      "first_name": "John",
      "last_name": "Smith",
      "name": "John Smith",
      "title": "CEO",
      "linkedin_url": "https://linkedin.com/in/...",
      "city": "Baltimore",
      "state": "Maryland",
      "country": "United States",
      "organization": {
        "name": "Acme Corp",
        "primary_domain": "acme.com",
        "industry": "real estate",
        "num_employees": 25,
        "keywords": ["real estate", "investing"]
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_entries": 4823,
    "total_pages": 193
  }
}
```

---

## Organization Search — `/mixed_companies/search` (POST)

**Consumes credits.**

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `organization_domains[]` | array | Domain names |
| `organization_num_employees_ranges[]` | array | Headcount ranges |
| `organization_locations[]` | array | HQ location |
| `organization_not_locations[]` | array | Exclude HQ locations |
| `revenue_range[min]` | number | Min revenue |
| `revenue_range[max]` | number | Max revenue |
| `q_organization_keyword_tags[]` | array | Industry keywords |
| `q_organization_name` | string | Company name (partial OK) |
| `organization_ids[]` | array | Apollo company IDs |
| `currently_using_any_of_technology_uids[]` | array | Tech filters |
| `page` / `per_page` | int | Pagination |

---

## People Enrichment — `/people/match` (POST)

**Consumes credits. Returns emails/phones.**

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `first_name` | string | Person's first name |
| `last_name` | string | Person's last name |
| `email` | string | Known email (improves match) |
| `domain` | string | Company domain (no www/@) |
| `organization_name` | string | Company name |
| `linkedin_url` | string | LinkedIn profile URL |
| `reveal_personal_emails` | bool | Include personal emails |
| `reveal_phone_number` | bool | Include phone numbers |

### Tips
- More data = better match accuracy
- Minimum viable: name + domain OR name + email
- Returns 200 even if no match — check `person` field in response

---

## Common Technology Filters
Replace spaces and periods with underscores:
- `salesforce`, `hubspot`, `google_analytics`, `wordpress_org`, `mailchimp`, `shopify`, `linkedin_insight_tag`, `google_ads`, `facebook_ads`

## Rate Limits
- People Search: no hard limit but add `time.sleep(0.5)` between pages
- Enrichment: based on your Apollo plan credits
- Display limit: 50,000 records per search (100/page × 500 pages)
