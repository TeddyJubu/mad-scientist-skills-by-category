#!/bin/bash
#
# setup_cron.sh - Install cron job for weekly newsletter delivery
#
# Usage:
#   ./setup_cron.sh [target_chat_id]
#
# Installs a cron job that runs every Monday at 9:00 AM ET

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_SCRIPT="$SCRIPT_DIR/run_newsletter.sh"

TARGET_ARG=""
if [ -n "$1" ]; then
    TARGET_ARG=" $1"
fi

# Cron entry (every Monday at 9:00 AM)
CRON_ENTRY="0 9 * * 1 $CRON_SCRIPT$TARGET_ARG >> /tmp/rei-ai-newsletter.log 2>&1"

# Check if cron entry already exists
if crontab -l 2>/dev/null | grep -q "run_newsletter.sh"; then
    echo "❌ Cron job already exists. Remove it first with:"
    echo "   crontab -e"
    exit 1
fi

# Add cron entry
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job installed successfully!"
echo "📅 Newsletter will be sent every Monday at 9:00 AM ET"
echo ""
echo "To view your cron jobs:"
echo "   crontab -l"
echo ""
echo "To edit or remove:"
echo "   crontab -e"
echo ""
echo "Logs will be written to: /tmp/rei-ai-newsletter.log"
