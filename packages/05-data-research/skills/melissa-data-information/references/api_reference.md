# Melissa Property API Reference

This document provides a summary of the key endpoints and data groups for the Melissa Property API.

## Base URL

`https://property.melissadata.net`

## Endpoints

| Endpoint | Description |
|---|---|
| `/v4/WEB/LookupProperty` | Looks up a property by address, FIPS/APN, or MAK. |
| `/v4/WEB/LookupDeeds` | Retrieves historical deed and transaction information. |
| `/v4/WEB/LookupHomesByOwner` | Finds other properties owned by the same individual. |

## Key Column Groups

When requesting data, you can specify column groups to retrieve related sets of information. The `GrpAll` group returns all available data.

| Group Name | Description |
|---|---|
| `GrpParcelInfo` | Basic parcel information (FIPS, APN, land use). |
| `GrpOwnerInfo` | Property owner's name and mailing address. |
| `GrpTaxInfo` | Tax assessment and exemption details. |
| `GrpValueInfo` | Assessed value, market value, and last sale price. |
| `GrpStructureInfo` | Details about the physical structure (square footage, rooms, year built). |
| `GrpMortgage1` / `GrpMortgage2` | Information on the first and second mortgages. |
| `GrpDocInfo` | Deed document information. |
| `GrpTxDefInfo` | Deed transaction details. |
