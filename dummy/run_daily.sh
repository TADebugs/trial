#!/bin/bash
# Manual Daily Contributor Runner
# Run this script to manually trigger daily commits

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 Running Daily GitHub Contributor..."
python3 daily_contributor.py

echo "✅ Manual run completed!"
