# Content Sources & Search Strategy

This document describes the sources and search strategies used by the REI AI Weekly newsletter.

## Content Categories

### 1. AI News for Real Estate
**Goal:** Find recent news about AI adoption, innovation, and trends in real estate investing.

**Sources:**
- General tech news sites (TechCrunch, VentureBeat, The Verge)
- Real estate tech publications (Inman, HousingWire)
- AI-focused news (AI Business, VentureBeat AI)

**Search queries:**
- "AI real estate investing news"
- "artificial intelligence property investment"
- "machine learning real estate technology"

**Filters:**
- Published within last 7 days
- Relevance to real estate investors (not just agents/brokers)

### 2. New AI Tools
**Goal:** Discover new AI-powered tools and platforms useful for real estate investors.

**Sources:**
- Product Hunt (AI category + Real Estate category)
- There's An AI For That
- AI tool directories
- Company launch announcements

**Search queries:**
- "AI tools real estate investors"
- "AI CRM real estate"
- "AI property analysis software"
- "real estate automation tools"

**Filters:**
- Launched or updated within last 7 days
- Applicable to investor workflows (not just listing/marketing)

### 3. Trending Automations
**Goal:** Highlight practical automation workflows, integrations, and use cases.

**Sources:**
- Zapier/Make.com community showcases
- Real estate investor forums (BiggerPockets, Reddit r/realestateinvesting)
- YouTube tutorial channels
- LinkedIn posts from automation experts

**Search queries:**
- "real estate AI automation workflow"
- "AI CRM automation real estate"
- "automated lead generation real estate"

**Filters:**
- Actionable and replicable
- Clear ROI or efficiency gain

### 4. YouTube Videos
**Goal:** Feature high-quality video tutorials, reviews, and case studies.

**Search queries:**
- "AI for real estate investors automation"
- "AI tools real estate wholesaling"
- "ChatGPT real estate investing"
- "AI lead generation real estate"

**Filters:**
- Published within last 7 days
- Minimum 1000 views (quality threshold)
- Channels focused on real estate investing (not general tech)

**Priority channels:** (Add trusted channels here as you discover them)

### 5. Reddit
**Goal:** Surface high-engagement discussions, tool recommendations, and real-world experiences.

**Subreddits:**
- r/realestateinvesting
- r/realtors
- r/artificial
- r/automation

**Search queries:**
- "AI tool" in r/realestateinvesting
- "automation" in r/realestateinvesting
- "ChatGPT" in r/realestateinvesting

**Filters:**
- Posts from last 7 days
- Minimum 10 upvotes or 5 comments

## Quality Criteria

Content is selected based on:
1. **Relevance:** Directly applicable to real estate investors (not just agents/homeowners)
2. **Recency:** Published/updated within last 7 days
3. **Actionability:** Provides clear takeaways or next steps
4. **Credibility:** From reputable sources or with social proof (upvotes, views, engagement)

## Search Optimization

The `aggregate_content.py` script uses these search strategies:
- Combines multiple keywords to improve precision
- Filters by date to ensure freshness
- Deduplicates results across sources
- Ranks by engagement metrics (views, upvotes, etc.)
