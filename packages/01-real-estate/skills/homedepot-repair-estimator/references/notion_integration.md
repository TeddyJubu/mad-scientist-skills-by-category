# Notion Integration for Home Depot Property Estimator

## Setup
**No manual setup required!** 

Zapier MCP is already connected to Notion. The skill will:
- Automatically create pages under "Property Estimate HD" parent page
- Handle all authentication via existing MCP connection
- Include 🏠 icon on all property estimate pages

## Notion Page Structure
Each estimate creates a Notion page with:

**Title**: `[Property Address] - [Property Type] - $[Total Cost]`

**Icon**: 🏠 (required by Zapier MCP)

**Properties** (passed in instructions):
- **Address**: Full property address
- **Date**: Date of estimate
- **Property Type**: Room/space type (e.g., "Basement", "Kitchen", "Bedroom")
- **Dimensions**: L x W x H
- **Total Cost**: Grand total materials cost range

**Content**:
- Property condition summary
- Materials breakdown by category
- Product links with pricing
- Quantity calculations with formulas
- Notes and recommendations

## MCP Command Format
```bash
mcporter call zapier notion_create_page \
  "Create Notion page under 'Property Estimate HD' parent for property estimate: [ADDRESS] - [TYPE]. Date: [DATE], Dimensions: [LxWxH], Total Cost: $[AMOUNT]. [SUMMARY]" \
  --icon "🏠" \
  --title "[Address] - [Property Type] - $[Total]"
```

## Implementation
The skill uses `scripts/create_notion_estimate.sh`:

```bash
#!/bin/bash
ADDRESS="$1"
PROPERTY_TYPE="$2"
DATE="$3"
TOTAL_COST="$4"
DIMENSIONS="$5"
SUMMARY="$6"

mcporter call zapier notion_create_page \
  "Create Notion page under 'Property Estimate HD' parent for property estimate: ${ADDRESS} - ${PROPERTY_TYPE}. Date: ${DATE}, Dimensions: ${DIMENSIONS}, Total Cost: \$${TOTAL_COST}. ${SUMMARY}" \
  --icon "🏠" \
  --title "${ADDRESS} - ${PROPERTY_TYPE} - \$${TOTAL_COST}"
```

## Parent Page
- **Name**: `Welcome to Notion`
- **Reason**: This is the default accessible parent page for Zapier MCP
- **Organization**: User can manually move pages to "Property Estimate HD" or other folders after creation
- **Purpose**: Ensures reliable page creation without permission issues

## Notes
- Icon emoji (🏠) is **required** by Zapier MCP for page creation
- Zapier MCP intelligently selects parent page based on instructions
- Page creation is asynchronous - typically completes in 2-5 seconds
- Full estimate content included in instructions parameter
- No need to manually specify parent page ID - MCP finds it by name
