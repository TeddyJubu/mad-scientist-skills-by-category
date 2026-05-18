#!/usr/bin/env bash
# enhancor_status.sh — Check the status of an Enhancor video generation job
# Usage: ./enhancor_status.sh --request-id <request_id>

set -e

API_KEY="${ENHANCOR_API_KEY:-3778dcad6b8406f39e1ed08bdbab27930a5bdaace4e555b02617ff57224072c7}"
BASE_URL="https://apireq.enhancor.ai/api/enhancor-ugc-full-access/v1"

usage() {
  echo "Usage: $0 --request-id <request_id>"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --request-id) REQUEST_ID="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

[[ -z "$REQUEST_ID" ]] && usage

RESPONSE=$(curl -s -X POST "${BASE_URL}/status" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg request_id "$REQUEST_ID" '{request_id: $request_id}')")

# Handle both response shapes: requestId vs request_id
STATUS=$(echo "$RESPONSE" | jq -r '.status // empty')
RESULT=$(echo "$RESPONSE" | jq -r '.result // empty')
THUMBNAIL=$(echo "$RESPONSE" | jq -r '.thumbnail // empty')
ERROR=$(echo "$RESPONSE" | jq -r '.error // empty')

echo "Request ID: $REQUEST_ID"
echo "Status: $STATUS"

case "$STATUS" in
  PENDING|IN_QUEUE|IN_PROGRESS)
    echo "⏳ Job is still processing..."
    ;;
  COMPLETED)
    echo ""
    echo "✅ Complete!"
    [[ -n "$RESULT" && "$RESULT" != "null" ]] && echo "Video: $RESULT"
    [[ -n "$THUMBNAIL" && "$THUMBNAIL" != "null" ]] && echo "Thumbnail: $THUMBNAIL"
    ;;
  FAILED)
    echo ""
    echo "❌ Job failed."
    [[ -n "$ERROR" && "$ERROR" != "null" ]] && echo "Error: $ERROR"
    ;;
  *)
    # Check for auth errors
    AUTH_ERROR=$(echo "$RESPONSE" | jq -r '.error.message // empty')
    if [[ -n "$AUTH_ERROR" ]]; then
      echo "API Error: $AUTH_ERROR"
    else
      echo "Unexpected response:"
      echo "$RESPONSE" | jq .
    fi
    ;;
esac
