#!/bin/bash
# Poll for Opus Clip completion and post to Blotato
# Usage: ./poll_and_post.sh <project_id>

set -e

PROJECT_ID="$1"
MCP_TOKEN="ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9"
MCP_ENDPOINT="https://mcp.zapier.com/api/v1/connect"
MAX_ATTEMPTS=50
INTERVAL=30

if [ -z "$PROJECT_ID" ]; then
    echo "Error: Project ID required"
    echo "Usage: $0 <project_id>"
    exit 1
fi

echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Starting polling for project $PROJECT_ID"

for attempt in $(seq 1 $MAX_ATTEMPTS); do
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Attempt $attempt/$MAX_ATTEMPTS"
    
    # Get clips transcript (most reliable method)
    RESPONSE=$(curl -s -N -X POST "$MCP_ENDPOINT" \
        -H "Authorization: Bearer $MCP_TOKEN" \
        -H "Accept: application/json, text/event-stream" \
        -H "Content-Type: application/json" \
        -d "{
            \"jsonrpc\": \"2.0\",
            \"method\": \"tools/call\",
            \"params\": {
                \"name\": \"opusclip_get_transcript_of_clips\",
                \"arguments\": {
                    \"projectId\": \"$PROJECT_ID\"
                }
            },
            \"id\": $(date +%s)
        }" 2>&1)
    
    # Extract and parse response
    DATA_LINE=$(echo "$RESPONSE" | grep "^data:" || true)
    
    if [ -n "$DATA_LINE" ]; then
        JSON_DATA=$(echo "$DATA_LINE" | sed 's/^data: //')
        
        # Check if we have clips
        CLIPS_DATA=$(echo "$JSON_DATA" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'result' in data and 'content' in data['result']:
        for item in data['result']['content']:
            if item.get('type') == 'text':
                text_data = json.loads(item['text'])
                if 'results' in text_data:
                    clips = text_data['results'].get('clips', [])
                    if clips and len(clips) > 0:
                        print(json.dumps(clips))
                        sys.exit(0)
except:
    pass
print('[]')
" || echo "[]")
        
        if [ "$CLIPS_DATA" != "[]" ]; then
            echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] ✓ Clips found!"
            echo "$CLIPS_DATA" > /tmp/opus_clips_${PROJECT_ID}.json
            
            # Now call the Python script to handle Blotato posting
            echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Processing clips and posting to Blotato..."
            python3.11 "$(dirname "$0")/post_to_blotato.py" "$PROJECT_ID" "$CLIPS_DATA"
            exit 0
        fi
    fi
    
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] No clips ready yet. Waiting ${INTERVAL}s..."
    sleep $INTERVAL
done

echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Max attempts reached. No clips found."
exit 1
