#!/bin/bash
# macOS LaunchAgent Setup for Daily GitHub Contributor
# This creates a LaunchAgent that runs the script daily

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_NAME="com.github.contributor.daily"
PLIST_FILE="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

echo "🚀 Setting up macOS LaunchAgent for Daily GitHub Contributor"
echo "=========================================================="

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Create the plist file
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>${SCRIPT_DIR}/daily_contributor.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${SCRIPT_DIR}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>14</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${SCRIPT_DIR}/daily_contributor.log</string>
    <key>StandardErrorPath</key>
    <string>${SCRIPT_DIR}/daily_contributor_error.log</string>
</dict>
</plist>
EOF

echo "✅ Created LaunchAgent plist: $PLIST_FILE"

# Load the LaunchAgent
launchctl load "$PLIST_FILE"
echo "✅ Loaded LaunchAgent"

echo ""
echo "🎉 LaunchAgent setup complete!"
echo ""
echo "📋 What happens now:"
echo "  • Script will run daily at 2:00 PM"
echo "  • Logs will be saved to daily_contributor.log"
echo "  • Errors will be saved to daily_contributor_error.log"
echo ""
echo "🔧 Management commands:"
echo "  • Check status: launchctl list | grep ${PLIST_NAME}"
echo "  • Unload: launchctl unload $PLIST_FILE"
echo "  • Reload: launchctl load $PLIST_FILE"
echo "  • View logs: tail -f ${SCRIPT_DIR}/daily_contributor.log"
