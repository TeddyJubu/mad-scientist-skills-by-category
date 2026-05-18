# Data & Research Skills
**Package:** `@mad-scientist/data-research` | **12 Skills** | Version 1.0.0

---

## What This Package Does For You

This package turns your AI agent into a world-class research assistant. It can scrape websites, find business contacts, pull demographic data, audit SEO, and search the web at scale. If you need to find information — a list of businesses, a person's contact details, market data for a neighborhood — this package finds it.

Think of it as hiring a researcher who never gets tired, never misses a detail, and can look at everything on the internet at once.

---

## Skills In This Package

### 1. Apollo Find (B2B Contact Database)
**What it does:** Searches Apollo's database of 200M+ business contacts. Find anyone at any company — their email, phone number, LinkedIn URL, and job title. Perfect for outbound sales or finding decision-makers.

**What to say:**  
> "Find me all property managers in Baltimore MD with 50+ units, and get their work emails"

**What you get:** A spreadsheet of contacts with name, title, company, email, phone, and LinkedIn URL.

---

### 2. Brave Search
**What it does:** A private, ad-free web search that your AI agent can use to research any topic. Searches the full web and returns structured results. No tracking, no ads, no Google censoring.

**What to say:**  
> "Research the top 10 real estate investing blogs in Maryland and tell me what topics they cover most"

**What you get:** A structured list of results with titles, URLs, and summaries — no ads, no tracking.

---

### 3. Apify Runner
**What it does:** Runs web scraping robots (Apify Actors) through Apify's cloud platform. Scrape any website at scale — Google Maps listings, real estate portals, job boards, competitor sites. If the data is publicly visible on a website, this can pull it.

**What to say:**  
> "Scrape all the real estate agents on Google Maps in zip code 21201 and give me their names, ratings, and review counts"

**What you get:** A structured dataset (CSV or JSON) with all the scraped information, ready to import into a spreadsheet or CRM.

---

### 4. Apify Actor Finder
**What it does:** Finds the right Apify scraping tool for your specific job. Types in what you want to scrape and it recommends the best pre-built robot for the job.

**What to say:**  
> "I need to scrape LinkedIn profiles — what's the best Apify actor for that?"

**What you get:** The name of the best Apify actor for your task, a link to it, and instructions for running it.

---

### 5. Apify MCP
**What it does:** Connects Apify to your AI agent as a tool it can use directly — so your agent can trigger web scraping jobs as part of a larger workflow without you manually starting them.

**What to say:**  
> "Run a web scrape of all apartments listed for rent in 21201 and add the results to a spreadsheet"

**What you get:** Spreadsheet populated with scraped rental listings, no manual scraping required.

---

### 6. Census Data
**What it does:** Pulls US Census Bureau data — demographics, income levels, housing statistics, population figures — for any geographic area. Essential for real estate investment analysis.

**What to say:**  
> "Get the median household income, unemployment rate, and housing vacancy rate for zip code 21220"

**What you get:** A structured data table with all the census metrics for that area, with year-over-year comparisons where available.

---

### 7. Mad Census Baby
**What it does:** A simplified, user-friendly version of the Census data tool specifically designed for real estate analysis. Pulls exactly the metrics REI investors care about — population growth, income, housing stock age — for any market.

**What to say:**  
> "Give me a demographic snapshot of the Baltimore metro area for real estate investing purposes"

**What you get:** A clean report with the 8-10 key metrics every real estate investor needs, written in plain English with a recommendation on whether the market looks promising.

---

### 8. SEO Audit
**What it does:** Analyzes any website's SEO health — checks page speed, mobile-friendliness, keyword usage, backlinks, and technical issues. Tells you exactly what's broken and what to fix first.

**What to say:**  
> "Run a full SEO audit on my website realestateleads.com and tell me the top 5 issues to fix"

**What you get:** A prioritized report of SEO issues with specific fix-it instructions for each one.

---

### 9. Firecrawl
**What it does:** Scrapes entire websites and converts them into clean, readable text and markdown — perfect for analyzing competitor sites, aggregating content, or building datasets from web pages.

**What to say:**  
> "Scrape all the blog posts from this real estate investing website so I can analyze what topics they cover"

**What you get:** All website content in clean text format, organized by page, ready to read or analyze.

---

### 10. Firehose
**What it does:** Sets up real-time web monitoring — gets notified the moment something changes on a website, a new listing appears, or a competitor updates their pricing. Like a Google Alert but for anything on the web.

**What to say:**  
> "Monitor the listings page of this MLS reo site and alert me whenever a new property under $100k appears"

**What you get:** Instant Telegram notification when a new listing matches your criteria, with a direct link.

---

### 11. Melissa Data Information
**What it does:** Property data lookup using Melissa Data — the property owner's mailing address, phone number, and property characteristics for any US address.

**What to say:**  
> "Look up the property record for 123 Main Street, Baltimore MD using Melissa Data"

**What you get:** Owner name, mailing address, phone (if available), property characteristics, and any recorded liens.

---

### 12. Research
**What it does:** A general-purpose research tool that uses multiple sources — academic papers, news articles, industry reports — to give you a comprehensive answer to complex questions.

**What to say:**  
> "Research the best exit strategies for fix-and-flip properties in a rising interest rate environment"

**What you get:** A structured research summary with key findings, data sources cited, and a recommended approach.

---

## How To Use This Package

### Installation
```bash
npm install @mad-scientist/data-research
```

Or symlink into your Hermes skills folder:
```bash
ln -s $(pwd)/skills ~/.hermes/skills/data-research
```

### Quick Start
```
skill_view(name="apollo-find")
skill_view(name="census-data")
skill_view(name="seo-audit")
```

---

## What To Expect

| Skill | Time to Result | Best For |
|-------|---------------|----------|
| Apollo Find | 10-30 seconds | B2B contacts |
| Brave Search | 5-15 seconds | Private web search |
| Apify Runner | 1-5 minutes | Large-scale scraping |
| Apify Actor Finder | 5-10 seconds | Finding the right scraper |
| Apify MCP | 10-30 seconds | Automated scraping workflow |
| Census Data | 10-30 seconds | Demographics & income |
| Mad Census Baby | 15-30 seconds | REI-focused demographics |
| SEO Audit | 30-90 seconds | Website health check |
| Firecrawl | 1-5 minutes | Full website content |
| Firehose | Real-time | Web change monitoring |
| Melissa Data | 5-15 seconds | Property records lookup |
| Research | 1-3 minutes | Deep-dive research |

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved. Internal use only.
