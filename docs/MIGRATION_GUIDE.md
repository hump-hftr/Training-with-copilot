# Migration Guide - Moving Trading App to New Repository

## Overview

This guide explains how to move the IBKR trading app from the `Training-with-copilot` repository to a new dedicated repository.

---

## Why Separate Repository?

**Benefits:**
- ✅ Clean separation from high school management app
- ✅ Independent version control and release cycles
- ✅ Focused project scope and documentation
- ✅ Separate issue tracking and project management
- ✅ Clearer for collaborators and future maintenance
- ✅ Independent deployment and CI/CD

---

## Files to Migrate

### Documentation Files (from `docs/`)
```
docs/EXECUTIVE_SUMMARY.md
docs/IBKR_TRADING_APP_ARCHITECTURE.md
docs/IBKR_TRADING_APP_WORKPLAN.md
docs/IBKR_TRADING_APP_README.md
docs/SETUP_GUIDE.md
docs/SECURITY_SUMMARY.md
docs/PHASE0_REQUIREMENTS.md
docs/INDEX.md
```

### Configuration Files (from `src/trading_app/`)
```
src/trading_app/.env.example
src/trading_app/requirements.txt
```

### Project Files (root)
```
.gitignore (trading-specific parts)
```

### Files NOT to Migrate
- High school app files (`src/app.py`, `src/backend/`, `src/static/`)
- Original README.md (belongs to high school project)
- PROJECT_README.md (was temporary)

---

## Migration Steps

### Option 1: Manual Migration (Recommended)

#### Step 1: Create New Repository
1. Go to GitHub and create new repository
   - Suggested name: `ibkr-trading-app` or `trading-system`
   - Description: "IBKR trading application with position tracking, watchlist management, and automated opportunity analysis"
   - Visibility: Private (recommended for trading apps)
   - Initialize with: None (we'll push existing content)

#### Step 2: Clone New Repository
```bash
git clone https://github.com/your-username/ibkr-trading-app.git
cd ibkr-trading-app
```

#### Step 3: Copy Documentation
```bash
# Copy all trading-related docs
cp /path/to/Training-with-copilot/docs/EXECUTIVE_SUMMARY.md ./docs/
cp /path/to/Training-with-copilot/docs/IBKR_TRADING_APP_ARCHITECTURE.md ./docs/
cp /path/to/Training-with-copilot/docs/IBKR_TRADING_APP_WORKPLAN.md ./docs/
cp /path/to/Training-with-copilot/docs/IBKR_TRADING_APP_README.md ./docs/
cp /path/to/Training-with-copilot/docs/SETUP_GUIDE.md ./docs/
cp /path/to/Training-with-copilot/docs/SECURITY_SUMMARY.md ./docs/
cp /path/to/Training-with-copilot/docs/PHASE0_REQUIREMENTS.md ./docs/
cp /path/to/Training-with-copilot/docs/INDEX.md ./docs/
```

#### Step 4: Reorganize and Rename
```bash
# Move main README to root
cp docs/IBKR_TRADING_APP_README.md README.md

# Rename other docs (remove IBKR_TRADING_APP_ prefix)
mv docs/IBKR_TRADING_APP_ARCHITECTURE.md docs/ARCHITECTURE.md
mv docs/IBKR_TRADING_APP_WORKPLAN.md docs/WORKPLAN.md

# Update INDEX.md to reflect new names
```

#### Step 5: Create Project Structure
```bash
# Create standard Python project structure
mkdir -p src/trading_app/{models,ibkr,analysis,routers,static,utils}
mkdir -p tests scripts logs

# Copy configuration templates
cp /path/to/Training-with-copilot/src/trading_app/.env.example .env.example
cp /path/to/Training-with-copilot/src/trading_app/requirements.txt requirements.txt

# Create __init__.py files
touch src/__init__.py
touch src/trading_app/__init__.py
touch src/trading_app/{models,ibkr,analysis,routers,utils}/__init__.py
```

#### Step 6: Create Root README
Create `README.md` with:
```markdown
# IBKR Trading Application

Automated trading system for Interactive Brokers with position tracking, 
watchlist management, and opportunity analysis using technical indicators.

## Features
- 5-minute OHLC bar analysis
- Breakout detection
- Moving average crossovers
- Trailing stop orders
- Kill switch for emergency exits
- Multi-exchange support (NASDAQ, TSE)

## Quick Start
See [SETUP_GUIDE.md](docs/SETUP_GUIDE.md)

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Work Plan](docs/WORKPLAN.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Requirements](docs/PHASE0_REQUIREMENTS.md)

## Status
Phase 0: Requirements gathering complete ✅
Phase 1: Implementation starting

## License
[Your chosen license]
```

#### Step 7: Create .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv

# Environment
.env
.env.local

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage

# OS
.DS_Store
Thumbs.db
```

#### Step 8: Commit and Push
```bash
git add .
git commit -m "Initial commit: Trading app architecture and documentation

- Complete system architecture (SQLite-based)
- 8-week implementation work plan
- Phase 0 requirements gathered
- Security audit complete
- Setup and configuration guides"

git push origin main
```

### Option 2: Using Git Subtree (Advanced)

If you want to preserve commit history:

```bash
# In the old repo, create a subtree of trading-specific files
cd /path/to/Training-with-copilot
git subtree split -P docs -b trading-app-docs

# In new repo
cd /path/to/ibkr-trading-app
git remote add old-repo /path/to/Training-with-copilot
git pull old-repo trading-app-docs --allow-unrelated-histories
```

**Note:** This is more complex and may not be worth it for documentation-only files.

---

## Post-Migration Updates

### Update Documentation References

In the new repo, update all documentation to remove references to the old repo:

1. **INDEX.md** - Update file paths
2. **EXECUTIVE_SUMMARY.md** - Update repository name
3. **ARCHITECTURE.md** - Update any repo-specific references
4. **WORKPLAN.md** - Update file structure references

### Update Architecture for SQLite

Based on Phase 0 feedback, update architecture document:

1. Change MongoDB to SQLite
2. Update schema for 5-minute bars
3. Add breakout detection specifications
4. Document kill switch implementation
5. Add multi-exchange support details

### Create New Issues

Transfer relevant issues to new repo:
- Phase 1 implementation tasks
- Phase 2 feature requests
- Future ML integration planning

---

## Recommended New Repository Structure

```
ibkr-trading-app/
├── README.md                    # Main project README
├── LICENSE                      # Your license choice
├── .gitignore                   # Python/trading specific
├── .env.example                 # Configuration template
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup (optional)
├── pyproject.toml              # Modern Python config (optional)
│
├── docs/                        # Documentation
│   ├── INDEX.md                # Doc navigation
│   ├── ARCHITECTURE.md         # System design
│   ├── WORKPLAN.md            # Implementation plan
│   ├── SETUP_GUIDE.md         # Installation
│   ├── PHASE0_REQUIREMENTS.md # User requirements
│   ├── SECURITY_SUMMARY.md    # Security docs
│   └── EXECUTIVE_SUMMARY.md   # Overview
│
├── src/                        # Source code
│   └── trading_app/
│       ├── __init__.py
│       ├── main.py            # Application entry
│       ├── config.py          # Configuration
│       ├── database.py        # SQLite setup
│       │
│       ├── models/            # Data models
│       │   ├── __init__.py
│       │   ├── position.py
│       │   ├── watchlist.py
│       │   └── order.py
│       │
│       ├── ibkr/              # IBKR integration
│       │   ├── __init__.py
│       │   ├── connector.py
│       │   ├── data_feed.py
│       │   └── order_manager.py
│       │
│       ├── analysis/          # Analysis engine
│       │   ├── __init__.py
│       │   ├── indicators.py
│       │   ├── breakout.py
│       │   └── patterns.py
│       │
│       ├── routers/           # API routes
│       │   ├── __init__.py
│       │   ├── positions.py
│       │   ├── orders.py
│       │   └── watchlist.py
│       │
│       ├── static/            # Frontend
│       │   ├── index.html
│       │   ├── css/
│       │   └── js/
│       │
│       └── utils/             # Utilities
│           ├── __init__.py
│           ├── logger.py
│           └── helpers.py
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_ibkr.py
│   └── test_analysis.py
│
├── scripts/                    # Utility scripts
│   ├── setup_database.py
│   ├── import_data.py
│   └── run_analysis.py
│
└── logs/                       # Application logs
    └── .gitkeep
```

---

## Cleanup in Original Repository

After successful migration:

1. **Remove trading app files** from Training-with-copilot repo
2. **Update original README** to note trading app has moved
3. **Close related issues** with note about new repo
4. **Optional:** Add link to new repo in original README

---

## Benefits After Migration

✅ Clear project boundaries  
✅ Independent development cycles  
✅ Better suited for collaboration  
✅ Cleaner CI/CD pipeline  
✅ Trading-specific issue tracking  
✅ Appropriate security model  
✅ Professional presentation  

---

## Next Steps After Migration

1. Set up CI/CD (GitHub Actions)
2. Configure branch protection rules
3. Set up issue templates
4. Configure dependabot for security updates
5. Begin Phase 1 implementation
6. Set up project board for tracking

---

**Estimated Migration Time:** 30-60 minutes

**Recommended Approach:** Manual migration (Option 1) - cleaner and simpler

**When to Migrate:** Before starting Phase 1 implementation

---

**Questions?** Refer to the documentation in the new repository once migrated.
