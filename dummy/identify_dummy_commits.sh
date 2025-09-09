#!/bin/bash

# Identify Dummy Commits Script
# This script helps you identify and filter dummy commits

echo "🔍 Identifying Dummy Commits"
echo "============================"
echo

# Count total commits
total_commits=$(git rev-list --count HEAD)
echo "📊 Total commits: $total_commits"
echo

# Count dummy commits by message pattern
echo "🤖 Dummy commits by message pattern:"
dummy_count=0

# Check each dummy pattern
patterns=(
    "Update documentation"
    "Fix minor bug"
    "Refactor code"
    "Add feature"
    "Improve performance"
    "Update dependencies"
    "Fix typo"
    "Optimize code"
    "Add tests"
    "Update README"
    "Fix formatting"
    "Add comments"
    "Update config"
    "Clean up code"
    "Fix linting issues"
    "Update styles"
    "Add validation"
    "Fix edge case"
    "Update error handling"
    "Improve UX"
)

for pattern in "${patterns[@]}"; do
    count=$(git log --grep="$pattern" --oneline | wc -l)
    if [ $count -gt 0 ]; then
        echo "  • $pattern: $count commits"
        dummy_count=$((dummy_count + count))
    fi
done

echo
echo "📈 Total dummy commits (by message): $dummy_count"

# Count commits touching dummy files
echo
echo "📁 Commits touching dummy files:"
dummy_file_count=$(git log --name-only --pretty=format: | grep -E "(daily_update_|contributions)" | wc -l)
echo "  • Files with 'daily_update_' or 'contributions': $dummy_file_count"

# Show recent dummy commits
echo
echo "🕒 Recent dummy commits (last 10):"
git log --grep="Update documentation\|Fix minor bug\|Refactor code\|Add feature\|Improve performance\|Update dependencies\|Fix typo\|Optimize code\|Add tests\|Update README\|Fix formatting\|Add comments\|Update config\|Clean up code\|Fix linting issues\|Update styles\|Add validation\|Fix edge case\|Update error handling\|Improve UX" --oneline -10

echo
echo "🔧 Useful commands to filter out dummy commits:"
echo "=============================================="
echo
echo "1. Show only real commits:"
echo "   git log --grep='Update documentation' --invert-grep --grep='Fix minor bug' --invert-grep"
echo
echo "2. Show commits excluding dummy files:"
echo "   git log -- . ':!daily_update_*.md' ':!contributions*.json'"
echo
echo "3. Create a clean branch:"
echo "   git checkout -b clean-history"
echo "   git reset --hard <first-real-commit-hash>"
echo
echo "4. View clean history:"
echo "   git log --oneline --grep='Update documentation' --invert-grep"
