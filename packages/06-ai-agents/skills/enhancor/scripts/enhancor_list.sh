#!/usr/bin/env bash
# enhancor_list.sh — List all video generations from Enhancor API
# Usage: ./enhancor_list.sh

set -e

API_KEY="${ENHANCOR_API_KEY:-3778dcad6b8406f39e1ed08bdbab27930a5bdaace4e555b02617ff57224072c7}"
BASE_URL="https://apireq.enhancor.ai/api/enhancor-ugc-full-access/v1"

echo "Fetching all generations..."

RESPONSE=$(curl -s -X GET "${BASE_URL}/b2b-generations" \
  -H "x-api-key: ${API_KEY}")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success // empty')
GENERATIONS=$(echo "$RESPONSE" | jq '.generations // []')

if [[ "$SUCCESS" == "true" ]]; then
  COUNT=$(echo "$GENERATIONS" | jq 'length')
  echo "Found $COUNT generation(s):"
  echo ""
  echo "$GENERATIONS" | jq -r '.[] | "  [\(.status)] \(.requestId)\n    Result: \(.result // "—")\n    Thumbnail: \(.thumbnail // "—")\n"' 2>/dev/null || echo "$GENERATIONS" | jq .
else
  echo "❌ Failed to fetch generations:"
  echo "$RESPONSE" | jq .
  exit 1
fi
