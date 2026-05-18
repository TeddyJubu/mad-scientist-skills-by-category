# Firehose Example Queries

## Real Estate / REI Use Cases

### 1. Brand Mentions (Chucky Buys Lucky Houses)
```
title:chucky AND language:"en" AND NOT url:/.*\\/page\\/[0-9]+.*/ AND NOT url:*\\/category\\/* AND NOT url:*\\/tag\\/*
```

### 2. Competitor Mentions (HomeVestors, Offerpad, Opendoor)
```
(title:homevestors OR title:offerpad OR title:opendoor) AND language:"en" AND recent:24h
```

### 3. REI News & Articles
```
(added:"real estate" OR added:"property investing") AND page_category:"/News" AND recent:7d
```

### 4. Probate Listings
```
(added:probate OR added:"estate sale") AND page_type:"/Listing/Property" AND language:"en"
```

### 5. Foreclosure/Distressed Properties
```
(added:foreclosure OR added:"short sale" OR added:"distressed property") AND language:"en"
```

### 6. REI Education & Courses
```
(added:"real estate investing" OR added:"rental property") AND (page_type:"/Article/How_to" OR page_type:"/Article/Tutorial_or_Guide") AND recent:7d
```

---

## Marketing / Business Use Cases

### 7. AI + Real Estate
```
(added:"artificial intelligence" OR added:"AI automation") AND added:"real estate" AND recent:24h
```

### 8. GoHighLevel Mentions
```
(title:gohighlevel OR title:"go high level" OR domain:gohighlevel.com) AND language:"en"
```

### 9. Competitor Blog Posts (TechCrunch example)
```
domain:techcrunch.com AND page_type:"/Article" AND recent:7d
```

### 10. Lead Magnet Ideas (How-To Content)
```
(title:"how to" OR title:"step by step") AND page_category:"/Business_and_Industrial" AND recent:7d
```

---

## Content Discovery

### 11. Viral YouTube Videos (mentions)
```
(added:"youtube" OR added:"viral video") AND page_category:"/Arts_and_Entertainment/Online_Media" AND recent:24h
```

### 12. Product Launches (Tech)
```
(added:"new product" OR added:"just launched") AND page_category:"/Computers_and_Electronics" AND recent:24h
```

### 13. Industry Reports (REI)
```
(added:"market report" OR added:"housing market") AND page_type:"/Document/Report" AND language:"en"
```

---

## Advanced Patterns

### 14. Exclude Junk URLs (pagination, tags, categories)
```
title:tesla AND NOT url:/.*\\/page\\/[0-9]+.*/ AND NOT url:*\\/category\\/* AND NOT url:*\\/tag\\/*
```

### 15. Domain Filter + Keyword
```
domain:zillow.com AND added:"investment property"
```

### 16. Multi-Language (English + Spanish)
```
title:propiedades AND (language:"en" OR language:"es")
```

### 17. Recency + Quality Filters
```
title:openai AND recent:1h AND quality:true
```

### 18. Exclude Adult Content (default behavior, but explicit)
```
title:dating AND nsfw:false
```

---

## Tips

1. **Use `quality:true` (default)** to filter out pagination, category, and tag URLs automatically.
2. **Combine `recent:` with keywords** for real-time monitoring (e.g., `recent:1h`, `recent:24h`).
3. **Escape slashes in URL patterns:** `\\/` for wildcards, `\\/` inside regex `/.../.../`.
4. **Test queries incrementally:** start simple (`title:keyword`), then add filters (`AND language:"en"`).
5. **Use tags** to organize rules (e.g., `"brand-mentions"`, `"competitor-tracking"`).

---

## Limits

- **25 rules max** per organization
- **Max 24-hour replay** via `since` parameter
- **Timeout: 1-300 seconds** (default 300s)

---

## External Reference

Full Lucene syntax: [https://firehose.com/api-docs#lucene-query-syntax](https://firehose.com/api-docs#lucene-query-syntax)
