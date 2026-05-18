# Census Data Skill

Fetch demographic, economic, housing, and business data from the U.S. Census Bureau Data API.

## Quick Start

```bash
# Test the skill with a simple query
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E \
  --for "state:*"
```

## What This Skill Does

- Queries the U.S. Census Bureau Data API
- Supports 50+ datasets (ACS, Decennial, Economic Census, Business Patterns, Population Estimates, etc.)
- Handles complex geography queries (states, counties, metros, tracts, block groups)
- Returns data as JSON or CSV
- Stores your API key securely in `.secrets/census.env`

## Common Use Cases

### 1. Population Data
```bash
# Total population by state (2021)
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E \
  --for "state:*" \
  --output population.csv
```

### 2. Income & Poverty
```bash
# Median household income for Maryland counties
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B19013_001E,B19013_001M \
  --for "county:*" \
  --in "state:24"
```

### 3. Business Data
```bash
# Tech sector establishments in Montgomery County, MD
./run-census-query.js \
  --dataset cbp \
  --year 2021 \
  --variables NAME,ESTAB,EMP,PAYANN \
  --NAICS2017 54 \
  --for "county:031" \
  --in "state:24"
```

### 4. Poverty Estimates
```bash
# Poverty rates for Virginia counties
./run-census-query.js \
  --dataset timeseries/poverty/saipe \
  --year 2021 \
  --variables NAME,SAEPOVRTALL_PT,SAEMHI_PT \
  --for "county:*" \
  --in "state:51" \
  --time 2021
```

## Files

- **SKILL.md** — Complete API reference and documentation
- **run-census-query.js** — CLI script to execute queries
- **.secrets/census.env** — API key (already configured)
- **examples/** — Sample queries with expected output

## Key Concepts

### Datasets
- **ACS 5-Year** (`acs/acs5`) — Most reliable, all geographies down to block group
- **ACS 1-Year** (`acs/acs1`) — Most recent, areas 65,000+ population
- **Decennial Census** (`dec/pl`) — Every 10 years, complete population count
- **County Business Patterns** (`cbp`) — Business statistics by industry/geography
- **SAIPE** (`timeseries/poverty/saipe`) — Poverty and income estimates

### Geography Codes (FIPS)
- **State**: 2-digit code (01=AL, 24=MD, 51=VA)
- **County**: 3-digit code within state (031=Montgomery County, MD)
- **Wildcard**: Use `*` for all geographies (`state:*` = all states)
- **Nesting**: Use `&in=` for parent geographies (`&for=county:*&in=state:24`)

### Variables
- Find variables at: `https://api.census.gov/data/{year}/{dataset}/variables.html`
- **ACS variables**: `B#####_###E` (estimate), `B#####_###M` (margin of error)
- **Common variables**:
  - `B01003_001E` — Total population
  - `B19013_001E` — Median household income
  - `B17001_002E` — Population below poverty level

### Output Formats
- **JSON** (default): `--format json`
- **CSV**: `--format csv` or `--output file.csv`
- **Markdown table**: Automatically printed to console for JSON responses

## Advanced Features

### Group Queries (Entire Tables)
```bash
# Get all variables in ACS Table B02015 (Asian Alone by Detailed Group)
./run-census-query.js \
  --dataset acs/acs1 \
  --year 2019 \
  --variables "group(B02015)" \
  --for "state:*"
```

### Descriptive Labels
```bash
# Add variable labels to output
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E \
  --for "state:*" \
  --descriptive
```

### Direct URL Queries
```bash
# Use a pre-built Census API URL
./run-census-query.js \
  --url "https://api.census.gov/data/2021/acs/acs5?get=NAME,B01003_001E&for=state:*"
```

## Resources

- **Census API Home**: https://www.census.gov/data/developers/data-sets.html
- **API Discovery Tool**: https://api.census.gov/data.html
- **User Guide**: https://www.census.gov/data/developers/guidance/api-user-guide.html
- **FIPS Codes**: https://www.census.gov/library/reference/code-lists/ansi.html

## Examples

See the `examples/` directory for:
- Population by state
- Median income by county
- Business patterns (tech sector)
- Poverty estimates

---

**Version**: 1.0.0  
**Author**: James  
**API Key**: Configured in `.secrets/census.env`
