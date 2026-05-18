# Beautiful Websites Workflow

This document explains how the 4-step pipeline works in detail.

## Overview

```
scrape → qualify → redesign → deploy
```

The pipeline is designed to run either with pauses (default) or automatically (`--auto` flag). Pauses allow Charles to review results before moving forward, which is important because the scrape step costs money and the qualify step is subjective.

---

## Step 1: Scrape Leads

**Input:** User provides niche + city (e.g. "nail salons in Austin TX")

**Output:** `scrape_results.json` — array of business objects

**Process:**

1. Parse user input into:
   - **Search query** (business type only, e.g. "nail salons")
   - **Location** (city/region only, e.g. "Austin TX")
   - **Country code** (optional, e.g. "us", "au", "gb") — infer from context or ask

2. Before running, calculate cost and get approval:
   - Default max: 20 places
   - Cost: $4 per 1,000 places
   - Example: "I'm about to scrape 20 places, which will cost approximately $0.08. OK to proceed?"

3. Start Apify run via API:
   ```bash
   POST https://api.apify.com/v2/acts/lukaskrivka~google-maps-with-contact-details/runs?token={APIFY_TOKEN}
   ```

4. Poll every 8 seconds until `status === "SUCCEEDED"`

5. Download results from dataset

6. Filter to businesses with:
   - A `website` field (not empty)
   - At least one entry in the `emails` array
   - Website that is NOT a Facebook/Yelp/Instagram page
   - Name that is NOT a national chain

7. Save to `scrape_results.json`

8. **Pause (default):** Show count and table with name, website URL, email. Ask: "Proceed to qualify?"

---

## Step 2: Qualify Leads

**Input:** `scrape_results.json`

**Output:** `qualify_results.json` — array with `qualify: "YES"` or `"NO"` per lead

**Process:**

1. Check `qualify_results.json` — skip any lead already processed

2. Check `sites/build-log.md` — skip any business name or website URL already in the log (deduplicate against previous runs)

3. For each remaining lead:
   - Run `node scripts/screenshot.js --url {website} --out screenshots/{slug}.png`
   - Read the PNG image directly with vision
   - Apply qualification criteria (YES if ANY signal is present, NO only if ALL premium signals are present)
   - Return `YES`, `NO`, or `SKIP` with a one-line reason

4. Save to `qualify_results.json`

5. **Pause (default):** Show YES/NO breakdown with reasons. Ask: "Proceed to redesign?"

**Qualification criteria:** See SKILL.md for full criteria. The bar is HIGH — most local business sites will be a YES.

---

## Step 3: Redesign Sites

**Input:** `qualify_results.json` (YES leads only)

**Output:** `sites/{slug}/index.html` per lead + updated `sites/build-log.md`

**Process:**

1. For each lead where `qualify === "YES"`:

   a. Use `web_fetch` to scrape their current website content

   b. Check `sites/build-log.md` to see which design combos have been used

   c. Pick a unique palette + font + layout combination from the design system

   d. Search Unsplash for 2–3 photos relevant to the business type

   e. Verify each photo URL loads (200 status) before using it

   f. Generate a complete `index.html` file with:
      - All CSS in `<style>`
      - All JS in `<script>`
      - Real content from the scraped site (no placeholders)
      - 6 sections: Navbar, Hero, Services, Philosophy, Contact, Footer
      - GSAP animations
      - Responsive design (375px mobile, 1440px desktop)

   g. Save to `sites/{business-slug}/index.html`

   h. Append to `sites/build-log.md`:
      - Business name, slug, palette, font, layout, date

2. **Pause (default):** Describe each site built (design choices, key content). Ask: "Deploy these?"

**Architecture rules:** See SKILL.md for full rules. Key points:

- One file only (no separate CSS/JS files)
- No frameworks (no React, Vue, Tailwind build, npm)
- CDN only (Google Fonts, GSAP, Lucide Icons)
- Dynamic copyright year (never hardcode)

---

## Step 4: Deploy to Vercel

**Input:** `sites/` folder (subfolders with `index.html` files)

**Output:** Live Vercel URLs logged to `sites/build-log.md`

**Process:**

1. Check if `VERCEL_TOKEN` is set in `.env`
   - If yes, use `--token {VERCEL_TOKEN}` flag
   - If no (local), ensure `vercel login` has been run

2. For each site folder in `sites/`:
   - Run `vercel deploy --yes --prod sites/{slug}`
   - Capture the live URL from output (e.g. `https://zen-nail-bar.vercel.app`)
   - **Wait 10 seconds** (Vercel rate-limits rapid CLI deploys)

3. Update `sites/build-log.md` with Vercel URL for each deployed site

4. Print final summary table:

   | Business | Old Site | Qualify | Vercel URL |
   |----------|----------|---------|------------|
   | Zen Nail Bar | zennailbar.com | YES | https://zen-nail-bar.vercel.app |

---

## Pause Behavior

### Default (no flag)

Pause after each step:

1. After scrape → show lead count + list (name, website, email)
2. After qualify → show YES/NO breakdown with reasons
3. After redesign → describe each site built, explain how to preview
4. After deploy → show final summary table

### With `--auto`

Skip all pauses and print the summary at the end only. Only use when Charles explicitly requests it.

---

## File Structure

```
workspace/
├── .env
│   ├── APIFY_TOKEN (required)
│   └── VERCEL_TOKEN (optional for local, required for remote/SSH)
├── scrape_results.json (leads from Apify)
├── qualify_results.json (YES/NO per lead)
├── screenshots/
│   └── {slug}.png (full-page screenshots)
└── sites/
    ├── build-log.md (tracks design combos + Vercel URLs)
    └── {business-slug}/
        └── index.html (single-file site)
```

---

## Timing

- Scrape 20 places: 2–5 minutes
- Screenshot + qualify 10 sites: ~3 minutes
- Redesign 5 sites: ~15 minutes
- Deploy 5 sites: ~2 minutes
- **Total: ~25 minutes for 5 live redesigns**

---

## Cost Breakdown

| Step | Cost | Notes |
|------|------|-------|
| Scrape | $4 per 1,000 places | Apify API usage |
| Qualify | Free | Local Playwright + vision |
| Redesign | Free | Local generation |
| Deploy | Free | Vercel Hobby plan |

**Total cost for 20 leads:** ~$0.08 (scrape only)

---

## Good Niches

Businesses that care about design and have budget to pay for it:

- Nail salons
- Med spas & Botox clinics
- Hair salons & barbershops
- Massage & wellness studios
- Wedding venues & planners
- Boutique hotels / B&Bs

**Avoid:**

- National chains
- Franchises
- Restaurants (razor-thin margins)
- Lawyers (already have agencies)

---

## Deduplication Strategy

To avoid redesigning the same business twice:

1. **Before qualifying:** Check `sites/build-log.md` for business name or website URL
2. **During scrape:** Filter out national chains by name
3. **During qualify:** Mark as `SKIP` if already in build log

This allows you to run the pipeline multiple times for the same niche/city without duplicating work.

---

## Preview Before Deploy

You can preview generated sites locally before deploying:

**Local machine:** Open `sites/{slug}/index.html` directly in your browser.

**Remote / SSH setup:** Start a temporary web server:

```bash
cd sites && python3 -m http.server 8080 --bind 127.0.0.1
```

Then visit `http://localhost:8080/{slug}/` in your browser. If using VS Code Remote SSH, the port will be forwarded automatically.

---

## Troubleshooting

See SKILL.md for full troubleshooting section.

Quick fixes:

- **Screenshots fail:** Run `npx playwright install-deps chromium` (Linux)
- **Scrape returns 0 leads:** Try `--max 50` or broader location
- **Deploy fails:** Run `vercel login` (local) or add `VERCEL_TOKEN` to `.env` (remote)
- **Node.js errors:** Upgrade to Node.js 18+
