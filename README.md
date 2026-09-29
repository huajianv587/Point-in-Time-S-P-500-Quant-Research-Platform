# S&P 500 Multi-Factor Quantitative Research Platform

> A private, research-oriented quantitative investment platform for systematic multi-factor analysis of S&P 500 constituents.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Private-red)](LICENSE)

---

## 📖 Overview

This platform combines **multi-source market data**, **factor-based signal generation**, **portfolio optimization**, and **backtesting** into a unified research terminal for quantitative investment strategies. Built with modern Python and FastAPI, it emphasizes point-in-time data integrity, modular architecture, and reproducible research workflows.

**Key Capabilities:**
- 📊 **Multi-Factor Analysis**: Value, Quality, Momentum, Volatility, Sentiment, ESG
- 🎯 **Signal Generation**: IC/RankIC validation, alpha ranking, confidence scoring
- 💼 **Portfolio Construction**: Mean-variance optimization with sector constraints and risk controls
- ⏱️ **Backtesting Engine**: Daily rebalancing simulation with transaction cost modeling
- 📈 **Paper Trading**: Alpaca integration for strategy validation
- 🤖 **AI Research Agent**: LLM-powered factor discovery and risk analysis using RAG
- 🔄 **Real-time Data**: Alpaca API, yfinance with SQLite caching

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │  Landing    │  │   Control    │  │   API Docs       │      │
│  │  Page (/)   │  │Console (/app)│  │   (/docs)        │      │
│  └─────────────┘  └──────────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (FastAPI)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /api/v1/quant/*    │ /api/v1/agent/*  │ /api/v1/rl/*    │  │
│  │ Platform, Research │ AI Assistant     │ Reinforcement   │  │
│  │ Backtest, Trading  │ RAG Integration  │ Learning Exp    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Quantitative System Service                 │
│                                                                 │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Market Data    │  │  Factor Engine   │  │  Portfolio   │ │
│  │  Gateway        │  │                  │  │  Optimizer   │ │
│  │                 │  │  • Value         │  │              │ │
│  │  • Alpaca API   │  │  • Quality       │  │  • Mean-Var  │ │
│  │  • yfinance     │  │  • Momentum      │  │  • Risk Ctrl │ │
│  │  • SQLite Cache │  │  • Volatility    │  │  • Sector    │ │
│  │                 │  │  • Sentiment     │  │    Constraints│ │
│  │  Point-in-Time  │  │  • ESG (opt)     │  │              │ │
│  │  Integrity      │  │                  │  │              │ │
│  └─────────────────┘  │  IC/RankIC Valid │  └──────────────┘ │
│                       └──────────────────┘                     │
│                                                                 │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Backtest       │  │  Risk Monitor    │  │  AI Agent    │ │
│  │  Engine         │  │                  │  │  (RAG)       │ │
│  │                 │  │  • Sharpe Ratio  │  │              │ │
│  │  • Daily Rebal  │  │  • Max Drawdown  │  │  • Factor    │ │
│  │  • Txn Costs    │  │  • CVaR          │  │    Discovery │ │
│  │  • Slippage     │  │  • Exposure      │  │  • Risk      │ │
│  │  • P&L Track    │  │  • Concentration │  │    Analysis  │ │
│  │                 │  │                  │  │  • Research  │ │
│  └─────────────────┘  └──────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Storage Layer                            │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────────┐    │
│  │   SQLite     │  │  Supabase   │  │  Cloudflare R2     │    │
│  │   (Cache)    │  │  (Metadata) │  │  (Artifacts)       │    │
│  └──────────────┘  └─────────────┘  └────────────────────┘    │
│                                                                 │
│  Local Fallback: storage/quant/                                │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Market Data Ingestion
   ├─ Alpaca API (real-time bars)
   ├─ yfinance (historical data)
   └─ SQLite cache (point-in-time snapshots)

2. Factor Calculation
   ├─ Value: P/E, P/B, Dividend Yield
   ├─ Quality: ROE, Profit Margins
   ├─ Momentum: 20/60 day trends
   ├─ Volatility: Realized vol, Beta
   ├─ Sentiment: News, Analyst ratings
   └─ ESG: Optional factor scores

3. Signal Generation
   ├─ Alpha Ranker (IC/RankIC validation)
   ├─ Confidence scoring
   └─ Expected return estimation

4. Portfolio Construction
   ├─ Mean-variance optimization
   ├─ Sector constraints
   ├─ Position limits
   └─ Risk budgeting

5. Execution Simulation
   ├─ Backtest engine (daily rebalancing)
   ├─ Transaction cost modeling
   ├─ Paper trading (Alpaca)
   └─ Performance attribution
```

---

## 📂 Project Structure

```
.
├── gateway/                 # FastAPI application
│   ├── api/                # API routes
│   │   ├── routers/       # Endpoint handlers
│   │   └── factory.py     # App factory
│   ├── quant/             # Quantitative system
│   │   ├── service.py     # Core quant service
│   │   ├── market_data.py # Data gateway
│   │   ├── signals.py     # Signal engine
│   │   ├── alpha_ranker.py # Alpha ranking
│   │   └── models.py      # Data models
│   ├── agents/            # AI research agents
│   └── config.py          # Configuration
│
├── dist/                   # Frontend static files
│   ├── index.html         # Landing page
│   └── app/               # Control console
│
├── scripts/               # Utility scripts
│   └── import_sp500_universe.py  # Universe import
│
├── tests/                 # Test suite
│   ├── test_api_contracts.py
│   ├── test_quant_api.py
│   └── test_frontend_click_contracts.py
│
├── storage/               # Local storage
│   └── quant/
│       ├── market_data/   # SQLite cache
│       └── backtests/     # Backtest results
│
├── docs/                  # Documentation
│   ├── FINAL_STATUS.md           # Project status
│   ├── RESUME_DESCRIPTION.md     # Resume guide
│   ├── QUICK_START.md            # Getting started
│   └── ISSUES_AND_FIXES.md       # Known issues
│
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.10 or higher (required for modern type annotations)
- **pip**: Latest version
- **Git**: For cloning the repository

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Point-in-Time-S-P-500-Quant-Research-Platform-main

# Install dependencies
pip install -r requirements.txt

# Copy environment template (optional)
cp .env.example .env
# Edit .env to add API keys if available
```

### Running the Platform

```bash
# Start the FastAPI server
python -m uvicorn gateway.main:app --host 0.0.0.0 --port 8000

# Server will start at http://localhost:8000
```

### Accessing the Platform

| Interface | URL | Description |
|-----------|-----|-------------|
| **Landing Page** | http://localhost:8000/ | Product overview |
| **Control Console** | http://localhost:8000/app/ | Research terminal |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs |
| **Platform Overview** | http://localhost:8000/api/v1/quant/platform/overview | System status JSON |

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_api_contracts.py -v
python -m pytest tests/test_quant_api.py -v

# Run with coverage
python -m pytest tests/ --cov=gateway --cov-report=html
```

---

## ⚙️ Configuration

The platform can run in **local fallback mode** with minimal configuration. API keys are optional.

### Essential Configuration

Edit `.env` file:

```bash
# Core settings
APP_MODE=local
DEBUG=true
QUANT_DEFAULT_CAPITAL=1000000
QUANT_DEFAULT_UNIVERSE=SP500

# Market data (optional - uses yfinance fallback)
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here

# LLM for AI agent (optional)
OPENAI_API_KEY=your_key_here
# or
ANTHROPIC_API_KEY=your_key_here
```

### Universe Data Import

```bash
# Import S&P 500 constituents from CSV
python scripts/import_sp500_universe.py sp500.csv --snapshot-date 2024-12-31

# CSV format:
# symbol,company_name,sector,industry,weight
# AAPL,Apple Inc.,Technology,Consumer Electronics,0.068
# MSFT,Microsoft Corporation,Technology,Software,0.072
```

---

## 📊 Features

### Multi-Factor Analysis
- **Value Factors**: P/E, P/B, Dividend Yield, FCF Yield
- **Quality Factors**: ROE, ROIC, Profit Margins, Asset Turnover
- **Momentum Factors**: Price trends, Relative strength, Volume
- **Volatility Factors**: Realized volatility, Beta, Downside deviation
- **Sentiment Factors**: News sentiment, Analyst ratings, Social media
- **ESG Factors**: Environmental, Social, Governance scores (optional)

### Signal Validation
- Information Coefficient (IC) and Rank IC computation
- Factor correlation analysis
- Leakage detection
- Transaction cost impact modeling

### Portfolio Optimization
- Mean-variance optimization
- Sector neutrality constraints
- Position size limits
- Risk budgeting (CVaR, tracking error)
- Maximum drawdown controls

### Backtesting
- Daily rebalancing simulation
- Transaction cost modeling (commissions + slippage)
- Point-in-time data integrity
- Performance attribution
- Risk metrics (Sharpe, Sortino, Calmar, Max DD)

### AI Research Assistant
- LLM-powered factor discovery
- RAG (Retrieval-Augmented Generation) for research notes
- Natural language risk analysis
- Strategy explanation and debugging

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | FastAPI | REST API framework |
| **Language** | Python 3.10+ | Core implementation |
| **Data Science** | pandas, numpy | Data processing |
| **Optimization** | scipy, cvxpy | Portfolio optimization |
| **Market Data** | Alpaca API, yfinance | Real-time & historical data |
| **Database** | SQLite | Local caching |
| **Cloud (optional)** | Supabase, Cloudflare R2 | Metadata & artifacts |
| **AI** | OpenAI/Anthropic | LLM research agent |
| **Frontend** | Vanilla JS, HTML/CSS | Control console |
| **Visualization** | Chart.js, ECharts | Charts & graphs |

---

## 📈 Usage Examples

### Research Workflow

```python
# 1. Get platform status
GET /api/v1/quant/platform/overview

# 2. Run factor research
POST /api/v1/quant/research/run
{
  "universe": ["AAPL", "MSFT", "GOOGL"],
  "factors": ["value", "momentum", "quality"]
}

# 3. Backtest strategy
POST /api/v1/quant/backtests/run
{
  "strategy_name": "multi_factor",
  "capital_base": 1000000,
  "lookback_days": 90
}

# 4. Get backtest results
GET /api/v1/quant/backtests/{backtest_id}
```

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Run a backtest
response = requests.post(
    f"{BASE_URL}/api/v1/quant/backtests/run",
    json={
        "strategy_name": "momentum_cross",
        "universe": None,  # Uses default SP500
        "capital_base": 1_000_000,
        "lookback_days": 90
    }
)

result = response.json()
print(f"Sharpe Ratio: {result['sharpe']:.2f}")
print(f"Total Return: {result['total_return']:.2%}")
print(f"Max Drawdown: {result['max_drawdown']:.2%}")
```

---

## ⚠️ Limitations & Disclaimers

### Current Limitations
- **Universe Size**: Demo uses ~26 stocks; full S&P 500 requires CSV import
- **Project Status**: Research prototype, not production-ready
- **Data Sources**: Free APIs (Alpaca, yfinance); institutional data requires paid subscriptions
- **Python Version**: Requires 3.10+ due to modern type annotations

### Disclaimers
- **Not Financial Advice**: This is an educational/research platform
- **No Real Trading**: Paper trading only; no real money execution
- **Backtest Results**: Historical simulations do not guarantee future performance
- **Data Quality**: Free data sources may have gaps or delays

---

## 📚 Documentation

- **[FINAL_STATUS.md](FINAL_STATUS.md)** - Complete project status and summary
- **[RESUME_DESCRIPTION.md](RESUME_DESCRIPTION.md)** - How to present this project on your resume
- **[QUICK_START.md](QUICK_START.md)** - Detailed getting started guide
- **[ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md)** - Known issues and solutions

---

## 🤝 Contributing

This is a private research project. For improvements or suggestions, please reach out directly.

---

## 📄 License

Private - All Rights Reserved

---

## 🙏 Acknowledgments

- **Data Sources**: Alpaca Markets, Yahoo Finance
- **Frameworks**: FastAPI, pandas, numpy, scipy
- **Inspiration**: Quantopian, QuantConnect, Lean Algorithm Framework

---

## 📞 Contact

For questions about this project or collaboration opportunities, please contact via [your contact method].

---

**Last Updated**: September 2024  
**Python Version**: 3.10+  
**Status**: Research Prototype - Portfolio Ready
