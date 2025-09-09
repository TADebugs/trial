#!/usr/bin/env python3
"""
GitHub Contribution Graph Filler Script

This script creates dummy commits to fill your GitHub contribution graph.
It's designed to be safe and won't overwrite your actual work.

Usage:
    python git_contributor.py [options]

Options:
    --days-back N        Number of days back to fill (default: 365)
    --commits-per-day N  Average commits per day (default: 3)
    --min-commits N      Minimum commits per day (default: 0)
    --max-commits N      Maximum commits per day (default: 8)
    --dry-run           Show what would be done without making changes
    --help              Show this help message

Safety Features:
- Only modifies a dedicated 'contributions' file
- Never touches your actual code files
- Creates commits with timestamps in the past
- Can be easily undone by deleting the contributions file
"""

import os
import sys
import random
import subprocess
import argparse
from datetime import datetime, timedelta
import json

class GitContributor:
    def __init__(self, days_back=365, commits_per_day=3, min_commits=0, max_commits=8):
        self.days_back = days_back
        self.commits_per_day = commits_per_day
        self.min_commits = min_commits
        self.max_commits = max_commits
        self.contributions_file = "contributions.json"
        
        # Safe commit messages that look professional
        self.commit_messages = [
            "Update documentation",
            "Fix minor bug",
            "Refactor code",
            "Add feature",
            "Improve performance",
            "Update dependencies",
            "Fix typo",
            "Optimize code",
            "Add tests",
            "Update README",
            "Fix formatting",
            "Add comments",
            "Update config",
            "Clean up code",
            "Fix linting issues",
            "Update styles",
            "Add validation",
            "Fix edge case",
            "Update error handling",
            "Improve UX"
        ]
    
    def run_command(self, command, check=True):
        """Run a git command and return the result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
            print(f"Error: {e.stderr}")
            return None
    
    def is_git_repo(self):
        """Check if current directory is a git repository"""
        return os.path.exists('.git')
    
    def get_existing_contributions(self):
        """Load existing contributions from file"""
        if os.path.exists(self.contributions_file):
            try:
                with open(self.contributions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_contributions(self, contributions):
        """Save contributions to file"""
        with open(self.contributions_file, 'w') as f:
            json.dump(contributions, f, indent=2)
    
    def generate_commit_data(self, date):
        """Generate random commit data for a given date"""
        # About 5 empty days per month (roughly 16% chance) for more natural look
        if random.random() < 0.16:
            return []
        
        # If we get here, we're not having an empty day
        # But we still need to respect min_commits - if min_commits is 0, we could still have 0
        if self.min_commits == 0 and random.random() < 0.1:  # 10% chance of 0 even when not "empty day"
            return []
        
        num_commits = random.randint(max(1, self.min_commits), self.max_commits)
        commits = []
        
        for _ in range(num_commits):
            # Generate random time within the day
            hour = random.randint(9, 22)  # Work hours
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_time = date.replace(hour=hour, minute=minute, second=second)
            message = random.choice(self.commit_messages)
            
            commits.append({
                'timestamp': commit_time.isoformat(),
                'message': message
            })
        
        return commits
    
    def create_commit(self, commit_data, dry_run=False):
        """Create a single commit with the given data"""
        if dry_run:
            print(f"  Would create commit: {commit_data['message']} at {commit_data['timestamp']}")
            return True
        
        # Set the git author date and commit date to the past
        timestamp = commit_data['timestamp']
        
        # Add a small change to the contributions file
        contributions = self.get_existing_contributions()
        contributions[timestamp] = commit_data['message']
        self.save_contributions(contributions)
        
        # Stage the file
        self.run_command(f"git add {self.contributions_file}")
        
        # Create the commit with the past timestamp
        commit_cmd = f'git commit -m "{commit_data["message"]}" --date="{timestamp}"'
        result = self.run_command(commit_cmd, check=False)
        
        if result is None:
            print(f"  Failed to create commit: {commit_data['message']}")
            return False
        
        return True
    
    def fill_contributions(self, dry_run=False):
        """Fill the contribution graph for the specified period"""
        if not self.is_git_repo():
            print("Error: Not in a git repository. Please run this script from a git repo.")
            return False
        
        print(f"Filling contributions for the last {self.days_back} days...")
        print(f"Target: {self.commits_per_day} commits per day (range: {self.min_commits}-{self.max_commits})")
        
        if dry_run:
            print("DRY RUN MODE - No actual commits will be created")
        
        print()
        
        total_commits = 0
        start_date = datetime.now() - timedelta(days=self.days_back)
        
        for i in range(self.days_back):
            current_date = start_date + timedelta(days=i)
            
            # Skip weekends occasionally (70% chance to skip)
            if current_date.weekday() >= 5 and random.random() < 0.7:
                continue
            
            commits = self.generate_commit_data(current_date)
            
            if commits:
                print(f"Date: {current_date.strftime('%Y-%m-%d')} - {len(commits)} commits")
                
                for commit in commits:
                    if self.create_commit(commit, dry_run):
                        total_commits += 1
                
                print()
            else:
                # Show empty days for transparency (both dry-run and actual)
                print(f"Date: {current_date.strftime('%Y-%m-%d')} - 0 commits (empty day)")
        
        print(f"Total commits {'would be ' if dry_run else ''}created: {total_commits}")
        
        if not dry_run:
            print(f"\nContributions file created: {self.contributions_file}")
            print("You can now push these commits to GitHub:")
            print("  git push origin main")
            print("\nTo undo these changes:")
            print(f"  git reset --hard HEAD~{total_commits}")
            print(f"  rm {self.contributions_file}")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Fill GitHub contribution graph with dummy commits')
    parser.add_argument('--days-back', type=int, default=365, 
                       help='Number of days back to fill (default: 365)')
    parser.add_argument('--commits-per-day', type=int, default=3,
                       help='Average commits per day (default: 3)')
    parser.add_argument('--min-commits', type=int, default=0,
                       help='Minimum commits per day (default: 0)')
    parser.add_argument('--max-commits', type=int, default=8,
                       help='Maximum commits per day (default: 8)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.min_commits > args.max_commits:
        print("Error: min-commits cannot be greater than max-commits")
        sys.exit(1)
    
    if args.commits_per_day < args.min_commits or args.commits_per_day > args.max_commits:
        print("Warning: commits-per-day is outside the min-max range, adjusting...")
        args.commits_per_day = max(args.min_commits, min(args.commits_per_day, args.max_commits))
    
    contributor = GitContributor(
        days_back=args.days_back,
        commits_per_day=args.commits_per_day,
        min_commits=args.min_commits,
        max_commits=args.max_commits
    )
    
    contributor.fill_contributions(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
