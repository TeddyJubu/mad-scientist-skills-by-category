#!/bin/bash
# Run Apify actor and export results to CSV
# Usage: ./run_and_export_csv.sh "actor_id" "input_json" "output.csv" [max_items]

set -e

ACTOR_ID="${1:?Missing actor ID (format: username/actor-name)}"
INPUT_JSON="${2:?Missing input JSON}"
OUTPUT_FILE="${3:?Missing output file path}"
MAX_ITEMS="${4:-100}"

echo "🚀 Running actor: $ACTOR_ID"
echo "📥 Input: $INPUT_JSON"
echo ""

# Run actor and capture result
RUN_RESULT=$(mcpc @apify tools-call call-actor \
  actor:="$ACTOR_ID" \
  input:="$INPUT_JSON" \
  --json)

# Extract dataset ID
DATASET_ID=$(echo "$RUN_RESULT" | jq -r '.content[0].text | fromjson | .defaultDatasetId')

if [ -z "$DATASET_ID" ] || [ "$DATASET_ID" = "null" ]; then
  echo "❌ Actor run failed or produced no dataset"
  echo "$RUN_RESULT" | jq '.'
  exit 1
fi

echo "✅ Actor completed. Dataset ID: $DATASET_ID"
echo "📥 Fetching up to $MAX_ITEMS items..."

# Fetch items as JSON
ITEMS=$(mcpc @apify tools-call get-actor-output \
  datasetId:="$DATASET_ID" \
  limit:="$MAX_ITEMS" \
  --json | jq -r '.content[0].text | fromjson | .items')

if [ -z "$ITEMS" ] || [ "$ITEMS" = "null" ] || [ "$ITEMS" = "[]" ]; then
  echo "⚠️  No items returned from dataset"
  exit 0
fi

# Convert to CSV using jq
echo "$ITEMS" | jq -r '
  (.[0] | keys_unsorted) as $keys |
  $keys,
  (.[] | [.[$keys[]]] | @csv)
' > "$OUTPUT_FILE"

ROW_COUNT=$(tail -n +2 "$OUTPUT_FILE" | wc -l | tr -d ' ')

echo "✅ Saved $ROW_COUNT rows to: $OUTPUT_FILE"
echo ""
echo "Preview (first 5 rows):"
head -6 "$OUTPUT_FILE" | column -t -s ','
