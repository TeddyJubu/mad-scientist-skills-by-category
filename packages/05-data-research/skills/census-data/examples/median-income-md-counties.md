# Example: Median Household Income for Maryland Counties (2021 ACS 5-Year)

## Query
Get median household income for all counties in Maryland (state FIPS 24).

## Command
```bash
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B19013_001E,B19013_001M \
  --for "county:*" \
  --in "state:24" \
  --output md-income.csv
```

## API URL
```
https://api.census.gov/data/2021/acs/acs5?get=NAME,B19013_001E,B19013_001M&for=county:*&in=state:24&key=YOUR_KEY
```

## Variables
- `NAME` — County name
- `B19013_001E` — Median household income (estimate)
- `B19013_001M` — Margin of error

## Expected Output (sample)
| NAME | B19013_001E | B19013_001M | state | county |
|------|-------------|-------------|-------|--------|
| Montgomery County, Maryland | 111737 | 1344 | 24 | 031 |
| Howard County, Maryland | 124042 | 2890 | 24 | 027 |
| Baltimore County, Maryland | 83962 | 1116 | 24 | 005 |

## Notes
- Maryland counties ranked by median income (2021):
  1. Howard County: $124,042
  2. Montgomery County: $111,737
  3. Calvert County: $109,024
- Always include margin of error (`_M` suffix) for statistical rigor
- County FIPS codes are 3 digits within each state
