# GitHub Contribution Graph Filler

This repository contains scripts to help fill your GitHub contribution graph with dummy commits. Perfect for maintaining a consistent appearance when recruiters view your profile.

## ⚠️ Important Disclaimer

These scripts are for educational purposes and personal use. Use responsibly and be aware that:
- Some recruiters may notice patterns in commit messages
- This doesn't replace actual coding practice and skill development
- Always prioritize real contributions over artificial ones

## 🛡️ Safety Features

- **Safe Operation**: Only modifies a dedicated contributions file, never touches your actual code
- **Easy Undo**: Can be completely undone with simple git commands
- **Dry Run Mode**: Test what the script will do before making actual changes
- **Configurable**: Customize commit patterns, frequency, and time ranges

## 📁 Files Included

- `git_contributor.py` - Python version (recommended)
- `git_contributor.sh` - Shell script version
- `CONTRIBUTION_README.md` - This documentation

## 🚀 Quick Start

### Python Version (Recommended)

1. **Test first with dry run:**
   ```bash
   python3 git_contributor.py --dry-run
   ```

2. **Fill last 6 months with 2-5 commits per day:**
   ```bash
   python3 git_contributor.py --days-back 180 --min-commits 2 --max-commits 5
   ```

3. **Push to GitHub:**
   ```bash
   git push origin main
   ```

### Shell Script Version

1. **Test first with dry run:**
   ```bash
   ./git_contributor.sh --dry-run
   ```

2. **Fill last year with default settings:**
   ```bash
   ./git_contributor.sh
   ```

3. **Push to GitHub:**
   ```bash
   git push origin main
   ```

## ⚙️ Configuration Options

### Python Script Options

| Option | Description | Default |
|--------|-------------|---------|
| `--days-back N` | Number of days back to fill | 365 |
| `--commits-per-day N` | Average commits per day | 3 |
| `--min-commits N` | Minimum commits per day | 0 |
| `--max-commits N` | Maximum commits per day | 8 |
| `--dry-run` | Show what would be done without changes | False |

### Shell Script Options

Same options as Python version, but use `--help` to see full list.

## 📊 Example Usage Scenarios

### Scenario 1: Light Activity (1-3 commits/day)
```bash
python3 git_contributor.py --min-commits 1 --max-commits 3 --days-back 90
```

### Scenario 2: Heavy Activity (5-10 commits/day)
```bash
python3 git_contributor.py --min-commits 5 --max-commits 10 --days-back 180
```

### Scenario 3: Weekend Warrior (skip weekends)
The script automatically skips weekends 70% of the time to look more natural.

### Scenario 4: Recent Activity Only
```bash
python3 git_contributor.py --days-back 30 --commits-per-day 4
```

## 🔄 Undoing Changes

If you want to remove all the dummy commits:

```bash
# Find out how many commits were added
git log --oneline | wc -l

# Reset to before the dummy commits (replace N with actual number)
git reset --hard HEAD~N

# Remove the contributions file
rm contributions.json  # or contributions.txt for shell version

# Force push to update GitHub
git push --force origin main
```

## 🎯 Tips for Natural-Looking Contributions

1. **Vary commit times**: The script uses work hours (9 AM - 10 PM) for more realistic timestamps
2. **Mix commit frequencies**: Some days have 0 commits, others have more
3. **Professional messages**: All commit messages look like real development work
4. **Skip weekends**: 70% chance of skipping weekend days
5. **Gradual increase**: Consider running the script multiple times with different date ranges

## 🔍 How It Works

1. **Creates a contributions file**: Either `contributions.json` (Python) or `contributions.txt` (Shell)
2. **Generates realistic timestamps**: Random times within work hours
3. **Uses professional commit messages**: From a curated list of realistic messages
4. **Creates git commits**: With past timestamps using `--date` flag
5. **Safe operation**: Never modifies your actual code files

## 🛠️ Troubleshooting

### "Not in a git repository" error
Make sure you're running the script from a directory that contains a `.git` folder.

### "Permission denied" error (Shell script)
Make the script executable:
```bash
chmod +x git_contributor.sh
```

### Python not found
Install Python 3 or use `python` instead of `python3`:
```bash
python git_contributor.py --dry-run
```

### Commits not showing on GitHub
- Make sure you've pushed to the correct branch
- Check that your GitHub email matches your git config
- Wait a few minutes for GitHub to update

## 📝 Commit Messages Used

The script uses professional-sounding commit messages like:
- "Update documentation"
- "Fix minor bug"
- "Refactor code"
- "Add feature"
- "Improve performance"
- "Update dependencies"
- "Fix typo"
- "Optimize code"
- "Add tests"
- "Update README"

## ⚖️ Ethical Considerations

While this tool can help with appearance, remember:
- **Real skills matter more**: Focus on building actual projects
- **Be honest**: If asked about specific commits, be transparent
- **Use as supplement**: Don't rely solely on this for your portfolio
- **Learn continuously**: Use this time to actually improve your coding skills

## 🤝 Contributing

Feel free to improve these scripts:
- Add more realistic commit messages
- Improve the randomization algorithms
- Add more configuration options
- Create versions for other languages

## 📄 License

This project is for educational purposes. Use responsibly and at your own discretion.

---

**Remember**: The best way to have a great GitHub profile is to consistently work on real projects and contribute to open source. This tool should be used as a supplement, not a replacement for genuine development work.
