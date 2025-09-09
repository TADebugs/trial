#!/usr/bin/env python3
"""
Setup Real GitHub Repositories for Daily Contributor

This script helps you configure the daily contributor with your actual
GitHub repositories by cloning them locally and updating the configuration.

Usage:
    python setup_real_repos.py
"""

import os
import json
import subprocess
import sys

def clone_github_repo(repo_url, local_path, repo_name):
    """Clone a GitHub repository to local path"""
    print(f"📥 Cloning {repo_name}...")
    
    try:
        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(local_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        # Clone the repository
        subprocess.run(['git', 'clone', repo_url, local_path], check=True)
        print(f"  ✅ Successfully cloned {repo_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to clone {repo_name}: {e}")
        return False

def update_repositories_config(repos):
    """Update the repositories.json file"""
    config_file = "repositories.json"
    
    with open(config_file, 'w') as f:
        json.dump(repos, f, indent=2)
    
    print(f"✅ Updated {config_file} with {len(repos)} repositories")

def main():
    print("🚀 Setup Real GitHub Repositories")
    print("=" * 40)
    print()
    
    # Get user input for repositories
    print("Enter your GitHub repositories (one per line, empty line to finish):")
    print("Format: https://github.com/username/repo-name")
    print()
    
    repos = []
    repo_count = 0
    
    while True:
        repo_url = input(f"Repository {repo_count + 1} URL (or press Enter to finish): ").strip()
        
        if not repo_url:
            break
        
        if not repo_url.startswith('https://github.com/'):
            print("  ⚠️  Please enter a valid GitHub URL")
            continue
        
        # Extract repo name from URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Set local path (you can customize this)
        local_path = f"./github-repos/{repo_name}"
        
        # Clone the repository
        if clone_github_repo(repo_url, local_path, repo_name):
            repos.append({
                "name": repo_name,
                "path": os.path.abspath(local_path),
                "description": f"GitHub repository: {repo_name}",
                "active": True
            })
            repo_count += 1
        
        print()
    
    if not repos:
        print("❌ No repositories added. Exiting.")
        return
    
    # Update configuration
    update_repositories_config(repos)
    
    print()
    print("🎉 Setup completed!")
    print()
    print("📋 Next steps:")
    print("  1. Test the configuration: python3 manage_branches.py --status")
    print("  2. Set up dummy branches: python3 manage_branches.py --setup-branches")
    print("  3. Test daily contributor: python3 daily_contributor.py --dry-run")
    print("  4. Run daily contributor: python3 daily_contributor.py")

if __name__ == "__main__":
    main()
