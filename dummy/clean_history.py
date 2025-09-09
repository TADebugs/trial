#!/usr/bin/env python3
"""
Git History Cleaner

This script helps you filter out dummy commits from your git history
and provides various ways to view clean commit history.

Usage:
    python clean_history.py [options]

Options:
    --show-real          Show only real commits (exclude dummy)
    --show-dummy         Show only dummy commits
    --count              Count commits by type
    --clean-branch       Create a clean branch without dummy commits
    --help               Show this help message
"""

import os
import sys
import subprocess
import argparse
import re
from datetime import datetime

class GitHistoryCleaner:
    def __init__(self):
        self.dummy_patterns = [
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
        
        self.dummy_files = [
            "daily_update_",
            "contributions",
            "contributions_historical"
        ]
    
    def run_git_command(self, command):
        """Run a git command and return the result"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {command}")
            print(f"Error: {e.stderr}")
            return None
    
    def is_dummy_commit(self, commit_message):
        """Check if a commit message matches dummy patterns"""
        return any(pattern in commit_message for pattern in self.dummy_patterns)
    
    def is_dummy_file_commit(self, commit_hash):
        """Check if a commit touches dummy files"""
        files = self.run_git_command(f"git show --name-only --pretty=format: {commit_hash}")
        if files:
            return any(any(dummy_file in file for dummy_file in self.dummy_files) for file in files.split('\n'))
        return False
    
    def get_commit_history(self, limit=None):
        """Get commit history with details"""
        limit_cmd = f" --max-count={limit}" if limit else ""
        command = f"git log --pretty=format:'%H|%an|%ad|%s' --date=short{limit_cmd}"
        result = self.run_git_command(command)
        
        if not result:
            return []
        
        commits = []
        for line in result.split('\n'):
            if '|' in line:
                parts = line.split('|', 3)
                if len(parts) == 4:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'date': parts[2],
                        'message': parts[3]
                    })
        
        return commits
    
    def show_real_commits(self, limit=None):
        """Show only real commits (exclude dummy)"""
        print("🔍 Real Commits (excluding dummy commits)")
        print("=" * 50)
        
        commits = self.get_commit_history(limit)
        real_commits = []
        
        for commit in commits:
            if not self.is_dummy_commit(commit['message']) and not self.is_dummy_file_commit(commit['hash']):
                real_commits.append(commit)
        
        if not real_commits:
            print("No real commits found.")
            return
        
        for commit in real_commits:
            print(f"📝 {commit['date']} - {commit['message']}")
            print(f"   Hash: {commit['hash'][:8]}...")
            print(f"   Author: {commit['author']}")
            print()
        
        print(f"Total real commits: {len(real_commits)}")
    
    def show_dummy_commits(self, limit=None):
        """Show only dummy commits"""
        print("🤖 Dummy Commits")
        print("=" * 30)
        
        commits = self.get_commit_history(limit)
        dummy_commits = []
        
        for commit in commits:
            if self.is_dummy_commit(commit['message']) or self.is_dummy_file_commit(commit['hash']):
                dummy_commits.append(commit)
        
        if not dummy_commits:
            print("No dummy commits found.")
            return
        
        for commit in dummy_commits:
            print(f"🤖 {commit['date']} - {commit['message']}")
            print(f"   Hash: {commit['hash'][:8]}...")
            print()
        
        print(f"Total dummy commits: {len(dummy_commits)}")
    
    def count_commits(self, limit=None):
        """Count commits by type"""
        print("📊 Commit Statistics")
        print("=" * 30)
        
        commits = self.get_commit_history(limit)
        real_count = 0
        dummy_count = 0
        
        for commit in commits:
            if self.is_dummy_commit(commit['message']) or self.is_dummy_file_commit(commit['hash']):
                dummy_count += 1
            else:
                real_count += 1
        
        total = real_count + dummy_count
        
        print(f"Total commits: {total}")
        print(f"Real commits: {real_count} ({real_count/total*100:.1f}%)")
        print(f"Dummy commits: {dummy_count} ({dummy_count/total*100:.1f}%)")
        print()
        
        # Show dummy commit patterns
        dummy_patterns_count = {}
        for commit in commits:
            if self.is_dummy_commit(commit['message']):
                for pattern in self.dummy_patterns:
                    if pattern in commit['message']:
                        dummy_patterns_count[pattern] = dummy_patterns_count.get(pattern, 0) + 1
        
        if dummy_patterns_count:
            print("Most common dummy commit messages:")
            for pattern, count in sorted(dummy_patterns_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {pattern}: {count} times")
    
    def create_clean_branch(self, branch_name="clean-history"):
        """Create a clean branch without dummy commits"""
        print(f"🧹 Creating clean branch: {branch_name}")
        
        # Get all commits
        commits = self.get_commit_history()
        real_commits = []
        
        for commit in commits:
            if not self.is_dummy_commit(commit['message']) and not self.is_dummy_file_commit(commit['hash']):
                real_commits.append(commit['hash'])
        
        if not real_commits:
            print("No real commits found to create clean branch.")
            return
        
        # Create new branch
        self.run_git_command(f"git checkout -b {branch_name}")
        
        # Reset to the first real commit
        first_real_commit = real_commits[-1]  # Last in list is oldest
        self.run_git_command(f"git reset --hard {first_real_commit}")
        
        print(f"✅ Created clean branch '{branch_name}' with {len(real_commits)} real commits")
        print("🔍 You can now view clean history with: git log --oneline")
    
    def show_git_filters(self):
        """Show useful git filter commands"""
        print("🔧 Useful Git Filter Commands")
        print("=" * 40)
        print()
        print("1. Show only real commits:")
        print("   git log --grep='Update documentation' --invert-grep --grep='Fix minor bug' --invert-grep")
        print()
        print("2. Show commits excluding dummy files:")
        print("   git log -- . ':!daily_update_*.md' ':!contributions*.json'")
        print()
        print("3. Show commits from specific time period:")
        print("   git log --since='2025-01-01' --until='2025-03-13'")
        print()
        print("4. Show commits by author:")
        print("   git log --author='Your Name'")
        print()
        print("5. Show commits with specific file changes:")
        print("   git log --follow -- your-actual-file.py")
        print()
        print("6. Create a clean branch:")
        print("   git checkout -b clean-history")
        print("   git reset --hard <first-real-commit-hash>")

def main():
    parser = argparse.ArgumentParser(description='Git History Cleaner - Filter out dummy commits')
    parser.add_argument('--show-real', action='store_true',
                       help='Show only real commits (exclude dummy)')
    parser.add_argument('--show-dummy', action='store_true',
                       help='Show only dummy commits')
    parser.add_argument('--count', action='store_true',
                       help='Count commits by type')
    parser.add_argument('--clean-branch', action='store_true',
                       help='Create a clean branch without dummy commits')
    parser.add_argument('--limit', type=int,
                       help='Limit number of commits to analyze')
    parser.add_argument('--filters', action='store_true',
                       help='Show useful git filter commands')
    
    args = parser.parse_args()
    
    cleaner = GitHistoryCleaner()
    
    if args.filters:
        cleaner.show_git_filters()
    elif args.show_real:
        cleaner.show_real_commits(args.limit)
    elif args.show_dummy:
        cleaner.show_dummy_commits(args.limit)
    elif args.count:
        cleaner.count_commits(args.limit)
    elif args.clean_branch:
        cleaner.create_clean_branch()
    else:
        # Default: show statistics
        cleaner.count_commits(args.limit)

if __name__ == "__main__":
    main()
