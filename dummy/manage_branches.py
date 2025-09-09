#!/usr/bin/env python3
"""
Branch Management Script for Documentation Commits

This script helps you manage the branch strategy for documentation commits:
- Create documentation branches in all repositories
- Switch between main and documentation branches
- Push documentation commits to GitHub
- Keep main branches clean

Usage:
    python manage_branches.py [options]

Options:
    --setup-branches     Create dummy-commits branches in all repos
    --switch-to-dummy    Switch all repos to dummy-commits branch
    --switch-to-main     Switch all repos to main branch
    --push-dummy         Push dummy-commits branches to GitHub
    --status             Show current branch status
    --help               Show this help message
"""

import os
import sys
import json
import subprocess
import argparse

class BranchManager:
    def __init__(self):
        self.repos_file = "repositories.json"
        self.dummy_branch = "documentation"
        self.main_branch = "main"
    
    def load_repositories(self):
        """Load repositories from file"""
        try:
            with open(self.repos_file, 'r') as f:
                repos = json.load(f)
            return [repo for repo in repos if repo.get('active', True)]
        except:
            return []
    
    def run_git_command(self, command, repo_path):
        """Run a git command in a specific repository"""
        try:
            result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error in {os.path.basename(repo_path)}: {e.stderr}")
            return None
    
    def get_current_branch(self, repo_path):
        """Get current branch name"""
        result = self.run_git_command(['git', 'branch', '--show-current'], repo_path)
        return result if result else "unknown"
    
    def branch_exists(self, repo_path, branch_name):
        """Check if a branch exists"""
        result = self.run_git_command(['git', 'branch', '--list', branch_name], repo_path)
        return branch_name in result if result else False
    
    def create_dummy_branch(self, repo_path, repo_name):
        """Create documentation branch"""
        print(f"  📁 {repo_name}:")
        
        # Check if documentation branch exists
        if self.branch_exists(repo_path, self.dummy_branch):
            print(f"    ✅ {self.dummy_branch} branch already exists")
            return True
        
        # Create documentation branch from main
        result = self.run_git_command(['git', 'checkout', '-b', self.dummy_branch, self.main_branch], repo_path)
        if result is not None:
            print(f"    ✅ Created {self.dummy_branch} branch from {self.main_branch}")
            return True
        else:
            print(f"    ❌ Failed to create {self.dummy_branch} branch")
            return False
    
    def switch_to_branch(self, repo_path, repo_name, target_branch):
        """Switch to a specific branch"""
        print(f"  📁 {repo_name}:")
        
        current_branch = self.get_current_branch(repo_path)
        if current_branch == target_branch:
            print(f"    ✅ Already on {target_branch} branch")
            return True
        
        # Check if target branch exists
        if not self.branch_exists(repo_path, target_branch):
            print(f"    ❌ {target_branch} branch does not exist")
            return False
        
        # Switch to target branch
        result = self.run_git_command(['git', 'checkout', target_branch], repo_path)
        if result is not None:
            print(f"    ✅ Switched to {target_branch} branch")
            return True
        else:
            print(f"    ❌ Failed to switch to {target_branch} branch")
            return False
    
    def push_branch(self, repo_path, repo_name, branch_name):
        """Push a branch to GitHub"""
        print(f"  📁 {repo_name}:")
        
        # Check if we're on the right branch
        current_branch = self.get_current_branch(repo_path)
        if current_branch != branch_name:
            print(f"    ⚠️  Not on {branch_name} branch (currently on {current_branch})")
            return False
        
        # Push the branch
        result = self.run_git_command(['git', 'push', 'origin', branch_name], repo_path)
        if result is not None:
            print(f"    ✅ Pushed {branch_name} branch to GitHub")
            return True
        else:
            print(f"    ❌ Failed to push {branch_name} branch")
            return False
    
    def setup_branches(self):
        """Create documentation branches in all repositories"""
        print("🏗️  Setting up documentation branches...")
        print("=" * 50)
        
        repos = self.load_repositories()
        if not repos:
            print("❌ No repositories found. Please run setup_daily_contributor.py first.")
            return
        
        success_count = 0
        for repo in repos:
            if self.create_dummy_branch(repo['path'], repo['name']):
                success_count += 1
        
        print(f"\n✅ Successfully set up {success_count}/{len(repos)} repositories")
    
    def switch_to_dummy(self):
        """Switch all repositories to documentation branch"""
        print("🔄 Switching to documentation branches...")
        print("=" * 50)
        
        repos = self.load_repositories()
        if not repos:
            print("❌ No repositories found.")
            return
        
        success_count = 0
        for repo in repos:
            if self.switch_to_branch(repo['path'], repo['name'], self.dummy_branch):
                success_count += 1
        
        print(f"\n✅ Successfully switched {success_count}/{len(repos)} repositories")
    
    def switch_to_main(self):
        """Switch all repositories to main branch"""
        print("🔄 Switching to main branches...")
        print("=" * 50)
        
        repos = self.load_repositories()
        if not repos:
            print("❌ No repositories found.")
            return
        
        success_count = 0
        for repo in repos:
            if self.switch_to_branch(repo['path'], repo['name'], self.main_branch):
                success_count += 1
        
        print(f"\n✅ Successfully switched {success_count}/{len(repos)} repositories")
    
    def push_dummy(self):
        """Push documentation branches to GitHub"""
        print("📤 Pushing documentation branches to GitHub...")
        print("=" * 50)
        
        repos = self.load_repositories()
        if not repos:
            print("❌ No repositories found.")
            return
        
        success_count = 0
        for repo in repos:
            if self.push_branch(repo['path'], repo['name'], self.dummy_branch):
                success_count += 1
        
        print(f"\n✅ Successfully pushed {success_count}/{len(repos)} repositories")
    
    def show_status(self):
        """Show current branch status for all repositories"""
        print("📊 Current Branch Status")
        print("=" * 30)
        
        repos = self.load_repositories()
        if not repos:
            print("❌ No repositories found.")
            return
        
        for repo in repos:
            current_branch = self.get_current_branch(repo['path'])
            dummy_exists = self.branch_exists(repo['path'], self.dummy_branch)
            main_exists = self.branch_exists(repo['path'], self.main_branch)
            
            print(f"📁 {repo['name']}:")
            print(f"  Current branch: {current_branch}")
            print(f"  {self.main_branch} exists: {'✅' if main_exists else '❌'}")
            print(f"  {self.dummy_branch} exists: {'✅' if dummy_exists else '❌'}")
            print()

def main():
    parser = argparse.ArgumentParser(description='Branch Management for Documentation Commits')
    parser.add_argument('--setup-branches', action='store_true',
                       help='Create documentation branches in all repos')
    parser.add_argument('--switch-to-dummy', action='store_true',
                       help='Switch all repos to documentation branch')
    parser.add_argument('--switch-to-main', action='store_true',
                       help='Switch all repos to main branch')
    parser.add_argument('--push-dummy', action='store_true',
                       help='Push documentation branches to GitHub')
    parser.add_argument('--status', action='store_true',
                       help='Show current branch status')
    
    args = parser.parse_args()
    
    manager = BranchManager()
    
    if args.setup_branches:
        manager.setup_branches()
    elif args.switch_to_dummy:
        manager.switch_to_dummy()
    elif args.switch_to_main:
        manager.switch_to_main()
    elif args.push_dummy:
        manager.push_dummy()
    elif args.status:
        manager.show_status()
    else:
        # Default: show status
        manager.show_status()

if __name__ == "__main__":
    main()
