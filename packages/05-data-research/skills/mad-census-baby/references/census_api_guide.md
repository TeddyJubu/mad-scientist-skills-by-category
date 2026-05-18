# Census API Guide

This document provides a basic reference for interacting with the US Census Bureau API.

## Base URL

The base URL for the Decennial Census Summary File 1 (SF1) data for 2020 (used in `census_data_fetcher.py`) is:

`https://api.census.gov/data/2020/dec/sf1`

## Key Parameters

-   `get`: Specifies the variables to retrieve. For example:
    -   `P1_001N`: Total Population (used in the script)
    -   `P1_003N`: Population of one race: White alone
    -   `H1_001N`: Total housing units
-   `for`: Specifies the geographic level and code. For example:
    -   `for=state:XX`: For a specific state (XX is state code)
    -   `for=place:YYYYY&in=state:XX`: For a specific place (city) within a state
    -   `for=zip code tabulation area:ZZZZZ`: For a specific ZIP Code Tabulation Area
-   `in`: Used to specify a geographic component that a requested `for` geography is within (e.g., `in=state:XX`).
-   `key`: Your Census API key.

## Example Endpoints and Variables

### Decennial Census (SF1) - 2020

-   **Endpoint**: `/data/2020/dec/sf1`
-   **Common Variables**:
    -   `P1_001N`: Total Population
    -   `P2_005N`: Hispanic or Latino: Mexican
    -   `H1_001N`: Total Housing Units

### American Community Survey (ACS) - 5-Year Estimates

-   **Endpoint Example**: `/data/2021/acs/acs5` (for 2021 5-year estimates)
-   **Common Variables**:
    -   `B01003_001E`: Total Population (Estimate)
    -   `B19013_001E`: Median Household Income in the past 12 Months (in 2021 Inflation-Adjusted Dollars)

## Geographic Identifiers

-   **State Codes**: Two-digit FIPS codes (e.g., `01` for Alabama, `06` for California, `36` for New York).
-   **Place Codes**: Five-digit FIPS codes for incorporated places and census designated places.
-   **ZIP Code Tabulation Area (ZCTA)**: Five-digit ZCTA codes.

## Finding Variables and Geographies

-   **Census API Discovery Tool**: Use the official Census API website to discover variables and their codes for different datasets.
    -   [https://www.census.gov/data/developers/data-sets.html](https://www.census.gov/data/developers/data-sets.html)
-   **Geographic Lookup**: Use Census geographic files to find codes for states, counties, places, etc.
    -   [https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html](https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html)
