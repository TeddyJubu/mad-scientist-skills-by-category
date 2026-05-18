# Example: Poverty Estimates for Virginia Counties (SAIPE 2021)

## Query
Get poverty rate and median household income for all counties in Virginia (state FIPS 51) using Small Area Income and Poverty Estimates (SAIPE).

## Command
```bash
./run-census-query.js \
  --dataset timeseries/poverty/saipe \
  --year 2021 \
  --variables NAME,SAEPOVRTALL_PT,SAEMHI_PT \
  --for "county:*" \
  --in "state:51" \
  --time 2021 \
  --output va-poverty.csv
```

## API URL
```
https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEPOVRTALL_PT,SAEMHI_PT&for=county:*&in=state:51&time=2021&key=YOUR_KEY
```

## Variables
- `NAME` — County name
- `SAEPOVRTALL_PT` — All ages in poverty (percent)
- `SAEMHI_PT` — Median household income (dollars)
- `time=2021` — Year (required for time series datasets)

## Expected Output (sample)
| NAME | SAEPOVRTALL_PT | SAEMHI_PT | state | county | time |
|------|----------------|-----------|-------|--------|------|
| Loudoun County, Virginia | 3.6 | 156821 | 51 | 107 | 2021 |
| Fairfax County, Virginia | 5.9 | 133974 | 51 | 059 | 2021 |
| Buchanan County, Virginia | 23.8 | 38013 | 51 | 027 | 2021 |

## Notes
- **SAIPE** provides poverty and income estimates for states, counties, and school districts
- Virginia counties with **lowest poverty**:
  - Falls Church City: 2.8%
  - Loudoun County: 3.6%
  - Arlington County: 5.1%
- Virginia counties with **highest poverty**:
  - Buchanan County: 23.8%
  - Lee County: 21.7%
  - Dickenson County: 20.4%
- Time series datasets require `&time=YYYY` parameter
- SAIPE is released annually (typically December for prior year data)
