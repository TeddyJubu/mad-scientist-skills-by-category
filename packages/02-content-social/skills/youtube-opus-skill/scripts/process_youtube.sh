#!/bin/bash
# Process YouTube via OpusClip MCP
source "$(dirname "$0")/config.sh"
YOUTUBE_URL="${1:-$YOUTUBE_URL}"
[ -z "$YOUTUBE_URL" ] && { echo "Error: No YouTube URL"; exit 1; }
echo "Processing: $YOUTUBE_URL"
echo "MCP: $MCP_OPUS_URL"
echo "Status: Ready for MCP tool invocation"
