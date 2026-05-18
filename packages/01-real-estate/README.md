# Real Estate Skills
**Package:** `@mad-scientist/real-estate` | **7 Skills** | Version 1.0.0

---

## What This Package Does For You

This is your complete real estate research toolkit. It helps you find property owners, look up property details, estimate how much a renovation will cost, and pull real estate data — all without making a single phone call or driving to a courthouse.

Whether you're trying to find a distressed property to buy, track down the owner's contact info to send a mailer, or figure out how much a kitchen remodel should cost — these skills handle the research in seconds.

---

## Skills In This Package

### 1. SDAT Property Search
**What it does:** Searches the Maryland State Department of Assessments and Taxation (SDAT) database — the official Maryland property records. You can look up any property in Maryland by address or owner name and get the assessed value, tax history, ownership date, property size, and more.

**What to say:**  
> "Look up the property at 123 Main Street, Baltimore MD"  
> "Find all properties owned by Smith in zip code 21201"

**What you get:** The property's assessed value, last sale price, tax bill, lot size, building square footage, owner name, and how long they've owned it.

---

### 2. RentCast Property Report
**What it does:** Pulls a full investment analysis for any property — estimated rental value, ARV (after repair value), comparable rents, and market data. Perfect for deciding if a deal makes sense before you sign anything.

**What to say:**  
> "Run a RentCast report on 456 Oak Avenue, Silver Spring MD"

**What you get:** Estimated monthly rent, estimated value after repairs, comparable properties, market absorption rate, and a thumbs up/thumbs down on whether it's a good deal.

---

### 3. Home Depot Repair Estimator
**What it does:** Takes a list of repairs (like "new roof, 2 bathrooms, kitchen remodel") and looks up the actual cost of materials at Home Depot. Gives you a realistic rehab estimate so you don't overpay for a fix-and-flip.

**What to say:**  
> "Estimate a full rehab for a 1,800 sq ft house: roof replacement, 2 bathroom remodels, new kitchen, hardwood floors throughout"

**What you get:** A line-by-line cost estimate for materials, organized by room/project, with Home Depot links for each item.

---

### 4. LandGlide Lookup
**What it does:** Looks up parcel data for any property in the US — gives you the legal description, zoning, GIS data, and property boundaries. Useful when you need more detail than SDAT provides.

**What to say:**  
> "Look up the parcel for 789 Elm Street, Washington DC"

**What you get:** Parcel ID, zoning classification, land use, GIS coordinates, tax jurisdiction, and any liens or encumbrances on record.

---

### 5. BatchData Skip Trace
**What it does:** Takes a list of property addresses and finds the owner's mailing address, phone number, and in some cases email. This is how you find hard-to-reach owners who haven't responded to mailers.

**What to say:**  
> "Skip trace these 10 addresses: [paste list]"

**What you get:** A spreadsheet with owner name, mailing address, phone number, and email for each property — ready to use for direct mail or cold calling lists.

---

### 6. Mad Skip Trace
**What it does:** A more aggressive skip-trace that cross-references multiple databases to find owner contact info. Good for finding people who've gone silent or properties with unusual ownership structures.

**What to say:**  
> "Find the owner of 321 Pine Road, Hyattsville MD — they've been non-responsive for 6 months"

**What you get:** Owner name, best available phone number, mailing address, and a confidence score on how current the data is.

---

### 7. Owner Skip Trace
**What it does:** Given a property address, finds the current owner's contact information using public records. Faster version for single-property lookups.

**What to say:**  
> "Who owns 555 Maple Street, Bethesda MD?"

**What you get:** Owner name, mailing address, and phone number if available.

---

## How To Use This Package

### Installation
```bash
npm install @mad-scientist/real-estate
```

Or symlink into your Hermes skills folder:
```bash
ln -s $(pwd)/skills ~/.hermes/skills/real-estate
```

### Quick Start
```
skill_view(name="rentcast-property-report")
skill_view(name="homedepot-repair-estimator")
```

Then just ask your AI agent to run any of the skills above using natural language.

---

## What To Expect

| Skill | Time to Result | Best For |
|-------|---------------|----------|
| SDAT Property Search | 5-10 seconds | Maryland properties only |
| RentCast Report | 10-20 seconds | Investment deal analysis |
| Home Depot Estimator | 15-30 seconds | Rehab budgeting |
| LandGlide Lookup | 5-15 seconds | Parcel/gIS data |
| BatchData Skip Trace | 30-90 seconds | List of 10+ addresses |
| Mad Skip Trace | 10-20 seconds | Hard-to-find owners |
| Owner Skip Trace | 5-10 seconds | Single property |

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved. Internal use only.
