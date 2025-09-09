# GitHub Contribution Tools

This folder contains all the tools for managing GitHub contributions and maintaining consistent activity.

## 📁 Files Overview

### **Main Scripts:**
- `git_contributor.py` - Python script for filling contribution graphs
- `git_contributor.sh` - Shell script version
- `git_contributor_historical.py` - Historical contribution filler (12-6 months ago)
- `daily_contributor.py` - Daily automatic contributor with branch management

### **Setup & Management:**
- `setup_daily_contributor.py` - Initial setup for daily contributor
- `setup_real_repos.py` - Setup script for real GitHub repositories
- `manage_branches.py` - Branch management for documentation commits
- `clean_history.py` - Clean git history from dummy commits

### **Utility Scripts:**
- `identify_dummy_commits.sh` - Identify dummy commits in repositories
- `setup_cron.sh` - Set up automatic daily runs
- `run_daily.sh` - Manual daily run script

### **Configuration Files:**
- `repositories.json` - Repository configuration
- `contributions.json` - Contribution tracking
- `contributions_historical.json` - Historical contributions

### **Documentation:**
- `CONTRIBUTION_README.md` - Comprehensive usage guide

## 🚀 Quick Start

1. **Set up repositories:**
   ```bash
   python3 setup_real_repos.py
   ```

2. **Set up branches:**
   ```bash
   python3 manage_branches.py --setup-branches
   ```

3. **Test daily contributor:**
   ```bash
   python3 daily_contributor.py --dry-run
   ```

4. **Set up automation:**
   ```bash
   ./setup_cron.sh
   ```

## 🎯 Key Features

- **Clean main branches** - Never touches your real work
- **Documentation branches** - All dummy commits go to separate branches
- **Natural patterns** - Realistic commit timing and messages
- **Multi-repository** - Works with multiple GitHub repos
- **Easy management** - Simple commands to manage everything

## ⚠️ Important Notes

- All dummy commits go to "documentation" branches
- Main branches stay completely clean
- Use `clean_history.py` to filter out dummy commits if needed
- Configure `repositories.json` with your actual GitHub repos
