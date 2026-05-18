# Example: Population by State (2021 ACS 5-Year)

## Query
Get total population for all 50 states + DC using ACS 5-Year estimates.

## Command
```bash
./run-census-query.js \
  --dataset acs/acs5 \
  --year 2021 \
  --variables NAME,B01003_001E \
  --for "state:*" \
  --output population-by-state.csv
```

## API URL
```
https://api.census.gov/data/2021/acs/acs5?get=NAME,B01003_001E&for=state:*&key=YOUR_KEY
```

## Variables
- `NAME` — State name
- `B01003_001E` — Total population (estimate)

## Expected Output (first 5 rows)
| NAME | B01003_001E | state |
|------|-------------|-------|
| Alabama | 5024279 | 01 |
| Alaska | 733391 | 02 |
| Arizona | 7151502 | 04 |
| Arkansas | 3011524 | 05 |
| California | 39538223 | 06 |

## Notes
- ACS 5-Year provides the most reliable estimates for all geographies
- State FIPS codes: 01=AL, 02=AK, 04=AZ, 05=AR, 06=CA, etc.
- Use `B01003_001M` to get margin of error
