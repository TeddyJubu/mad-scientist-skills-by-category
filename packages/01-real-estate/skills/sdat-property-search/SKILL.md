---
name: sdat-property-search
description: Search Maryland SDAT Real Property database for property owner, assessment, and tax info — no login required. Use when Charles asks to look up a property in Maryland via SDAT.
---

# SDAT Real Property Search

Search the Maryland Department of Assessments and Taxation (SDAT) Real Property database.
No login required. Works for all Maryland counties including Baltimore City.

## URL

https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx

## Known Browser Automation Pitfalls

This is a legacy ASP.NET government form. It fights browser automation hard. Key lessons learned:

### 1. Close the alert banner FIRST
On page load there is a Tax Credit alert popup banner. Click Close (ref button) before touching any form elements. If you skip this, the dropdowns may not respond correctly.

### 2. Use keyboard navigation for dropdowns — NOT browser_click on option refs
The county and search method dropdowns do NOT respond reliably to clicking option refs directly (they timeout or silently fail). Instead:
- Click the combobox ref to focus it
- Use `browser_press(key="ArrowDown")` repeatedly to reach the desired option
- Baltimore City = 3 ArrowDown presses from -Select one-
- Street Address = 1 ArrowDown press from -Select one-

### 3. Do NOT use Enter to submit the address form
The page has a site-wide search bar in the header. Pressing Enter in any form field submits the HEADER search bar, not the address form — and redirects to a different page (or Facebook via social links). Always click the "Next" button ref explicitly.

### 4. The "Next" button is NOT a navigation link — it's a form submit
It looks like a button next to "New Search" and "Previous". It must be clicked by its button ref, not via keyboard shortcuts.

### 5. URL parameters don't work
This ASP.NET site ignores URL query parameters (e.g. `?County=03&SearchType=ADDR`). The form must be filled out interactively — you cannot skip steps by crafting a URL.

### 6. Type carefully — verify field refs before typing
The street number and street name are two separate textboxes. Verify which ref is which with browser_snapshot before typing. The first textbox is street number (e.g. "944"), the second is street name (e.g. "N HILL"). Do NOT include street suffix (Road, Ave, etc.).

### 7. The header search bar STEALS keystrokes
The site-wide header search bar (ref e7 or similar) can absorb typed text if focus is unclear. Always explicitly browser_click() the target textbox ref IMMEDIATELY before browser_type() — even if you think it's focused. If text lands in the wrong field (e.g. street number shows "N HIL"), it means the header bar captured the first keystrokes. Clear and retype carefully.

### 8. Session restart is your friend
If the form gets into a bad state (wrong text in fields, unexpected redirects), do a full browser_navigate() back to the SDAT URL and start over from step 1. Do not try to recover a broken form session.

## Step-by-Step Workflow

```
1. browser_navigate("https://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx")
2. browser_snapshot() — find the Close button ref for the alert
3. browser_click(close_button_ref)
4. browser_click(county_combobox_ref)
5. browser_press("ArrowDown") × N  (3x for Baltimore City)
6. browser_click(search_method_combobox_ref)
7. browser_press("ArrowDown") × 1  (for Street Address)
8. browser_click(continue_button_ref)
9. browser_snapshot() — find street number textbox ref and street name textbox ref
10. browser_click(street_number_ref)  — click to focus first
11. browser_type(street_number_ref, "944")
12. browser_click(street_name_ref)    — click to focus
13. browser_type(street_name_ref, "N HILL")  — no suffix, no period
14. browser_click(next_button_ref)    — DO NOT use Enter
15. browser_snapshot() — read results
```

## County Arrow-Down Count Reference

| County | Arrow presses |
|--------|--------------|
| ALLEGANY | 1 |
| ANNE ARUNDEL | 2 |
| BALTIMORE CITY | 3 |
| BALTIMORE COUNTY | 4 |
| CALVERT | 5 |
| (continue pattern...) | |

## What SDAT Shows

- Owner name and mailing address
- Property account identifier (parcel ID)
- Assessed value (land + improvements)
- Use code / property class
- Deed reference
- Sale price and date (most recent transfer)
- Tax credit status

## Alternative: MDLandRec

For deed/title documents (not just assessment data), use MDLandRec (https://landrec.msa.maryland.gov) — but this REQUIRES login credentials. Ask Charles for his MDLandRec email/password before attempting.

## Notes

- SDAT may be unavailable before 7:00 AM ET for maintenance
- Data is for informational purposes only — not for legal documents
- Baltimore City and Baltimore County are separate entries — be precise
