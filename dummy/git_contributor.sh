#!/bin/bash

# GitHub Contribution Graph Filler Script (Shell Version)
# This script creates dummy commits to fill your GitHub contribution graph

# Default values
DAYS_BACK=365
COMMITS_PER_DAY=3
MIN_COMMITS=0
MAX_COMMITS=8
DRY_RUN=false
CONTRIBUTIONS_FILE="contributions.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Help function
show_help() {
    echo "GitHub Contribution Graph Filler Script"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --days-back N        Number of days back to fill (default: 365)"
    echo "  --commits-per-day N  Average commits per day (default: 3)"
    echo "  --min-commits N      Minimum commits per day (default: 0)"
    echo "  --max-commits N      Maximum commits per day (default: 8)"
    echo "  --dry-run           Show what would be done without making changes"
    echo "  --help              Show this help message"
    echo ""
    echo "Safety Features:"
    echo "- Only modifies a dedicated '$CONTRIBUTIONS_FILE' file"
    echo "- Never touches your actual code files"
    echo "- Creates commits with timestamps in the past"
    echo "- Can be easily undone by deleting the contributions file"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --days-back)
            DAYS_BACK="$2"
            shift 2
            ;;
        --commits-per-day)
            COMMITS_PER_DAY="$2"
            shift 2
            ;;
        --min-commits)
            MIN_COMMITS="$2"
            shift 2
            ;;
        --max-commits)
            MAX_COMMITS="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate arguments
if [ "$MIN_COMMITS" -gt "$MAX_COMMITS" ]; then
    echo -e "${RED}Error: min-commits cannot be greater than max-commits${NC}"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not in a git repository. Please run this script from a git repo.${NC}"
    exit 1
fi

# Array of professional commit messages
commit_messages=(
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

# Function to get random commit message
get_random_message() {
    local index=$((RANDOM % ${#commit_messages[@]}))
    echo "${commit_messages[$index]}"
}

# Function to generate random number of commits for a day
get_commits_for_day() {
    local min=$1
    local max=$2
    
    # About 5 empty days per month (roughly 16% chance) for more natural look
    if [ $((RANDOM % 100)) -lt 16 ]; then
        echo 0
    else
        # If we get here, we're not having an empty day
        # But we still need to respect min_commits - if min_commits is 0, we could still have 0
        if [ "$min" -eq 0 ] && [ $((RANDOM % 100)) -lt 10 ]; then  # 10% chance of 0 even when not "empty day"
            echo 0
        else
            # Ensure we don't go below min_commits when min > 0
            local actual_min=$min
            if [ "$min" -eq 0 ]; then
                actual_min=1
            fi
            echo $((RANDOM % (max - actual_min + 1) + actual_min))
        fi
    fi
}

# Function to create a commit
create_commit() {
    local message="$1"
    local timestamp="$2"
    local dry_run="$3"
    
    if [ "$dry_run" = true ]; then
        echo -e "  ${YELLOW}Would create commit: $message at $timestamp${NC}"
        return 0
    fi
    
    # Add content to contributions file
    echo "$timestamp: $message" >> "$CONTRIBUTIONS_FILE"
    
    # Stage the file
    git add "$CONTRIBUTIONS_FILE" > /dev/null 2>&1
    
    # Create commit with past timestamp
    GIT_AUTHOR_DATE="$timestamp" GIT_COMMITTER_DATE="$timestamp" \
        git commit -m "$message" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}Created commit: $message${NC}"
        return 0
    else
        echo -e "  ${RED}Failed to create commit: $message${NC}"
        return 1
    fi
}

# Main execution
echo -e "${BLUE}GitHub Contribution Graph Filler${NC}"
echo "=================================="
echo "Filling contributions for the last $DAYS_BACK days..."
echo "Target: $COMMITS_PER_DAY commits per day (range: $MIN_COMMITS-$MAX_COMMITS)"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}DRY RUN MODE - No actual commits will be created${NC}"
fi

echo ""

total_commits=0
# Calculate start date (macOS compatible)
start_timestamp=$(($(date +%s) - (DAYS_BACK * 86400)))
current_date=$(date -r $start_timestamp +%Y-%m-%d)

for ((i=0; i<DAYS_BACK; i++)); do
    # Calculate current date (macOS compatible)
    current_timestamp=$((start_timestamp + (i * 86400)))
    current_date=$(date -r $current_timestamp +%Y-%m-%d)
    day_of_week=$(date -r $current_timestamp +%u)
    
    # Skip weekends occasionally (70% chance to skip)
    if [ "$day_of_week" -ge 6 ] && [ $((RANDOM % 10)) -lt 7 ]; then
        continue
    fi
    
    # Get number of commits for this day
    num_commits=$(get_commits_for_day $MIN_COMMITS $MAX_COMMITS)
    
    if [ "$num_commits" -gt 0 ]; then
        echo -e "${BLUE}Date: $current_date - $num_commits commits${NC}"
        
        for ((j=0; j<num_commits; j++)); do
            # Generate random time within work hours (9 AM to 10 PM)
            hour=$((9 + RANDOM % 14))
            minute=$((RANDOM % 60))
            second=$((RANDOM % 60))
            
            timestamp="${current_date} ${hour}:${minute}:${second}"
            message=$(get_random_message)
            
            if create_commit "$message" "$timestamp" "$DRY_RUN"; then
                total_commits=$((total_commits + 1))
            fi
        done
        echo ""
    else
        # Show empty days for transparency
        if [ "$DRY_RUN" = true ]; then
            echo -e "${YELLOW}Date: $current_date - 0 commits (empty day)${NC}"
        fi
    fi
done

echo -e "${GREEN}Total commits ${DRY_RUN:+would be }created: $total_commits${NC}"

if [ "$DRY_RUN" = false ]; then
    echo ""
    echo -e "${BLUE}Contributions file created: $CONTRIBUTIONS_FILE${NC}"
    echo "You can now push these commits to GitHub:"
    echo "  git push origin main"
    echo ""
    echo "To undo these changes:"
    echo "  git reset --hard HEAD~$total_commits"
    echo "  rm $CONTRIBUTIONS_FILE"
fi
