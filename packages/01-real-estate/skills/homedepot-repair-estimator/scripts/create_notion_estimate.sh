#!/bin/bash
# Create Notion page for Home Depot estimate via Zapier MCP
# Uses existing MCP connection - no manual setup required

ADDRESS="$1"
PROPERTY_TYPE="$2"
DATE="$3"
TOTAL_COST="$4"
DIMENSIONS="$5"
SUMMARY="$6"

if [ -z "$ADDRESS" ] || [ -z "$PROPERTY_TYPE" ]; then
  echo "Usage: $0 <address> <property_type> <date> <total_cost> <dimensions> <summary>"
  exit 1
fi

# Create Notion page via Zapier MCP (requires icon emoji)
# Parent page: "Welcome to Notion" (accessible to Zapier MCP)
mcporter call zapier notion_create_page \
  "Create Notion page under 'Welcome to Notion' parent for property estimate: ${ADDRESS} - ${PROPERTY_TYPE}. Date: ${DATE}, Dimensions: ${DIMENSIONS}, Total Cost: \$${TOTAL_COST}. ${SUMMARY}" \
  --icon "🏠" \
  --title "${ADDRESS} - ${PROPERTY_TYPE} - \$${TOTAL_COST}"
