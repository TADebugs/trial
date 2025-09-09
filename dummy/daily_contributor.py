#!/usr/bin/env python3
"""
Daily GitHub Contributor Script

This script automatically makes commits to random repositories daily to maintain
consistent GitHub activity. It includes a smart scheduling algorithm that varies
commit patterns to look natural.

Usage:
    python daily_contributor.py [options]

Options:
    --dry-run           Show what would be done without making changes
    --force            Force commit even if already committed today
    --help             Show this help message

Scheduling Algorithm:
- 70% chance of committing on weekdays
- 30% chance of committing on weekends
- 15% chance of skipping a day (natural breaks)
- Varies commit times throughout the day
- Different commit patterns for different days
"""

import os
import sys
import random
import subprocess
import argparse
from datetime import datetime, timedelta
import json
import time

class DailyContributor:
    def __init__(self):
        self.contributions_file = "daily_contributions.json"
        self.repos_file = "repositories.json"
        
        # Professional commit messages by category
        self.commit_categories = {
            'documentation': [
                "Update README",
                "Add documentation",
                "Update comments",
                "Fix typos in docs",
                "Improve code comments",
                "Update API documentation"
            ],
            'bugfix': [
                "Fix minor bug",
                "Fix edge case",
                "Fix typo",
                "Fix formatting",
                "Fix linting issues",
                "Fix validation error"
            ],
            'feature': [
                "Add new feature",
                "Add validation",
                "Add error handling",
                "Add tests",
                "Add configuration",
                "Add utility function"
            ],
            'refactor': [
                "Refactor code",
                "Clean up code",
                "Optimize performance",
                "Improve code structure",
                "Simplify logic",
                "Update dependencies"
            ],
            'maintenance': [
                "Update dependencies",
                "Update config",
                "Update styles",
                "Improve UX",
                "Update error handling",
                "Maintenance update"
            ]
        }
        
        # Initialize repositories if not exists
        self.initialize_repositories()
    
    def initialize_repositories(self):
        """Initialize the repositories list if it doesn't exist"""
        if not os.path.exists(self.repos_file):
            # Default repositories - user should customize these
            default_repos = [
                {
                    "name": "learning-projects",
                    "path": "./learning-projects",
                    "description": "Personal learning projects",
                    "active": True
                },
                {
                    "name": "experiments",
                    "path": "./experiments", 
                    "description": "Code experiments and prototypes",
                    "active": True
                },
                {
                    "name": "utilities",
                    "path": "./utilities",
                    "description": "Utility scripts and tools",
                    "active": True
                }
            ]
            
            with open(self.repos_file, 'w') as f:
                json.dump(default_repos, f, indent=2)
            
            print(f"Created {self.repos_file} with default repositories.")
            print("Please edit this file to add your actual repository paths.")
    
    def load_repositories(self):
        """Load repositories from file"""
        try:
            with open(self.repos_file, 'r') as f:
                repos = json.load(f)
            return [repo for repo in repos if repo.get('active', True)]
        except:
            return []
    
    def get_commit_message(self, category=None):
        """Get a random commit message from a category"""
        if category is None:
            category = random.choice(list(self.commit_categories.keys()))
        
        messages = self.commit_categories.get(category, self.commit_categories['maintenance'])
        return random.choice(messages)
    
    def should_commit_today(self):
        """Scheduling algorithm to determine if we should commit today"""
        now = datetime.now()
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        
        # Check if we already committed today
        if not self.has_committed_today():
            # Weekday logic (Monday=0 to Friday=4)
            if day_of_week < 5:
                # 70% chance on weekdays
                return random.random() < 0.70
            else:
                # 30% chance on weekends
                return random.random() < 0.30
        
        return False
    
    def has_committed_today(self):
        """Check if we've already committed today"""
        try:
            with open(self.contributions_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime('%Y-%m-%d')
            return data.get('last_commit_date') == today
        except:
            return False
    
    def get_commit_time(self):
        """Get a random commit time based on day of week"""
        now = datetime.now()
        day_of_week = now.weekday()
        
        # Different time patterns for different days
        if day_of_week < 5:  # Weekdays
            # Work hours: 9 AM to 6 PM (with some evening work)
            hour = random.randint(9, 20)
        else:  # Weekends
            # More relaxed: 10 AM to 8 PM
            hour = random.randint(10, 20)
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return now.replace(hour=hour, minute=minute, second=second)
    
    def select_random_repo(self):
        """Select a random active repository"""
        repos = self.load_repositories()
        if not repos:
            return None
        
        return random.choice(repos)
    
    def create_commit_content(self, repo_name):
        """Create content for the commit"""
        content_types = [
            f"# {repo_name} Updates\n\n",
            f"## Daily Update - {datetime.now().strftime('%Y-%m-%d')}\n\n",
            f"### Changes\n\n",
            f"- Minor improvements\n",
            f"- Code optimization\n",
            f"- Documentation updates\n\n",
            f"*Auto-generated commit*\n"
        ]
        
        return ''.join(random.sample(content_types, random.randint(3, 6)))
    
    def setup_dummy_branch(self, dry_run=False):
        """Create or switch to dummy commits branch"""
        dummy_branch = "documentation"
        
        if dry_run:
            print(f"  Would create/switch to branch: {dummy_branch}")
            return
        
        try:
            # Check if dummy branch exists
            result = subprocess.run(['git', 'branch', '--list', dummy_branch], 
                                 capture_output=True, text=True, check=True)
            
            if dummy_branch in result.stdout:
                # Branch exists, switch to it
                subprocess.run(['git', 'checkout', dummy_branch], check=True)
                print(f"  ✅ Switched to existing branch: {dummy_branch}")
            else:
                # Create new branch from main/master
                try:
                    # Try to create from main first
                    subprocess.run(['git', 'checkout', '-b', dummy_branch, 'main'], check=True)
                    print(f"  ✅ Created new branch: {dummy_branch} from main")
                except subprocess.CalledProcessError:
                    try:
                        # Try to create from master
                        subprocess.run(['git', 'checkout', '-b', dummy_branch, 'master'], check=True)
                        print(f"  ✅ Created new branch: {dummy_branch} from master")
                    except subprocess.CalledProcessError:
                        # Create from current HEAD
                        subprocess.run(['git', 'checkout', '-b', dummy_branch], check=True)
                        print(f"  ✅ Created new branch: {dummy_branch} from current HEAD")
        
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Could not setup dummy branch: {e}")
            # Continue anyway, might work on current branch
    
    def make_commit(self, repo, dry_run=False):
        """Make a commit to the selected repository"""
        repo_path = repo['path']
        repo_name = repo['name']
        
        if not os.path.exists(repo_path):
            print(f"Repository path does not exist: {repo_path}")
            return False
        
        # Change to repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)
        
        try:
            # Check if it's a git repository
            if not os.path.exists('.git'):
                print(f"Not a git repository: {repo_path}")
                return False
            
            # Create or switch to dummy commits branch
            self.setup_dummy_branch(dry_run)
            
            # Create or update a file
            filename = f"daily_update_{datetime.now().strftime('%Y%m%d')}.md"
            content = self.create_commit_content(repo_name)
            
            if dry_run:
                print(f"  Would create/update: {filename}")
                print(f"  Repository: {repo_name}")
                print(f"  Message: {self.get_commit_message()}")
                return True
            
            # Write content to file
            with open(filename, 'w') as f:
                f.write(content)
            
            # Stage the file
            subprocess.run(['git', 'add', filename], check=True)
            
            # Create commit
            commit_message = self.get_commit_message()
            commit_time = self.get_commit_time()
            
            # Set git environment for commit time
            env = os.environ.copy()
            env['GIT_AUTHOR_DATE'] = commit_time.isoformat()
            env['GIT_COMMITTER_DATE'] = commit_time.isoformat()
            
            subprocess.run(['git', 'commit', '-m', commit_message], 
                         env=env, check=True)
            
            # Update tracking file
            self.update_commit_tracking(repo_name, commit_message)
            
            print(f"✅ Committed to {repo_name}: {commit_message}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error in {repo_name}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error in {repo_name}: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def update_commit_tracking(self, repo_name, message):
        """Update the commit tracking file"""
        try:
            with open(self.contributions_file, 'r') as f:
                data = json.load(f)
        except:
            data = {}
        
        today = datetime.now().strftime('%Y-%m-%d')
        data['last_commit_date'] = today
        data['last_repo'] = repo_name
        data['last_message'] = message
        
        if 'commits' not in data:
            data['commits'] = []
        
        data['commits'].append({
            'date': today,
            'repo': repo_name,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        with open(self.contributions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def run_daily_commit(self, dry_run=False, force=False):
        """Main function to run daily commit process"""
        print("🤖 Daily GitHub Contributor")
        print("=" * 40)
        
        # Check if we should commit today
        if not force and not self.should_commit_today():
            if self.has_committed_today():
                print("✅ Already committed today!")
            else:
                print("⏭️  Skipping today (scheduling algorithm)")
            return
        
        # Select random repository
        repo = self.select_random_repo()
        if not repo:
            print("❌ No active repositories found!")
            print(f"Please edit {self.repos_file} to add your repositories.")
            return
        
        print(f"📁 Selected repository: {repo['name']}")
        print(f"📝 Description: {repo.get('description', 'No description')}")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No actual commits will be made")
        
        # Make the commit
        success = self.make_commit(repo, dry_run)
        
        if success and not dry_run:
            print("🎉 Daily commit completed successfully!")
        elif dry_run:
            print("🔍 Dry run completed - no changes made")
        else:
            print("❌ Daily commit failed!")
    
    def show_scheduling_algorithm(self):
        """Show the scheduling algorithm details"""
        print("📊 Daily Commit Scheduling Algorithm")
        print("=" * 50)
        print()
        print("🎯 Probability Rules:")
        print("  • Weekdays (Mon-Fri): 70% chance of commit")
        print("  • Weekends (Sat-Sun): 30% chance of commit")
        print("  • Skip if already committed today")
        print()
        print("⏰ Time Patterns:")
        print("  • Weekdays: 9 AM - 8 PM (work hours)")
        print("  • Weekends: 10 AM - 8 PM (relaxed)")
        print()
        print("📝 Commit Categories:")
        for category, messages in self.commit_categories.items():
            print(f"  • {category.title()}: {len(messages)} message types")
        print()
        print("🔄 Natural Variation:")
        print("  • Random repository selection")
        print("  • Random commit messages")
        print("  • Random commit times")
        print("  • Different content each day")

def main():
    parser = argparse.ArgumentParser(description='Daily GitHub Contributor Script')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--force', action='store_true',
                       help='Force commit even if already committed today')
    parser.add_argument('--show-algorithm', action='store_true',
                       help='Show the scheduling algorithm details')
    
    args = parser.parse_args()
    
    contributor = DailyContributor()
    
    if args.show_algorithm:
        contributor.show_scheduling_algorithm()
    else:
        contributor.run_daily_commit(dry_run=args.dry_run, force=args.force)

if __name__ == "__main__":
    main()
