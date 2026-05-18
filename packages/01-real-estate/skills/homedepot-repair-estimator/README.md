# Home Depot Property Repair Estimator

**Version**: 1.0  
**Created**: 2026-03-26  
**Author**: James (OpenClaw Agent)

## Overview
This skill analyzes property images to identify needed repairs, searches Home Depot for required materials, and generates contractor-style estimates with pricing.

## Workflow
1. **Image Analysis**: Identifies damage, missing elements, and repair needs
2. **Material Search**: Queries Home Depot API for relevant products
3. **Estimate Generation**: Creates formatted materials list with pricing

## Files
- `SKILL.md`: Main skill workflow and instructions
- `scripts/search_homedepot.sh`: Home Depot search helper script
- `references/estimate_template.md`: Report formatting template

## Requirements
- SerpApi API key (configured)
- `jq` for JSON parsing
- `curl` for API requests
- Image analysis capability

## Usage
**Trigger**: User sends property image + requests repair estimate

**Example**:
> [User sends image of damaged room]
> "What materials do I need from Home Depot to fix this?"

**Agent Response**:
1. Analyzes image
2. Searches Home Depot for materials
3. Generates estimate report
4. Delivers formatted markdown

## Output
- Markdown estimate saved to `/data/.openclaw/workspace/estimates/`
- Formatted table with product details, pricing, quantities
- Total cost calculation
- Direct links to Home Depot products

## API Details
- **Provider**: SerpApi
- **Endpoint**: `https://serpapi.com/search?engine=home_depot`
- **Key**: Stored in skill configuration
- **Rate Limits**: Standard SerpApi limits apply

## Testing
To test the search script:
```bash
cd /data/.openclaw/workspace/skills/homedepot-repair-estimator
./scripts/search_homedepot.sh "drywall repair kit"
```

## Notes
- Estimates are materials-only (no labor)
- Quantities based on visible damage
- Pricing is real-time from Home Depot
- All products link to Home Depot for ordering
