# Data Research Skills
**Package:** `@mad-scientist/data-research` | **14 Skills** | Version 1.0.0

---

## What This Package Does

Web research, public data, search, scraping, SEO, and source collection

## Skills In This Package

### 1. apify-actor-finder
**Folder:** `skills/apify-actor-finder`

Finds the best Apify actor for a web scraping or data extraction task, runs it via the Apify API, and delivers the results as a CSV file. Use this skill whenever a user wants to scrape a website or extract data from any platform (e.g. Google Maps, Twitter/X, Instagram, Facebook, TikTok, LinkedIn, Amazon, real estate sites, etc.). This skill handles the full workflow: finding the actor, running it, and returning results.

### 2. brave-search
**Folder:** `skills/brave-search`

brave-search lets the user search the web and extract content via the Brave Search API, which is useful when they need quick answers, fact checks, documentation lookups, or want to pull structured content from websites without running a full browser or web crawler.

### 3. census-data
**Folder:** `skills/census-data`

Fetch demographic, economic, and population data from the U.S. Census Bureau API. Use this skill when you need population statistics, housing data, business patterns, income/poverty estimates, or any U.S. government statistical data at national, state, county, metro, tract, or block group levels.

### 4. firecrawl
**Folder:** `skills/firecrawl`

firecrawl lets the user scrape, crawl, and map websites into clean markdown, which is useful when they need to extract content from pages, audit site structures, build knowledge bases from web sources, or feed structured web content into AI workflows without broken HTML or layout artifacts.

### 5. firehose
**Folder:** `skills/firehose`

firehose lets the user monitor the web in real-time by creating Lucene query rules that track specific keywords, domains, or page types and stream matching results via Server-Sent Events, which is useful when they want to track brand mentions, competitor activity, news alerts, or website changes as they happen instead of polling manually.

### 6. mad-census-baby
**Folder:** `skills/mad-census-baby`

Fetches demographic and census data from the US Census Bureau API based on user-provided location information (city, state, zip code, or address). Outputs data in markdown, CSV, or basic PDF format. Use this skill when you need to retrieve population, housing, or economic data for a specific geographic area.

### 7. melissa-data-information
**Folder:** `skills/melissa-data-information`

melissa-data-information lets the user look up a single property address or process a CSV of multiple addresses to enrich them with Melissa Data property and ownership information, which is useful when they want to verify addresses, get property characteristics, or add structured property data to leads without manual research.

### 8. arxiv
**Folder:** `skills/arxiv`

Search arXiv papers by keyword, author, category, or ID.

### 9. blogwatcher
**Folder:** `skills/blogwatcher`

Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool.

### 10. llm-wiki
**Folder:** `skills/llm-wiki`

Karpathy's LLM Wiki: build/query interlinked markdown KB.

### 11. ml-paper-writing
**Folder:** `skills/ml-paper-writing`

Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, verifying citations, or preparing camera-ready submissions. Includes LaTeX templates, reviewer guidelines, and citation verification workflows.

### 12. polymarket
**Folder:** `skills/polymarket`

Query Polymarket: markets, prices, orderbooks, history.

### 13. research-paper-writing
**Folder:** `skills/research-paper-writing`

Write ML papers for NeurIPS/ICML/ICLR: design→submit.

### 14. seo-audit
**Folder:** `skills/seo-audit`

seo-audit lets the user audit, review, and diagnose SEO issues on their website by checking on-page elements, meta tags, technical health, and ranking factors, which is useful when they want to understand why they are not ranking, identify quick wins, or get a structured health check before pursuing a broader SEO strategy.

## Agent Install

```bash
npm install @mad-scientist/data-research
```

Or copy the `skills/` directory into your agent skills root.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
