# Example: County Business Patterns - Tech Sector in Montgomery County, MD (2021)

## Query
Get number of establishments, employees, and annual payroll for the Professional, Scientific, and Technical Services sector (NAICS 54) in Montgomery County, Maryland.

## Command
```bash
./run-census-query.js \
  --dataset cbp \
  --year 2021 \
  --variables NAME,ESTAB,EMP,PAYANN \
  --NAICS2017 54 \
  --for "county:031" \
  --in "state:24" \
  --output montgomery-tech.json
```

## API URL
```
https://api.census.gov/data/2021/cbp?get=NAME,ESTAB,EMP,PAYANN&NAICS2017=54&for=county:031&in=state:24&key=YOUR_KEY
```

## Variables
- `NAME` — Geography name
- `ESTAB` — Number of establishments
- `EMP` — Mid-March employment
- `PAYANN` — Annual payroll ($1,000)
- `NAICS2017=54` — Professional, Scientific, and Technical Services

## Expected Output
| NAME | ESTAB | EMP | PAYANN | state | county | NAICS2017 |
|------|-------|-----|--------|-------|--------|-----------|
| Montgomery County, Maryland | 7428 | 96847 | 9472881 | 24 | 031 | 54 |

## Notes
- **7,428 establishments** in tech/professional services
- **96,847 employees** (mid-March snapshot)
- **$9.47 billion** in annual payroll
- NAICS codes:
  - 54 = Professional, Scientific, and Technical Services
  - 5415 = Computer Systems Design and Related Services
  - 5417 = Scientific Research and Development Services
- Use `NAICS2017=5415` for more specific computer/tech industries
