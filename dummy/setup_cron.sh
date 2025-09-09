#!/bin/bash
# Daily GitHub Contributor Cron Setup
# Run this script to set up automatic daily commits

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/daily_contributor.py"

# Add cron job (runs every day at 2 PM)
(crontab -l 2>/dev/null; echo "0 14 * * * cd $SCRIPT_DIR && python3 $PYTHON_SCRIPT") | crontab -

echo "✅ Daily contributor cron job added!"
echo "📅 Will run every day at 2:00 PM"
echo "🔍 To view cron jobs: crontab -l"
echo "🗑️  To remove cron job: crontab -e"
