#!/usr/bin/env python3
"""
Setup script for Daily GitHub Contributor

This script helps you set up the daily contributor by:
1. Creating the repositories.json file
2. Setting up the necessary directories
3. Testing the configuration

Usage:
    python setup_daily_contributor.py
"""

import os
import json
import subprocess
from datetime import datetime

def create_sample_repositories():
    """Create sample repository directories and git repos"""
    base_dir = os.getcwd()
    
    # Sample repositories to create
    repos = [
        {
            "name": "learning-projects",
            "path": os.path.join(base_dir, "learning-projects"),
            "description": "Personal learning projects and tutorials",
            "active": True
        },
        {
            "name": "experiments",
            "path": os.path.join(base_dir, "experiments"),
            "description": "Code experiments and prototypes",
            "active": True
        },
        {
            "name": "utilities",
            "path": os.path.join(base_dir, "utilities"),
            "description": "Utility scripts and tools",
            "active": True
        },
        {
            "name": "documentation",
            "path": os.path.join(base_dir, "documentation"),
            "description": "Documentation and notes",
            "active": True
        }
    ]
    
    print("🏗️  Setting up sample repositories...")
    
    for repo in repos:
        repo_path = repo['path']
        
        # Create directory if it doesn't exist
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
            print(f"  ✅ Created directory: {repo_path}")
        
        # Initialize git repository if it doesn't exist
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            try:
                subprocess.run(['git', 'init'], cwd=repo_path, check=True)
                print(f"  ✅ Initialized git repo: {repo['name']}")
            except subprocess.CalledProcessError:
                print(f"  ⚠️  Could not initialize git repo: {repo['name']}")
        
        # Create a README file
        readme_path = os.path.join(repo_path, 'README.md')
        if not os.path.exists(readme_path):
            readme_content = f"""# {repo['name'].title()}

{repo['description']}

## About

This repository is used for daily GitHub contributions to maintain consistent activity.

## Files

- `daily_update_YYYYMMDD.md` - Daily update files
- `README.md` - This file

## Usage

This repository is automatically updated by the Daily GitHub Contributor script.
"""
            
            with open(readme_path, 'w') as f:
                f.write(readme_content)
            
            # Add and commit the README
            try:
                subprocess.run(['git', 'add', 'README.md'], cwd=repo_path, check=True)
                subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=repo_path, check=True)
                print(f"  ✅ Created README for: {repo['name']}")
                
                # Create documentation branch
                subprocess.run(['git', 'checkout', '-b', 'documentation'], cwd=repo_path, check=True)
                print(f"  ✅ Created documentation branch for: {repo['name']}")
                
                # Switch back to main
                subprocess.run(['git', 'checkout', 'main'], cwd=repo_path, check=True)
                print(f"  ✅ Switched back to main for: {repo['name']}")
                
            except subprocess.CalledProcessError:
                print(f"  ⚠️  Could not commit README for: {repo['name']}")
    
    return repos

def save_repositories_config(repos):
    """Save the repositories configuration to file"""
    config_file = "repositories.json"
    
    with open(config_file, 'w') as f:
        json.dump(repos, f, indent=2)
    
    print(f"  ✅ Saved configuration to: {config_file}")

def create_cron_setup_script():
    """Create a script to help set up cron job"""
    cron_script = """#!/bin/bash
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
"""
    
    with open("setup_cron.sh", 'w') as f:
        f.write(cron_script)
    
    os.chmod("setup_cron.sh", 0o755)
    print("  ✅ Created cron setup script: setup_cron.sh")

def create_manual_run_script():
    """Create a script for manual runs"""
    manual_script = """#!/bin/bash
# Manual Daily Contributor Runner
# Run this script to manually trigger daily commits

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 Running Daily GitHub Contributor..."
python3 daily_contributor.py

echo "✅ Manual run completed!"
"""
    
    with open("run_daily.sh", 'w') as f:
        f.write(manual_script)
    
    os.chmod("run_daily.sh", 0o755)
    print("  ✅ Created manual run script: run_daily.sh")

def main():
    print("🚀 Daily GitHub Contributor Setup")
    print("=" * 40)
    print()
    
    # Create sample repositories
    repos = create_sample_repositories()
    
    # Save configuration
    save_repositories_config(repos)
    
    # Create helper scripts
    create_cron_setup_script()
    create_manual_run_script()
    
    print()
    print("🎉 Setup completed successfully!")
    print()
    print("📋 Next steps:")
    print("  1. Edit repositories.json to add your actual repositories")
    print("  2. Test the script: python3 daily_contributor.py --dry-run")
    print("  3. Run manually: ./run_daily.sh")
    print("  4. Set up automation: ./setup_cron.sh")
    print()
    print("📊 View scheduling algorithm: python3 daily_contributor.py --show-algorithm")

if __name__ == "__main__":
    main()
