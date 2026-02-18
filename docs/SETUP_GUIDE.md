# IBKR Trading App - Detailed Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [IBKR Account Configuration](#ibkr-account-configuration)
3. [System Setup](#system-setup)
4. [Application Installation](#application-installation)
5. [Configuration](#configuration)
6. [First Run](#first-run)
7. [Verification](#verification)
8. [Common Issues](#common-issues)

## Prerequisites

### 1. Interactive Brokers Account

**Required:**
- Active IBKR account (individual or institution)
- Account must have API access enabled
- Recommended: Paper Trading account for initial testing

**To Enable API Access:**
1. Log in to IBKR Client Portal (https://www.interactivebrokers.com)
2. Navigate to Settings → Account Settings
3. Under "Trading Platforms", find "API"
4. Enable "API Access"
5. Save changes

### 2. Trading Platform (TWS or IB Gateway)

**Option A: Trader Workstation (TWS)** - Full-featured platform
- Download: https://www.interactivebrokers.com/en/trading/tws.php
- Size: ~500MB
- Best for: Users who want full trading interface

**Option B: IB Gateway** - Lightweight API gateway (Recommended)
- Download: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php
- Size: ~100MB
- Best for: Automated trading, running as service

**Recommendation:** Use IB Gateway for this application as it's lighter and specifically designed for API access.

### 3. Python Environment

**Minimum Requirements:**
- Python 3.11 or higher
- pip (Python package installer)
- virtualenv (recommended)

**Check Your Python Version:**
```bash
python --version
# or
python3 --version
```

**Install Python (if needed):**
- Windows: https://www.python.org/downloads/
- macOS: `brew install python3`
- Linux: `sudo apt install python3.11 python3-pip`

### 4. MongoDB Database

**Option A: Local Installation**
- Windows: https://www.mongodb.com/try/download/community
- macOS: `brew install mongodb-community`
- Linux: `sudo apt install mongodb`

**Option B: MongoDB Atlas (Cloud)** - Recommended for beginners
1. Create free account: https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Add IP address to whitelist

### 5. System Requirements

**Minimum:**
- OS: Windows 10, macOS 10.14, Ubuntu 18.04 (or equivalent)
- RAM: 4GB
- Disk: 2GB free space
- Network: Stable internet connection

**Recommended:**
- RAM: 8GB+
- SSD storage
- Dedicated machine or VPS for 24/7 operation

## IBKR Account Configuration

### Step 1: Install TWS/IB Gateway

1. **Download the installer:**
   - TWS: https://www.interactivebrokers.com/en/trading/tws.php
   - IB Gateway: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php

2. **Install:**
   - Windows: Run `.exe` installer
   - macOS: Run `.dmg` and drag to Applications
   - Linux: Run `.sh` script

3. **Launch the application:**
   - First launch will download updates
   - Wait for update to complete

### Step 2: Configure API Settings

1. **Open Configuration:**
   - TWS: File → Global Configuration → API → Settings
   - IB Gateway: Configuration → API → Settings

2. **Configure Settings:**
   ```
   ✅ Enable ActiveX and Socket Clients
   ✅ Allow connections from localhost
   ✅ Read-Only API (for testing, uncheck later for trading)
   
   Socket Port: 7497 (paper trading) or 7496 (live trading)
   Master API client ID: Leave at 0
   
   ⚠️ Trusted IP Addresses: Add 127.0.0.1
   ```

3. **Save Configuration:**
   - Click "OK" to save
   - Restart TWS/Gateway if prompted

### Step 3: Paper Trading Account Setup (Recommended)

1. **Switch to Paper Trading:**
   - TWS: Login screen → Select "IB Paper Trading"
   - IB Gateway: Use paper trading credentials

2. **Paper Trading Credentials:**
   - Usually same username as live account
   - Password: Your live password (unless you've set a separate one)
   - Account ID: Will start with "DU" (e.g., DU1234567)

3. **Verify Paper Trading Mode:**
   - Look for "PAPER" indicator in title bar
   - Account value will show simulated funds ($1,000,000 default)

## System Setup

### Step 1: Install MongoDB

**Local Installation (Windows):**
```bash
# Download and install MongoDB Community Server
# Start MongoDB service
net start MongoDB
```

**Local Installation (macOS):**
```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community
```

**Local Installation (Linux):**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb
sudo systemctl start mongod
sudo systemctl enable mongod
```

**MongoDB Atlas (Cloud):**
1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Create database user
4. Whitelist your IP (or 0.0.0.0/0 for development)
5. Get connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

### Step 2: Verify MongoDB Installation

```bash
# Check if MongoDB is running
mongo --eval "db.version()"

# Expected output: MongoDB version number
```

## Application Installation

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/hump-hftr/Training-with-copilot.git
cd Training-with-copilot
```

### Step 2: Create Python Virtual Environment

```bash
# Navigate to trading app directory
cd src/trading_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Verify activation (should show venv in prompt)
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

**Required Packages:**
```
fastapi>=0.115.12
uvicorn[standard]>=0.34.2
pymongo>=4.12.1
ib_insync>=0.9.86
pandas>=2.0.0
pandas-ta>=0.3.14b
yfinance>=0.2.36
python-dotenv>=1.0.0
pydantic>=2.0.0
```

### Step 4: Create Project Structure

```bash
# Create necessary directories
mkdir -p src/trading_app/{models,ibkr,analysis,routers,static/css,static/js,utils}
mkdir -p scripts tests logs

# Create __init__.py files
touch src/trading_app/__init__.py
touch src/trading_app/models/__init__.py
touch src/trading_app/ibkr/__init__.py
touch src/trading_app/analysis/__init__.py
touch src/trading_app/routers/__init__.py
touch src/trading_app/utils/__init__.py
```

## Configuration

### Step 1: Create Environment File

```bash
# Copy example environment file
cp .env.example .env

# Edit with your preferred editor
nano .env  # or vim, code, etc.
```

### Step 2: Configure Environment Variables

**Edit `.env` file:**

```bash
# ============================================
# MONGODB CONFIGURATION
# ============================================
# For local MongoDB:
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=ibkr_trading_app

# For MongoDB Atlas (cloud):
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
# MONGODB_DB=ibkr_trading_app

# ============================================
# IBKR CONFIGURATION
# ============================================
IBKR_HOST=127.0.0.1

# Port for TWS/Gateway
IBKR_PORT=7497           # 7497 for paper trading
                         # 7496 for live trading

# Client ID (must be unique if running multiple instances)
IBKR_CLIENT_ID=1

# Your IBKR Account ID (found in TWS/Gateway)
IBKR_ACCOUNT_ID=DU1234567  # Replace with your account ID

# ============================================
# APPLICATION SETTINGS
# ============================================
# Refresh interval in seconds
REFRESH_INTERVAL=300

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# API CORS origins (for production)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# ============================================
# ANALYSIS SETTINGS
# ============================================
# RSI (Relative Strength Index)
RSI_PERIOD=14
RSI_OVERSOLD=30          # Buy signal threshold
RSI_OVERBOUGHT=70        # Sell signal threshold

# MACD (Moving Average Convergence Divergence)
MACD_FAST=12
MACD_SLOW=26
MACD_SIGNAL=9

# Moving Averages
SMA_SHORT=50             # Short-term MA period
SMA_LONG=200             # Long-term MA period

# Opportunity Scoring
MIN_OPPORTUNITY_SCORE=6.0  # Minimum score to display
MAX_OPPORTUNITIES=20        # Max opportunities to show

# ============================================
# OPTIONAL: EXTERNAL DATA SOURCES
# ============================================
# Alpha Vantage (for market data backup)
# ALPHA_VANTAGE_API_KEY=your_key_here

# Yahoo Finance timeout
YFINANCE_TIMEOUT=10
```

### Step 3: Configure Secrets (Production Only)

**For production, use a secrets manager:**

```bash
# Example using environment variables
export IBKR_ACCOUNT_ID="your_account_id"
export MONGODB_URI="your_mongodb_uri"
```

## First Run

### Step 1: Initialize Database

```bash
# Run database setup script
python scripts/setup_database.py

# Expected output:
# ✓ Connected to MongoDB
# ✓ Created database: ibkr_trading_app
# ✓ Created collections
# ✓ Created indexes
# ✓ Database initialized successfully
```

### Step 2: Start TWS/IB Gateway

1. **Launch TWS or IB Gateway**
2. **Login with paper trading credentials**
3. **Wait for connection to complete**
4. **Verify API is enabled** (check configuration)

### Step 3: Test IBKR Connection

```bash
# Run connection test script
python scripts/test_ibkr_connection.py

# Expected output:
# ✓ Connected to IBKR
# ✓ Account ID: DU1234567
# ✓ Connection working
```

### Step 4: Start Application

```bash
# Start the FastAPI application
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

### Step 5: Access Application

1. **Open browser:** http://localhost:8000
2. **Check API docs:** http://localhost:8000/docs
3. **Verify UI loads correctly**

## Verification

### Step 1: Check System Health

```bash
# Test MongoDB connection
curl http://localhost:8000/api/health/database

# Test IBKR connection
curl http://localhost:8000/api/health/ibkr

# Check application status
curl http://localhost:8000/api/health
```

### Step 2: Sync Initial Positions

```bash
# Via API
curl -X POST http://localhost:8000/api/positions/sync

# Via UI
# Click "Sync Positions" button in dashboard
```

### Step 3: Add Test Watchlist Item

```bash
# Via API
curl -X POST http://localhost:8000/api/watchlist \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "notes": "Test symbol",
    "target_price": 200.0
  }'

# Via UI
# Go to Watchlist → Add Symbol → Enter AAPL
```

### Step 4: Run Analysis

```bash
# Via API
curl -X POST http://localhost:8000/api/opportunities/analyze

# Via UI
# Click "Analyze" button in opportunities view
```

### Step 5: View Results

```bash
# Get opportunities
curl http://localhost:8000/api/opportunities/top?limit=5

# Expected: JSON array of opportunities with scores
```

## Common Issues

### Issue 1: Cannot Connect to IBKR

**Symptoms:**
- Error: "Connection refused" or "Socket error"

**Solutions:**
1. ✅ Verify TWS/Gateway is running
2. ✅ Check port number (7497 for paper, 7496 for live)
3. ✅ Verify API is enabled in configuration
4. ✅ Check firewall settings
5. ✅ Try changing CLIENT_ID in .env
6. ✅ Restart TWS/Gateway

**Test Connection:**
```bash
# Test if port is open
telnet localhost 7497
# Should connect without error
```

### Issue 2: MongoDB Connection Failed

**Symptoms:**
- Error: "Connection refused" or "Authentication failed"

**Solutions:**
1. ✅ Verify MongoDB is running: `mongosh`
2. ✅ Check MONGODB_URI in .env
3. ✅ For Atlas: verify IP whitelist
4. ✅ For Atlas: verify username/password
5. ✅ Check network connectivity

**Test MongoDB:**
```bash
# Local MongoDB
mongosh ibkr_trading_app --eval "db.version()"

# MongoDB Atlas
mongosh "your_connection_string"
```

### Issue 3: No Market Data

**Symptoms:**
- Prices show as 0 or null
- Error: "Market data not subscribed"

**Solutions:**
1. ✅ Check IBKR market data subscriptions
2. ✅ Use delayed data if no subscription
3. ✅ Enable Yahoo Finance fallback
4. ✅ Verify symbols are valid

**Enable Delayed Data:**
- TWS: Edit → Global Configuration → Market Data → Market Data Subscriptions
- Check "US Securities Snapshot and Futures Value Bundle"

### Issue 4: Import Errors

**Symptoms:**
- ModuleNotFoundError
- ImportError

**Solutions:**
1. ✅ Verify virtual environment is activated
2. ✅ Reinstall requirements: `pip install -r requirements.txt`
3. ✅ Check Python version: `python --version`
4. ✅ Clear pip cache: `pip cache purge`

### Issue 5: Port Already in Use

**Symptoms:**
- Error: "Address already in use"

**Solutions:**
```bash
# Find process using port
# Linux/macOS:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /F /PID <PID>  # Windows

# Or use different port
uvicorn main:app --port 8001
```

### Issue 6: Database Permission Denied

**Symptoms:**
- Error: "not authorized" or "permission denied"

**Solutions:**
1. ✅ MongoDB Atlas: create database user
2. ✅ MongoDB Atlas: add IP to whitelist
3. ✅ Local: check file permissions on data directory
4. ✅ Verify credentials in connection string

## Next Steps

After successful setup:

1. ✅ **Review Architecture:** Read `IBKR_TRADING_APP_ARCHITECTURE.md`
2. ✅ **Understand Workflow:** Read `IBKR_TRADING_APP_WORKPLAN.md`
3. ✅ **API Documentation:** Browse `/docs` endpoint
4. ✅ **Add Real Positions:** Sync your actual positions
5. ✅ **Build Watchlist:** Add symbols you're monitoring
6. ✅ **Customize Analysis:** Adjust indicators in `.env`
7. ✅ **Monitor Performance:** Check logs and opportunities

## Production Deployment

For production deployment:

1. ✅ Use production MongoDB (Atlas recommended)
2. ✅ Enable HTTPS with SSL certificates
3. ✅ Set up reverse proxy (Nginx)
4. ✅ Use process manager (systemd, PM2)
5. ✅ Enable authentication
6. ✅ Configure backup strategy
7. ✅ Set up monitoring and alerts
8. ✅ Use environment variables for secrets
9. ✅ Enable rate limiting
10. ✅ Regular security updates

## Support

- 📚 **Documentation:** See `/docs` folder
- 🐛 **Issues:** GitHub Issues
- 📧 **Contact:** [Your contact info]

## Security Checklist

Before going live:

- [ ] Changed default passwords
- [ ] API keys in environment variables
- [ ] .env file in .gitignore
- [ ] HTTPS enabled
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] Error messages don't leak info
- [ ] Logging configured correctly
- [ ] Backup strategy in place

---

**Last Updated:** 2026-02-17  
**Version:** 1.0.0
