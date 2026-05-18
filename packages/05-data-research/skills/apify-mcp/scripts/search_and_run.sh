#!/bin/bash
# Apify MCP Quick Runner: Search → Select → Run
# Usage: ./search_and_run.sh "search term" "input json" [max_results]

set -e

SEARCH_TERM="${1:?Missing search term}"
INPUT_JSON="${2:?Missing input JSON}"
MAX_RESULTS="${3:-100}"

echo "🔍 Searching for actors matching: $SEARCH_TERM"
ACTOR_ID=$(mcpc @apify tools-call search-actors keywords:="$SEARCH_TERM" limit:=5 --json \
  | jq -r '.content[0].text | fromjson | .items[0].name')

if [ -z "$ACTOR_ID" ] || [ "$ACTOR_ID" = "null" ]; then
  echo "❌ No actors found for: $SEARCH_TERM"
  exit 1
fi

echo "✅ Selected actor: $ACTOR_ID"
echo "📖 Fetching actor details..."

ACTOR_INFO=$(mcpc @apify tools-call fetch-actor-details actor:="$ACTOR_ID" --json \
  | jq -r '.content[0].text | fromjson')

echo "$ACTOR_INFO" | jq -r '.title, .description' | head -5
echo ""

echo "🚀 Running actor with input..."
RUN_RESULT=$(mcpc @apify tools-call call-actor \
  actor:="$ACTOR_ID" \
  input:="$INPUT_JSON" \
  --json)

echo "$RUN_RESULT" | jq '.'

DATASET_ID=$(echo "$RUN_RESULT" | jq -r '.content[0].text | fromjson | .defaultDatasetId')

if [ -z "$DATASET_ID" ] || [ "$DATASET_ID" = "null" ]; then
  echo "⚠️  No dataset returned (actor may have failed or produced no results)"
  exit 0
fi

echo ""
echo "📥 Fetching results (max $MAX_RESULTS items)..."
mcpc @apify tools-call get-actor-output \
  datasetId:="$DATASET_ID" \
  limit:="$MAX_RESULTS" \
  --json | jq '.content[0].text | fromjson'
