# Training with Copilot - Repository

This repository contains two separate applications:

## 1. High School Management System (Original)
Location: `/src/`

A simple FastAPI application for managing extracurricular activities at Mergington High School.

### Features:
- View available activities
- Student registration
- Teacher authentication
- Activity filtering and search

### Quick Start:
```bash
cd src
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Visit: http://localhost:8000

---

## 2. IBKR Trading App (New)
Location: `/src/trading_app/`

A comprehensive trading application that integrates with Interactive Brokers to analyze positions and identify trading opportunities.

### Features:
- 📊 Download positions from IBKR
- 👀 Manage watchlist of potential trades
- 🎯 Get AI-powered buy/sell recommendations
- 📈 Technical analysis (RSI, MACD, Moving Averages)
- 💾 MongoDB database for persistence
- 🖥️ Web-based user interface

### Documentation:
- **Architecture**: [docs/IBKR_TRADING_APP_ARCHITECTURE.md](./docs/IBKR_TRADING_APP_ARCHITECTURE.md)
- **Work Plan**: [docs/IBKR_TRADING_APP_WORKPLAN.md](./docs/IBKR_TRADING_APP_WORKPLAN.md)
- **Setup Guide**: [docs/SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)
- **README**: [docs/IBKR_TRADING_APP_README.md](./docs/IBKR_TRADING_APP_README.md)

### Quick Start:
```bash
cd src/trading_app
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python -m uvicorn main:app --reload
```

### Prerequisites:
- Interactive Brokers account with API access
- TWS or IB Gateway installed and running
- MongoDB (local or Atlas)
- Python 3.11+

### Status:
🚧 **Currently in Development** - Phase 0 (Planning and Architecture)

See [IBKR_TRADING_APP_WORKPLAN.md](./docs/IBKR_TRADING_APP_WORKPLAN.md) for implementation roadmap.

---

## Repository Structure

```
Training-with-copilot/
├── docs/                              # Documentation
│   ├── IBKR_TRADING_APP_ARCHITECTURE.md
│   ├── IBKR_TRADING_APP_WORKPLAN.md
│   ├── IBKR_TRADING_APP_README.md
│   ├── SETUP_GUIDE.md
│   └── how-to-develop.md
├── src/                               # High School Management App
│   ├── app.py
│   ├── backend/
│   ├── static/
│   └── requirements.txt
├── src/trading_app/                   # IBKR Trading App (New)
│   ├── main.py                        # (To be implemented)
│   ├── models/
│   ├── ibkr/
│   ├── analysis/
│   ├── routers/
│   ├── static/
│   ├── requirements.txt
│   └── .env.example
└── README.md                          # This file
```

---

## Getting Started

### For High School Management System:
1. Navigate to `/src`
2. Follow instructions in existing README
3. Start coding!

### For IBKR Trading App:
1. Review the architecture document: [docs/IBKR_TRADING_APP_ARCHITECTURE.md](./docs/IBKR_TRADING_APP_ARCHITECTURE.md)
2. Review the work plan: [docs/IBKR_TRADING_APP_WORKPLAN.md](./docs/IBKR_TRADING_APP_WORKPLAN.md)
3. **Answer the questions in Phase 0** of the work plan
4. Follow setup guide: [docs/SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)
5. Begin implementation according to the work plan

---

## Important Notes

### IBKR Trading App - Phase 0 Questions

Before starting development, please review and answer the critical questions in Phase 0 of the work plan:

1. **IBKR Integration Specifics** - Account type, API access, market data
2. **Analysis Requirements** - Technical indicators, timeframes, scoring
3. **Watchlist Management** - Size, organization, tracking
4. **UI/UX Preferences** - Interface type, real-time requirements
5. **Data & Storage** - Historical data needs, compliance
6. **Future Trading Features** - Timeline and capabilities
7. **Notifications** - Alert preferences

These answers will guide the implementation and ensure the app meets your specific needs.

---

## Contributing

This is a training repository. Feel free to explore and learn!

---

## License

See LICENSE file

---

## Contact

For questions about the IBKR Trading App, please refer to the documentation in the `/docs` folder.

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)
