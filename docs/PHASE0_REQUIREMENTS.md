# Phase 0 Requirements - User Responses

**Date:** 2026-02-17  
**Status:** Requirements Gathered  

This document captures the user's answers to the Phase 0 discovery questions.

---

## 1. IBKR Integration Specifics

### Account Type
- **Answer:** Paper trading account
- **Status:** Confirmed

### Trading Platform
- **Answer:** Trader Workstation (TWS) - already configured
- **Status:** Ready to use

### Market Data
- **Answer:** Currently using delayed data for mockup work
- **Real-time:** Not required initially
- **Status:** Delayed data sufficient

### Markets
- **Answer:** US NASDAQ (primarily) and TSE (Toronto Stock Exchange)
- **Status:** Multi-exchange support needed

---

## 2. Analysis & Scoring Requirements

### Technical Indicators (Priority)
- **Primary Focus:** 
  - Moving average crossovers
  - OHLC (Open, High, Low, Close) patterns
  - Volume trends
  - Double and triple bottoms/tops
  - Breakout detection
- **Timeframe:** 5-minute OHLC bars
- **Moving Averages:** 50-day and 200-day MA for long-term holds (configurable for shorter-term trends)
- **Bollinger Bands:** Confirmed as useful

**Note:** "We won't code this yet. Future TBD" - Start simple, add complexity later

### Trading Timeframe
- **Primary:** 5-minute OHLC bars
- **Strategy:** Trade on breakout detection
- **Entry:** Limit buy with trailing stop
- **Exit:** Limit sell, Market sell
- **Stop Loss:** Required on all trades
- **Trading Hours:** Market hours only (no pre-market or after-hours trading)

### Trend Analysis
- **Mix of:**
  - Short to medium-term trends
  - Sentiment indicators
  - Breaking news with price increases before market open
- **Restriction:** No trades outside market hours

### Opportunity Scoring/Triggering
- **Manual Phase:** Run on command prior to full automation
- **Future Automation:** Daily trigger to run prior to market open to scan trade opportunities
- **Trigger Combination:**
  - Technical indicators (price and volume)
  - News flow
  - Social sentiment
- **Portfolio Management:** Position sizing rules with trailing stop orders (future TBD)

---

## 3. Watchlist Management

### Size
- **Active Holdings:** Maximum 10 positions
- **Watchlist:** 5-10 additional symbols for tracking
- **Total:** ~15-20 symbols maximum

### Organization
- **Preference:** No firm views
- **Agent Recommendation:** Flexible system supporting tags/categories

### Data to Track Per Symbol
- **Required Fields:**
  - Symbol
  - Exchange
  - Contract ID
  - Market capitalization
  - Industry
  - ACB (Adjusted Cost Base)
  - Profit/Loss
  - Dates (acquisition, last trade, etc.)
- **Holdings Data:** Whatever needed to understand positions fully

---

## 4. UI/UX Requirements

### Interface Preference
- **Guidance Needed:** User open to agent recommendations
- **No strong preference stated**

### Real-time vs Periodic Updates
- **Open Orders (Active Trades):** Asynchronous updates from TWS (real-time)
- **Portfolio Positions:** Lower frequency (15 seconds to 1 minute) or manual screen refresh
- **Approach:** Real-time for active trading, periodic for positions

### Most Important Views
1. **Portfolio Holdings** - Current positions with P&L
2. **Open Orders** - Active trades in progress
3. **Activity Log** - Trade history and significant events
4. **Watchlist View** - With indicators and editing capability

**Priority Order:** Holdings → Orders → Log → Watchlist

---

## 5. Data & Storage Requirements

### Historical Data Needs
- **Current Phase:** Logging only (permanent trade logs)
- **Future ML Phase:** 
  - 2 years of historical data per tracked symbol
  - 5-minute bar data (OHLC + Volume)
  - Separate database structure for ML training
- **Status:** Current needs are minimal, plan for future expansion

### Track Closed Positions
- **Answer:** Logging only (all trades logged permanently)
- **No need for active closed position tracking in main database**

### Compliance Requirements
- **Answer:** No specific compliance requirements stated
- **Assumption:** Personal use, standard data protection

---

## 6. Future Trading Features

### Timeline for Trading Capabilities
- **Answer:** Depends on success of initial stages - likely months
- **Approach:** Incremental rollout based on validation

### Order Types Needed
- **Confirmed Requirements:**
  - Limit buy with trailing stop
  - Limit sell
  - Market sell
  - Short sales (to be considered)
  - **Kill switch:** Close all positions (emergency exit)
- **Priority:** Entry orders with stops, then sell orders, then advanced features

---

## 7. Notifications & Alerts

### Alert Preferences
- **Current Phase:** Screen logging and file logging
- **Trade Events:** Logged to screen and file
- **Significant Events:** Logged to screen and file
- **Future:** Notifications to be added later
- **Status:** Logging first, notifications later

### Alert Channels
- **Answer:** Future discussion
- **Current:** Not required for MVP

### Alert Triggers
- **Daily Pre-Market:** Run analysis before market open
- **Trade Alerts:** Triggered by combination of:
  - Technical indicators (price and volume)
  - News flow
  - Social sentiment

---

## 8. Database Preference

### User Preference
- **Concern:** MongoDB is text-based for legibility
- **Alternative Requested:** SQLite
- **Reasoning:** 
  - Reasonably efficient
  - Simple to use
  - Good for small dataset (10 positions, 5-10 watchlist)
  
### Future Considerations
- **ML Historical Database:** Will need separate structure
- **Could get large:** Different database approach may be needed
- **Recommendation:** SQLite for current app, evaluate TimescaleDB/PostgreSQL for ML phase

---

## Requirements Summary

### Must Have (MVP)
1. ✅ Paper trading account integration (TWS)
2. ✅ 5-minute OHLC bar data
3. ✅ Breakout detection
4. ✅ Moving average crossovers
5. ✅ Entry with trailing stop
6. ✅ Portfolio holdings view
7. ✅ Open orders tracking
8. ✅ Activity log (permanent)
9. ✅ Watchlist (5-10 symbols)
10. ✅ Max 10 active positions
11. ✅ US NASDAQ + TSE support
12. ✅ Market hours only trading
13. ✅ SQLite database

### Should Have (Phase 2)
1. Daily pre-market scan automation
2. News flow integration
3. Social sentiment indicators
4. Position sizing rules
5. Enhanced UI

### Could Have (Future)
1. Machine learning predictions
2. 2 years historical data (5-min bars)
3. Real-time market data
4. Email/SMS notifications
5. Short selling
6. Advanced order types
7. Multiple timeframe analysis

---

## Technical Specifications Based on Requirements

### Data Collection
- **Frequency:** 5-minute bars
- **Fields:** OHLC + Volume
- **Markets:** NASDAQ, TSE
- **Storage:** SQLite (main), separate DB for ML history

### Analysis Engine
- **Indicators:**
  - Moving averages (50-day, 200-day, configurable)
  - Volume analysis
  - Pattern detection (double/triple tops/bottoms)
  - Breakout detection
- **Update Frequency:** 
  - Active trades: Real-time
  - Positions: 15s - 1min
  - Pre-market scan: Daily

### Order Management
- **Entry:** Limit buy + trailing stop
- **Exit:** Limit sell, market sell
- **Risk Management:** Stop loss required
- **Emergency:** Kill switch for all positions

### Logging
- **Destinations:** Screen + File
- **Events:** All trades, significant events
- **Retention:** Permanent
- **Format:** Structured for future ML use

---

## Architecture Adjustments Needed

Based on user feedback, the following adjustments should be made to the original architecture:

1. **Database:** Change from MongoDB to SQLite
2. **Timeframe:** Focus on 5-minute bars (not daily)
3. **Scale:** Small dataset (10 positions max)
4. **Updates:** Hybrid approach (real-time for orders, periodic for positions)
5. **Simplicity:** Start simple, add complexity incrementally
6. **Markets:** Multi-exchange support (NASDAQ, TSE)

---

## Next Steps

1. ✅ User review and approval of requirements
2. 🔄 Update architecture document for SQLite
3. 🔄 Adjust database schema for 5-minute bars
4. 🔄 Design breakout detection algorithm
5. 🔄 Create kill switch specification
6. 🔄 Plan multi-exchange support
7. 🚀 Begin Phase 1 implementation

---

**Status:** Requirements Gathered - Ready for Architecture Update  
**Blocking Items:** None - Can proceed with updated architecture  
**Risk Level:** Low (clear requirements, realistic scope)
