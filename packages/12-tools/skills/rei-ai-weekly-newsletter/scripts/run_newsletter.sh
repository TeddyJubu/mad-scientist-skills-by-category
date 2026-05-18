#!/bin/bash
#
# run_newsletter.sh - Run the full REI AI Weekly newsletter workflow
#
# Usage:
#   ./run_newsletter.sh [target_chat_id]
#
# If target_chat_id is omitted, sends to the current Telegram chat.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/rei-ai-newsletter-$(date +%s)"

mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "🔍 [1/4] Aggregating content from web sources..."
python3 "$SCRIPT_DIR/aggregate_content.py" --output content.json

echo "📄 [2/4] Generating PDF newsletter..."
python3 "$SCRIPT_DIR/generate_pdf.py" --input content.json --output newsletter.pdf

echo "📤 [3/4] Sending to Telegram..."
if [ -n "$1" ]; then
    python3 "$SCRIPT_DIR/send_telegram.py" --pdf newsletter.pdf --target "$1"
else
    python3 "$SCRIPT_DIR/send_telegram.py" --pdf newsletter.pdf
fi

echo "✅ [4/4] Newsletter delivered!"

# Optional: archive the newsletter
ARCHIVE_DIR="$HOME/.openclaw/workspace/newsletters"
mkdir -p "$ARCHIVE_DIR"
cp newsletter.pdf "$ARCHIVE_DIR/rei-ai-weekly-$(date +%Y-%m-%d).pdf"
echo "📁 Archived to: $ARCHIVE_DIR/rei-ai-weekly-$(date +%Y-%m-%d).pdf"

# Cleanup
cd /
rm -rf "$WORK_DIR"
