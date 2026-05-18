# Reference Documentation for Rentcast Property Report

This document summarizes the Rentcast API endpoints used in the `generate_report.py` script.



## Base URL

`https://api.rentcast.io/v1`

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/properties` | Fetches detailed property records for a given address. |
| GET | `/avm/value` | Retrieves an Automated Valuation Model (AVM) sale price estimate and comparable sales. |
| GET | `/avm/rent/long-term` | Retrieves an AVM long-term rent estimate and comparable rentals. |
| GET | `/markets` | Fetches zip code-level market statistics for sales and rentals. |

## Authentication

All requests must include your API key in the `X-Api-Key` header.
