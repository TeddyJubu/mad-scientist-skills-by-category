# Census Data API - Quick Reference

## Common Datasets

| Dataset | Code | Use For |
|---------|------|---------|
| ACS 5-Year | `acs/acs5` | Most reliable demographic data, all geographies |
| ACS 1-Year | `acs/acs1` | Most recent data, areas 65k+ population |
| Decennial Census 2020 | `dec/pl` | Official population counts, redistricting data |
| County Business Patterns | `cbp` | Business statistics by industry/geography |
| Population Estimates | `pep/population` | Annual population estimates by demographics |
| SAIPE Poverty | `timeseries/poverty/saipe` | Poverty rates and median income by county |
| Economic Census | `ecnbasic` | Comprehensive business data (every 5 years) |

## Common Variables

### Population
- `B01003_001E` — Total population
- `B01001_001E` — Total population (with age/sex breakdown available)
- `B01002_001E` — Median age
- `B02001_002E` — White alone
- `B03003_003E` — Hispanic or Latino

### Housing
- `B25001_001E` — Total housing units
- `B25003_002E` — Owner-occupied housing units
- `B25003_003E` — Renter-occupied housing units
- `B25077_001E` — Median home value
- `B25064_001E` — Median gross rent

### Income & Poverty
- `B19013_001E` — Median household income
- `B19301_001E` — Per capita income
- `B17001_002E` — Population below poverty level
- `B17001_001E` — Population for whom poverty status is determined

### Education
- `B15003_022E` — Bachelor's degree
- `B15003_023E` — Master's degree
- `B15003_025E` — Doctorate degree

### Employment
- `B23025_003E` — Civilian labor force
- `B23025_005E` — Unemployed

## Geography Codes (FIPS)

### States (DMV Focus)
- `24` — Maryland
- `11` — District of Columbia
- `51` — Virginia

### Maryland Counties
- `031` — Montgomery County
- `033` — Prince George's County
- `005` — Baltimore County
- `003` — Anne Arundel County
- `027` — Howard County
- `013` — Carroll County
- `025` — Harford County
- `017` — Charles County
- `021` — Frederick County
- `510` — Baltimore City

### Virginia Counties (Northern VA)
- `059` — Fairfax County
- `013` — Arlington County
- `107` — Loudoun County
- `153` — Prince William County
- `510` — Alexandria City
- `610` — Falls Church City

### DC Metro Area (CBSA)
- `47900` — Washington-Arlington-Alexandria, DC-VA-MD-WV Metro Area

## Geography Syntax

### All States
```
&for=state:*
```

### All Counties in Maryland
```
&for=county:*&in=state:24
```

### Specific County (Montgomery County, MD)
```
&for=county:031&in=state:24
```

### All Counties in DC Metro Area
```
&for=county:*&in=metropolitan%20statistical%20area/micropolitan%20statistical%20area:47900
```

### All Census Tracts in Montgomery County
```
&for=tract:*&in=state:24&in=county:031
```

## Query Templates

### Template 1: State-Level Demographic Data
```bash
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E,B19013_001E \
  --for "state:*"
```

### Template 2: County-Level Data for One State
```bash
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E,B19013_001E \
  --for "county:*" \
  --in "state:24"
```

### Template 3: Single County Deep Dive
```bash
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E,B19013_001E,B25077_001E,B25064_001E \
  --for "county:031" \
  --in "state:24"
```

### Template 4: Business Data by Industry
```bash
./run-census-query.js \
  --dataset cbp \
  --year 2021 \
  --variables NAME,ESTAB,EMP,PAYANN \
  --NAICS2017 54 \
  --for "county:*" \
  --in "state:24"
```

### Template 5: Poverty Estimates
```bash
./run-census-query.js \
  --dataset timeseries/poverty/saipe \
  --year 2021 \
  --variables NAME,SAEPOVRTALL_PT,SAEMHI_PT \
  --for "county:*" \
  --in "state:24" \
  --time 2021
```

## NAICS Industry Codes (Common)

- `23` — Construction
- `44-45` — Retail Trade
- `52` — Finance and Insurance
- `53` — Real Estate and Rental and Leasing
- `54` — Professional, Scientific, and Technical Services
- `5415` — Computer Systems Design and Related Services
- `62` — Health Care and Social Assistance
- `72` — Accommodation and Food Services

## Tips

1. **Always include `NAME`** in your variables list for readable output
2. **Use ACS 5-Year for most queries** (most reliable, all geographies)
3. **Include margin of error** (`_M` suffix) for statistical rigor
4. **Check variable lists** before querying: `https://api.census.gov/data/{year}/{dataset}/variables.html`
5. **Use wildcards** to explore: `state:*`, `county:*`
6. **Nest geographies** with `&in=`: counties within states, tracts within counties
7. **Output to CSV** for Excel analysis: `--output results.csv`

## Rate Limits

- **With API key**: Unlimited (fair use expected)
- **Without key**: 500 requests/day per IP

Your API key is pre-configured in `.secrets/census.env`.

---

**Quick Help**: Read `SKILL.md` for full documentation, `README.md` for examples.
