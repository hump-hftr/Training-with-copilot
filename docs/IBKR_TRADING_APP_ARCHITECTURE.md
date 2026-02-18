# IBKR Trading App Architecture

## Overview
A comprehensive trading application that integrates with Interactive Brokers (IBKR) to download positions, analyze trading opportunities, manage a watchlist of potential investments, and provide actionable buy/sell recommendations.

## System Architecture

### 1. Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend Layer                        │
│  (HTML/CSS/JavaScript - React or Vanilla JS)           │
│  - Dashboard View                                       │
│  - Positions View                                       │
│  - Watchlist Management                                 │
│  - Trade Recommendations View                           │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Backend API Layer                      │
│             (FastAPI - Python)                          │
│  - Position Management Endpoints                        │
│  - Watchlist CRUD Operations                            │
│  - Analysis & Recommendation Engine                     │
│  - Authentication & Authorization                       │
└─────────────────────────────────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   IBKR Integration       │  │   Database Layer         │
│     Module               │  │     (MongoDB)            │
│  - API Connection        │  │  - Positions Collection  │
│  - Position Download     │  │  - Watchlist Collection  │
│  - Market Data Fetch     │  │  - Opportunities Coll.   │
│  - Order Management      │  │  - Historical Data Coll. │
└──────────────────────────┘  └──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              External Services                          │
│  - IBKR TWS/IB Gateway                                 │
│  - Market Data Provider (Yahoo Finance/Alpha Vantage)  │
│  - Technical Analysis Libraries                         │
└─────────────────────────────────────────────────────────┘
```

### 2. Database Schema

#### Collections

**positions**
```json
{
  "_id": "ObjectId",
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "quantity": 100,
  "avg_cost": 150.25,
  "current_price": 175.50,
  "market_value": 17550.00,
  "unrealized_pnl": 2525.00,
  "unrealized_pnl_pct": 16.82,
  "sector": "Technology",
  "last_updated": "2026-02-17T01:23:00Z",
  "source": "ibkr",
  "account_id": "U1234567"
}
```

**watchlist**
```json
{
  "_id": "ObjectId",
  "symbol": "MSFT",
  "name": "Microsoft Corporation",
  "added_date": "2026-02-15T10:00:00Z",
  "notes": "Strong cloud growth, monitoring for entry",
  "target_price": 400.00,
  "stop_loss": 350.00,
  "tags": ["tech", "cloud", "growth"],
  "status": "monitoring"
}
```

**opportunities**
```json
{
  "_id": "ObjectId",
  "symbol": "AAPL",
  "type": "position",  // or "watchlist"
  "action": "buy",  // or "sell"
  "score": 8.5,  // 0-10 rating
  "current_price": 175.50,
  "target_price": 200.00,
  "stop_loss": 165.00,
  "reasoning": [
    "RSI oversold at 28",
    "Strong support at $170",
    "Earnings beat expected"
  ],
  "indicators": {
    "rsi": 28.5,
    "macd": -1.2,
    "volume_ratio": 1.5,
    "price_vs_ma50": 0.95,
    "price_vs_ma200": 1.10
  },
  "generated_at": "2026-02-17T01:23:00Z",
  "expiry": "2026-02-18T01:23:00Z"
}
```

**market_data**
```json
{
  "_id": "ObjectId",
  "symbol": "AAPL",
  "timestamp": "2026-02-17T01:23:00Z",
  "open": 174.50,
  "high": 176.80,
  "low": 173.20,
  "close": 175.50,
  "volume": 52000000,
  "indicators": {
    "sma_50": 170.25,
    "sma_200": 159.80,
    "rsi_14": 58.3,
    "macd": 2.15,
    "macd_signal": 1.85
  }
}
```

**user_settings**
```json
{
  "_id": "ObjectId",
  "user_id": "user123",
  "ibkr_account_id": "U1234567",
  "refresh_interval": 300,  // seconds
  "risk_tolerance": "moderate",  // conservative, moderate, aggressive
  "notification_preferences": {
    "email": true,
    "threshold_pnl": 5.0  // notify when position moves >5%
  },
  "trading_preferences": {
    "auto_refresh": true,
    "show_extended_hours": false
  }
}
```

### 3. Backend API Endpoints

#### Position Management
- `GET /api/positions` - Get all current positions
- `GET /api/positions/{symbol}` - Get specific position details
- `POST /api/positions/sync` - Sync positions from IBKR
- `GET /api/positions/summary` - Get portfolio summary

#### Watchlist Management
- `GET /api/watchlist` - Get all watchlist items
- `POST /api/watchlist` - Add symbol to watchlist
- `PUT /api/watchlist/{symbol}` - Update watchlist item
- `DELETE /api/watchlist/{symbol}` - Remove from watchlist
- `GET /api/watchlist/{symbol}` - Get specific watchlist item details

#### Trading Opportunities
- `GET /api/opportunities` - Get all trading opportunities (sorted by score)
- `GET /api/opportunities/top` - Get top N buy/sell recommendations
- `POST /api/opportunities/analyze` - Trigger analysis for all symbols
- `GET /api/opportunities/{symbol}` - Get opportunities for specific symbol

#### Market Data
- `GET /api/market/{symbol}` - Get current market data for symbol
- `GET /api/market/{symbol}/history` - Get historical data
- `GET /api/market/{symbol}/indicators` - Get technical indicators

#### Configuration
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update user settings
- `POST /api/ibkr/connect` - Test IBKR connection

### 4. Frontend Components

#### Main Dashboard
- Portfolio summary (total value, P&L, allocation)
- Top 5 buy recommendations
- Top 5 sell recommendations
- Recent activity feed

#### Positions View
- Table of all current positions
- Sortable columns (symbol, quantity, P&L, etc.)
- Individual position cards with details
- Real-time price updates

#### Watchlist View
- List of monitored symbols
- Add/edit/remove functionality
- Quick view of current prices and indicators
- Notes and target prices per symbol

#### Opportunities View
- Unified view of buy/sell recommendations
- Filterable by action type, score, symbol
- Detailed reasoning for each opportunity
- Technical indicator charts

### 5. IBKR Integration Module

#### Components
1. **Connection Manager**
   - TWS/Gateway connection handling
   - Connection state management
   - Automatic reconnection

2. **Position Downloader**
   - Fetch all account positions
   - Parse and normalize data
   - Update database

3. **Market Data Handler**
   - Subscribe to market data
   - Real-time price updates
   - Historical data retrieval

4. **Order Management** (Future)
   - Place orders
   - Monitor order status
   - Manage open orders

### 6. Analysis Engine

#### Technical Analysis Module
- Calculate key indicators (RSI, MACD, Moving Averages, Bollinger Bands)
- Identify support/resistance levels
- Detect chart patterns

#### Scoring Algorithm
```python
def calculate_opportunity_score(symbol_data):
    """
    Score: 0-10 scale
    Factors:
    - Technical indicators (40%)
    - Momentum signals (30%)
    - Volume analysis (15%)
    - Price action patterns (15%)
    """
    score = 0
    
    # RSI scoring (0-40% of score)
    if rsi < 30: score += 4.0  # oversold
    elif rsi > 70: score += 4.0  # overbought for sell
    else: score += (50 - abs(rsi - 50)) / 12.5
    
    # MACD scoring (0-30% of score)
    if macd_crossover: score += 3.0
    
    # Volume scoring (0-15% of score)
    if volume_ratio > 1.5: score += 1.5
    
    # Price vs MA scoring (0-15% of score)
    if price_above_ma50 and price_above_ma200: score += 1.5
    
    return min(score, 10.0)
```

### 7. Technology Stack

**Backend:**
- Python 3.11+
- FastAPI (Web framework)
- pymongo (MongoDB driver)
- ib_insync (IBKR API wrapper)
- pandas (Data manipulation)
- ta-lib or pandas-ta (Technical analysis)
- yfinance (Market data backup)

**Frontend:**
- HTML5/CSS3/JavaScript
- Option: React.js or Vue.js for SPA
- Chart.js or TradingView Lightweight Charts
- Tailwind CSS or Bootstrap

**Database:**
- MongoDB (Document store for flexible schema)

**External Services:**
- IBKR TWS or IB Gateway
- Optional: Alpha Vantage or Yahoo Finance API

### 8. Security Considerations

- Store IBKR credentials securely (encrypted)
- Use environment variables for sensitive data
- Implement rate limiting on API endpoints
- Add authentication/authorization for multi-user support
- Use HTTPS for all communications
- Implement session management
- Add CORS protection

### 9. Deployment Architecture

**Development:**
- Local MongoDB instance
- Local TWS/Gateway connection
- FastAPI development server

**Production:**
- MongoDB Atlas or managed MongoDB
- TWS Gateway on VPS/Cloud
- FastAPI with Gunicorn/Uvicorn
- Nginx reverse proxy
- Optional: Docker containers

## Summary

This architecture provides a scalable, maintainable foundation for the IBKR trading app with:
- Clear separation of concerns
- Extensible design for future features
- Real-time data processing capabilities
- Flexible analysis engine
- User-friendly interface
- Database designed for trading analytics
