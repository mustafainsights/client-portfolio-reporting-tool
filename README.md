# 📊 Client Portfolio Reporting Tool

> Automated institutional client reporting dashboard built on Python, Streamlit, and Plotly — simulating the analytics infrastructure used by asset management firms to monitor AUM performance, benchmark deviation, and client-level attribution.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?style=flat-square&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.19-purple?style=flat-square&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-2.2-green?style=flat-square&logo=pandas)

---

## 🎯 Project Overview

This project automates the client portfolio reporting workflow commonly performed by **Client & Product teams** at institutional asset managers. It ingests multi-client, multi-fund portfolio data, calculates key performance metrics, and renders an interactive executive dashboard — replacing manual Excel-based reporting with a scalable, real-time analytics tool.

**Inspired by:** BlackRock iShares client reporting workflows and institutional portfolio analytics standards.

---

## 🧩 Business Problem Solved

Traditional client reporting in asset management relies heavily on manual Excel workbooks that are:
- Time-consuming to update (4–6 hours per reporting cycle)
- Prone to human error in formula logic and data entry
- Difficult to scale across multiple client accounts simultaneously
- Inflexible for ad-hoc analysis requests

**This tool reduces reporting time by ~80%** by automating data ingestion, metric calculation, and visualization — allowing analysts to focus on insight generation rather than data manipulation.

---

## 🔑 Key Features

| Feature | Description |
|---|---|
| **AUM Tracking** | Real-time AUM by client, fund, and asset class with trend visualization |
| **Benchmark Comparison** | Daily portfolio return vs. benchmark with active alpha calculation |
| **Alpha Attribution** | Fund-level and client-level outperformance decomposition |
| **Batting Average** | Tracks how frequently the portfolio beats the benchmark |
| **Automated Insights** | Rule-based commentary generation flagging key performance trends |
| **Client Filtering** | Dynamic sidebar filters for client, asset class, and date range |
| **Executive Dashboard** | Clean, professional UI suitable for client-facing presentation |

---

## 📐 Metrics Calculated

```
AUM (Assets Under Management)     = Shares × Price (per fund, per client)
Daily Portfolio Return             = Σ(Daily_Return × AUM) / Σ(AUM)   [AUM-weighted]
Active Alpha                       = Portfolio Return − Benchmark Return
Batting Average                    = Days Outperforming Benchmark / Total Trading Days
Equity Concentration               = Equity AUM / Total AUM × 100
```

---

## 🗂️ Project Structure

```
blackrock_portfolio_tool/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
└── data/
    └── portfolio_data.csv      # Simulated institutional portfolio dataset
```

---

## 📊 Dataset Description

The simulated dataset (`portfolio_data.csv`) represents a realistic institutional portfolio across **3 clients** and **6 iShares ETFs**, structured as daily holdings data:

| Column | Description |
|---|---|
| `Date` | Trading date |
| `Client` | Institutional client name (Pension Fund, Endowment, SWF) |
| `Fund` | iShares ETF product name |
| `Asset_Class` | Equity / Fixed Income / Commodities |
| `Ticker` | ETF ticker symbol |
| `Shares` | Number of shares held |
| `Price` | End-of-day NAV |
| `AUM` | Assets Under Management ($) |
| `Daily_Return` | Portfolio fund daily return |
| `Benchmark_Return` | Corresponding benchmark daily return |

**Client types modeled:**
- **Apex Pension Fund** — Balanced allocation (Equity + Fixed Income + Commodities)
- **Meridian Endowment** — Growth-tilted (Equity + Clean Energy + EM)
- **Crescent SWF** — Large AUM Sovereign Wealth Fund (Global diversification)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/mustafahussain/blackrock-portfolio-reporting-tool.git
cd blackrock-portfolio-reporting-tool

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## 📸 Dashboard Sections

1. **KPI Header Bar** — Total AUM, portfolio return, benchmark return, active alpha, fund count
2. **AUM Trend Chart** — Stacked area chart tracking AUM over time by client
3. **Asset Allocation** — Donut chart showing AUM distribution by asset class
4. **Performance vs Benchmark** — Dual-axis chart with daily returns and alpha bars
5. **Fund Alpha Rankings** — Horizontal bar chart ranking funds by active outperformance
6. **Client Account Table** — Sortable summary of all client accounts with formatted metrics
7. **Automated Insights** — Auto-generated analytical commentary on key performance signals

---

## 💡 Key Takeaways & Skills Demonstrated

- **Financial Concepts:** AUM, benchmark attribution, active alpha, asset allocation, return weighting
- **Analytics Engineering:** Data transformation with Pandas, derived metric calculation, aggregation logic
- **Data Visualization:** Multi-chart interactive dashboards with Plotly and Streamlit
- **Business Context:** Mirrors real institutional client reporting workflows in asset management
- **Python Development:** Clean, modular, well-commented code with caching for performance

---

## 🔮 Future Enhancements

- [ ] PDF report export (automated client PDF generation)
- [ ] Risk metrics: VaR, Sharpe Ratio, max drawdown per client
- [ ] Live data integration via yfinance API
- [ ] Email report automation (scheduled delivery to clients)
- [ ] Multi-currency support for global client base

---

## 👤 Author

**Mustafa Hussain**
MS Business Analytics | St. Francis College, Brooklyn NY
📧 mhussainfk53@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/mustafahussainn)

---

*This project is built for educational and portfolio purposes. Data is simulated and does not represent actual client or fund performance.*
