#!/bin/bash
# OpusClip MCP - Clip a YouTube video
# Usage: ./clip_video.sh <youtube_url>

set -e

YOUTUBE_URL="$1"
MCP_TOKEN="ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9"
MCP_ENDPOINT="https://mcp.zapier.com/api/v1/connect"

if [ -z "$YOUTUBE_URL" ]; then
    echo "Error: YouTube URL required"
    echo "Usage: $0 <youtube_url>"
    exit 1
fi

# Call the MCP endpoint to clip the video
RESPONSE=$(curl -s -N -X POST "$MCP_ENDPOINT" \
    -H "Authorization: Bearer $MCP_TOKEN" \
    -H "Accept: application/json, text/event-stream" \
    -H "Content-Type: application/json" \
    -d "{
        \"jsonrpc\": \"2.0\",
        \"method\": \"tools/call\",
        \"params\": {
            \"name\": \"opusclip_clip_your_video\",
            \"arguments\": {
                \"instructions\": \"Create clipped segments from this YouTube video\",
                \"videoUrl\": \"$YOUTUBE_URL\",
                \"output_hint\": \"return the project ID, status, and any available clip URLs\"
            }
        },
        \"id\": $(date +%s)
    }" 2>&1)

# Extract the data event and parse JSON
DATA_LINE=$(echo "$RESPONSE" | grep "^data:")
JSON_DATA=$(echo "$DATA_LINE" | sed 's/^data: //')

# Parse the response
echo "$JSON_DATA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'result' in data:
    result = data['result']
    if 'content' in result:
        for item in result['content']:
            if item.get('type') == 'text':
                text_data = json.loads(item['text'])
                print(json.dumps(text_data, indent=2))
    else:
        print(json.dumps(result, indent=2))
elif 'error' in data:
    print(f\"Error: {data['error']}\")
else:
    print(json.dumps(data, indent=2))
"
