# 20 Sample Prompts for Census Data Skill

## Real Estate & Housing (REI Focus)

1. **"Get median home values for all Maryland counties in 2021"**
   - Perfect for market analysis and investment targeting
   - Variables: `B25077_001E` (median home value), `B25064_001E` (median rent)

2. **"Show me renter vs owner-occupied housing units in Montgomery County, MD"**
   - Identify rental market opportunities
   - Variables: `B25003_002E` (owner-occupied), `B25003_003E` (renter-occupied)

3. **"What's the vacancy rate for housing in Prince George's County, MD?"**
   - Spot oversupply or opportunity zones
   - Variables: `B25002_003E` (vacant units), `B25002_001E` (total units)

4. **"Compare median rent across DC, Montgomery County, and Prince George's County"**
   - Cross-market rental comparisons
   - Variable: `B25064_001E` (median gross rent)

5. **"Get population growth for Virginia counties from 2010 to 2020"**
   - Identify high-growth markets for REI
   - Use Decennial Census 2010 vs 2020 or Population Estimates time series

## Demographics (Tenant/Buyer Profiles)

6. **"What's the median age in all DC metro area counties?"**
   - Target age demographics for marketing
   - Variable: `B01002_001E` (median age)

7. **"Show me median household income for all census tracts in Montgomery County"**
   - Hyper-local income analysis for property targeting
   - Variable: `B19013_001E` (median household income)

8. **"How many households in Baltimore City earn over $100k per year?"**
   - High-income renter/buyer pool sizing
   - Variables: `B19001_013E` through `B19001_017E` (income brackets)

9. **"What percentage of DC residents have a bachelor's degree or higher?"**
   - Education demographics for tenant profiling
   - Variables: `B15003_022E` (bachelor's), `B15003_023E` (master's), `B15003_025E` (doctorate)

10. **"Get poverty rates for all ZIP codes in Baltimore"**
    - Identify distressed areas or opportunity zones
    - Dataset: SAIPE or ACS tract-level poverty estimates

## Business & Economic Data

11. **"How many real estate businesses operate in Fairfax County, VA?"**
    - Competitive analysis
    - Dataset: County Business Patterns, NAICS code `53` (Real Estate)

12. **"Show me total employment and payroll for construction companies in Maryland"**
    - Market health indicators
    - Dataset: CBP, NAICS code `23` (Construction)

13. **"What's the unemployment rate in Prince William County, VA?"**
    - Economic health check
    - Variables: `B23025_005E` (unemployed), `B23025_003E` (labor force)

14. **"List all counties in Virginia ranked by number of tech sector jobs"**
    - Identify white-collar job centers (strong rental demand)
    - Dataset: CBP, NAICS code `54` or `5415` (Professional/Tech Services)

15. **"Get annual payroll data for retail businesses in DC metro area"**
    - Economic activity measurement
    - Dataset: CBP, NAICS code `44-45` (Retail Trade)

## Population & Migration

16. **"What's the total population of the DC-MD-VA metro area (CBSA 47900)?"**
    - Market size for REI campaigns
    - Variable: `B01003_001E` (total population)

17. **"Show me population estimates for Montgomery County from 2015 to 2023"**
    - Long-term growth trends
    - Dataset: Population Estimates time series

18. **"How many people moved into Loudoun County, VA in the last year?"**
    - Migration and demand signals
    - Dataset: ACS Migration Flows

19. **"Get racial and ethnic demographics for all Maryland counties"**
    - Fair housing compliance + market segmentation
    - Variables: `B02001_*` (race), `B03003_003E` (Hispanic/Latino)

20. **"What's the average household size in census tracts with median income over $150k in Northern Virginia?"**
    - Luxury rental/buyer household profiling
    - Variables: `B25010_001E` (average household size), filter by `B19013_001E` > 150000

---

## How to Use These Prompts

Just ask me naturally:
> "Charles: Show me median home values for all Maryland counties in 2021"

I'll:
1. Read the Census Data skill (`SKILL.md`)
2. Translate your request into the correct dataset, year, variables, and geography
3. Run the query via `run-census-query.js`
4. Return results as a markdown table + offer CSV download

No need to know variable codes, FIPS codes, or API syntax — just describe what you want in plain English.

---

**Pro Tip**: Combine prompts for deeper analysis:
- "Get median income AND median rent for Montgomery County census tracts"
- "Show me population, poverty rate, and vacancy rate for Baltimore City ZIP codes"
- "Compare tech sector employment across Fairfax, Loudoun, and Montgomery counties"

The skill handles multi-variable queries, nested geographies, and cross-geography comparisons automatically.
