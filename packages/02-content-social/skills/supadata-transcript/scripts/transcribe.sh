#!/bin/bash
# Supadata Transcript Script
# Fetch transcripts from YouTube, TikTok, Twitter, Instagram, Facebook, or file URLs

set -e

# Load API key from secrets
SECRETS_FILE="${HOME}/.openclaw/workspace/.secrets/supadata.env"
if [ -f "$SECRETS_FILE" ]; then
  source "$SECRETS_FILE"
fi

if [ -z "$SUPADATA_API_KEY" ]; then
  echo "❌ Error: SUPADATA_API_KEY not set. Add it to $SECRETS_FILE" >&2
  exit 1
fi

# Parse arguments
URL=""
LANG=""
TEXT_MODE=""
MODE="auto"
CHUNK_SIZE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --lang)
      LANG="$2"
      shift 2
      ;;
    --text)
      TEXT_MODE="true"
      shift
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    --chunk-size)
      CHUNK_SIZE="$2"
      shift 2
      ;;
    *)
      if [ -z "$URL" ]; then
        URL="$1"
      fi
      shift
      ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Usage: $0 <video_url> [--lang <code>] [--text] [--mode native|auto|generate] [--chunk-size <num>]"
  exit 1
fi

# Build query string
QUERY="url=$(printf '%s' "$URL" | jq -sRr @uri)"
[ -n "$LANG" ] && QUERY="$QUERY&lang=$LANG"
[ -n "$TEXT_MODE" ] && QUERY="$QUERY&text=$TEXT_MODE"
[ -n "$MODE" ] && QUERY="$QUERY&mode=$MODE"
[ -n "$CHUNK_SIZE" ] && QUERY="$QUERY&chunkSize=$CHUNK_SIZE"

API_URL="https://api.supadata.ai/v1/transcript?$QUERY"

echo "🔄 Fetching transcript from: $URL" >&2
echo "   Mode: $MODE" >&2
[ -n "$LANG" ] && echo "   Language: $LANG" >&2

# Make API request
RESPONSE=$(curl -sS -w "\n%{http_code}" -X GET "$API_URL" \
  -H "x-api-key: $SUPADATA_API_KEY" \
  -H "Content-Type: application/json")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE" != "202" ]; then
  echo "❌ API Error (HTTP $HTTP_CODE):" >&2
  echo "$BODY" | jq -r '.message // .error // .' >&2
  exit 1
fi

# Check if response is a job ID (async processing)
JOB_ID=$(echo "$BODY" | jq -r '.jobId // empty')

if [ -n "$JOB_ID" ]; then
  echo "⏳ Large video detected. Job ID: $JOB_ID" >&2
  echo "   Polling for completion..." >&2
  
  # Poll for job completion
  MAX_ATTEMPTS=60
  ATTEMPT=0
  WAIT_TIME=5
  
  while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    sleep $WAIT_TIME
    ATTEMPT=$((ATTEMPT + 1))
    
    JOB_RESPONSE=$(curl -sS -w "\n%{http_code}" -X GET \
      "https://api.supadata.ai/v1/transcript/$JOB_ID" \
      -H "x-api-key: $SUPADATA_API_KEY" \
      -H "Content-Type: application/json")
    
    JOB_HTTP_CODE=$(echo "$JOB_RESPONSE" | tail -n1)
    JOB_BODY=$(echo "$JOB_RESPONSE" | sed '$d')
    
    if [ "$JOB_HTTP_CODE" = "200" ]; then
      # Job completed
      JOB_STATUS=$(echo "$JOB_BODY" | jq -r '.status // empty')
      
      if [ "$JOB_STATUS" = "completed" ]; then
        echo "✅ Transcript ready!" >&2
        echo "$JOB_BODY" | jq -r '.content'
        exit 0
      elif [ "$JOB_STATUS" = "failed" ]; then
        echo "❌ Job failed:" >&2
        echo "$JOB_BODY" | jq -r '.message // .error // .' >&2
        exit 1
      fi
    fi
    
    echo "   Still processing... (attempt $ATTEMPT/$MAX_ATTEMPTS)" >&2
    
    # Exponential backoff
    WAIT_TIME=$((WAIT_TIME + 2))
  done
  
  echo "❌ Timeout: Job did not complete in time" >&2
  exit 1
fi

# Immediate response (small video)
echo "✅ Transcript fetched successfully!" >&2
echo "$BODY"
