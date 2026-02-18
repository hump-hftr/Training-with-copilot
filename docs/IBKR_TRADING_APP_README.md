# IBKR Trading App - README

## Overview

A comprehensive trading application that integrates with Interactive Brokers (IBKR) to help you:
- 📊 Download and monitor your current positions
- 👀 Maintain a watchlist of potential trading opportunities
- 🎯 Get actionable buy/sell recommendations based on technical analysis
- 📈 View real-time market data and technical indicators
- 💾 Store all data in a database for future trading app integration

## Key Features

### Current Capabilities (MVP)
- ✅ IBKR position synchronization
- ✅ Watchlist management (add, edit, remove symbols)
- ✅ Technical analysis engine (RSI, MACD, Moving Averages, etc.)
- ✅ Opportunity scoring and ranking
- ✅ Web-based user interface
- ✅ MongoDB database for persistence
- ✅ RESTful API for all operations

### Planned Features
- 🔄 Real-time market data streaming
- 📱 Mobile-responsive design
- 🔔 Alerts and notifications
- 📊 Advanced charting
- 🤖 Automated trading capabilities
- 📉 Portfolio backtesting
- 🔐 Multi-user support

## Architecture Overview

```
Frontend (HTML/JS) → Backend API (FastAPI) → IBKR API + MongoDB
```

For detailed architecture, see [IBKR_TRADING_APP_ARCHITECTURE.md](./IBKR_TRADING_APP_ARCHITECTURE.md)

## Quick Start

### Prerequisites

1. **IBKR Account Setup**
   - Active Interactive Brokers account
   - API access enabled in account settings
   - TWS or IB Gateway installed
   - Paper trading account recommended for testing

2. **Software Requirements**
   - Python 3.11 or higher
   - MongoDB 4.4 or higher
   - Modern web browser

3. **Market Data**
   - IBKR market data subscription (for real-time) OR
   - Use delayed data (free) OR
   - Use Yahoo Finance as fallback

### Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Training-with-copilot
   ```

2. **Set Up Python Environment**
   ```bash
   cd src/trading_app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Start MongoDB**
   ```bash
   # Local installation
   mongod --dbpath /path/to/data
   
   # Or use MongoDB Atlas (cloud)
   # Update MONGODB_URI in .env
   ```

5. **Start TWS/IB Gateway**
   - Launch TWS or IB Gateway
   - Enable API connections (Configuration → API → Settings)
   - Set port to 7497 (paper) or 7496 (live)
   - Enable "ActiveX and Socket Clients"

6. **Initialize Database**
   ```bash
   python scripts/setup_database.py
   ```

7. **Run Application**
   ```bash
   python -m uvicorn main:app --reload
   ```

8. **Access Application**
   - Open browser to http://localhost:8000
   - API docs available at http://localhost:8000/docs

## Usage Guide

### 1. Sync Your Positions
Click "Sync Positions" button or use the API endpoint:
```bash
POST /api/positions/sync
```

### 2. Add Symbols to Watchlist
Enter symbol and details in the Watchlist view:
```bash
POST /api/watchlist
{
  "symbol": "AAPL",
  "notes": "Monitoring for entry",
  "target_price": 200.0
}
```

### 3. Run Analysis
Trigger analysis to generate opportunities:
```bash
POST /api/opportunities/analyze
```

### 4. View Recommendations
Check Dashboard for top buy/sell recommendations sorted by score.

## Configuration

### Environment Variables (.env)

```bash
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=ibkr_trading_app

# IBKR Configuration
IBKR_HOST=127.0.0.1
IBKR_PORT=7497          # 7497 for paper, 7496 for live
IBKR_CLIENT_ID=1
IBKR_ACCOUNT_ID=DU12345  # Your IBKR account ID

# Application Settings
REFRESH_INTERVAL=300     # Seconds between auto-refresh
LOG_LEVEL=INFO

# Analysis Settings
RSI_PERIOD=14
RSI_OVERSOLD=30
RSI_OVERBOUGHT=70
MACD_FAST=12
MACD_SLOW=26
MACD_SIGNAL=9
SMA_SHORT=50
SMA_LONG=200

# Optional: Market Data Fallback
ALPHA_VANTAGE_API_KEY=your_key_here
```

### User Settings (via API)

```json
{
  "refresh_interval": 300,
  "risk_tolerance": "moderate",
  "notification_preferences": {
    "email": true,
    "threshold_pnl": 5.0
  },
  "trading_preferences": {
    "auto_refresh": true
  }
}
```

## API Documentation

Full API documentation available at: http://localhost:8000/docs

### Key Endpoints

**Positions**
- `GET /api/positions` - List all positions
- `POST /api/positions/sync` - Sync from IBKR

**Watchlist**
- `GET /api/watchlist` - List watchlist
- `POST /api/watchlist` - Add symbol
- `PUT /api/watchlist/{symbol}` - Update
- `DELETE /api/watchlist/{symbol}` - Remove

**Opportunities**
- `GET /api/opportunities` - All opportunities
- `GET /api/opportunities/top?limit=5&action=buy` - Top recommendations

**Market Data**
- `GET /api/market/{symbol}` - Current data
- `GET /api/market/{symbol}/indicators` - Technical indicators

## Technical Analysis

### Indicators Calculated
- **RSI (Relative Strength Index)** - Momentum oscillator
- **MACD** - Trend-following momentum indicator
- **SMA 50/200** - Simple moving averages
- **Volume Ratio** - Volume vs. average
- **Price vs MA** - Price relative to moving averages

### Scoring Algorithm

Opportunities are scored 0-10 based on:
- Technical indicators (40%)
- Momentum signals (30%)
- Volume analysis (15%)
- Price action patterns (15%)

**Buy Signal Example:**
- RSI < 30 (oversold)
- MACD bullish crossover
- Volume above average
- Price above 200-day MA

**Sell Signal Example:**
- RSI > 70 (overbought)
- MACD bearish crossover
- Position with significant gains
- Price at resistance

## Project Structure

```
src/trading_app/
├── main.py                 # FastAPI application
├── config.py              # Configuration
├── database.py            # MongoDB setup
├── models/                # Data models
├── ibkr/                  # IBKR integration
├── analysis/              # Analysis engine
├── routers/               # API endpoints
├── static/                # Frontend files
└── utils/                 # Utilities

docs/
├── IBKR_TRADING_APP_ARCHITECTURE.md
├── IBKR_TRADING_APP_WORKPLAN.md
└── SETUP_GUIDE.md

scripts/
├── setup_database.py
├── sync_positions.py
└── run_analysis.py
```

## Troubleshooting

### IBKR Connection Issues

**Problem:** Cannot connect to TWS/Gateway
- Verify TWS/Gateway is running
- Check port configuration (7497 for paper)
- Enable API in TWS: Configuration → API → Settings
- Check firewall settings

**Problem:** "Already connected" error
- Restart TWS/Gateway
- Change CLIENT_ID in .env
- Check for other apps using the connection

### Database Issues

**Problem:** MongoDB connection failed
- Verify MongoDB is running: `mongo --eval "db.version()"`
- Check MONGODB_URI in .env
- Ensure database name doesn't have spaces

### Market Data Issues

**Problem:** No price updates
- Check IBKR market data subscriptions
- Verify delayed data settings
- Fall back to Yahoo Finance if needed

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
# Format code
black src/

# Lint
flake8 src/
```

### Database Shell
```bash
# Access MongoDB
mongo ibkr_trading_app

# Show collections
show collections

# Query positions
db.positions.find().pretty()
```

## Security Considerations

⚠️ **Important Security Notes:**
- Never commit .env file with credentials
- Use environment variables for all secrets
- Enable HTTPS in production
- Implement authentication for multi-user deployments
- Regularly update dependencies
- Use paper trading account for testing
- Monitor API rate limits

## Contributing

This is currently a personal project. Future contributions may be accepted.

## License

[Specify License]

## Disclaimer

⚠️ **IMPORTANT DISCLAIMER:**
This software is for educational and informational purposes only. 
- Not financial advice
- No guarantee of accuracy or profitability
- Trading involves substantial risk
- Test thoroughly with paper trading
- Author not responsible for trading losses
- Always do your own research

## Support & Contact

- Issues: [GitHub Issues]
- Documentation: See `/docs` folder
- API Docs: http://localhost:8000/docs

## Roadmap

### Phase 1 (Current) - MVP
- [x] Architecture design
- [x] Work plan creation
- [ ] Database implementation
- [ ] IBKR integration
- [ ] Analysis engine
- [ ] Basic UI

### Phase 2 - Enhanced Features
- [ ] Real-time updates
- [ ] Advanced charting
- [ ] Alerts system
- [ ] Mobile responsive design

### Phase 3 - Trading Capabilities
- [ ] Order placement
- [ ] Order management
- [ ] Position sizing calculator
- [ ] Risk management tools

### Phase 4 - Advanced Features
- [ ] Backtesting engine
- [ ] Portfolio optimization
- [ ] Machine learning predictions
- [ ] Multi-account support

## Acknowledgments

- **ib_insync** - Excellent IBKR API wrapper
- **FastAPI** - Modern, fast web framework
- **MongoDB** - Flexible document database
- **pandas-ta** - Technical analysis library

## References

- [IBKR API Documentation](https://interactivebrokers.github.io/tws-api/)
- [ib_insync Documentation](https://ib-insync.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Technical Analysis on Investopedia](https://www.investopedia.com/technical-analysis-4689657)

---

**Version:** 1.0.0-alpha  
**Last Updated:** 2026-02-17  
**Status:** In Development
