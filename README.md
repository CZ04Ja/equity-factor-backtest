# Equity Factor Research Backtest  
### Quality + Momentum Signal | IC Test | Transaction Cost-Aware Backtest

## Project Overview

This project is a prototype equity factor research workflow designed to test an interpretable **Quality + Momentum** stock selection signal. The goal is not to claim a production-ready trading strategy, but to demonstrate a structured quantitative research process:

**Idea → Data → Signal Construction → IC Test → Portfolio Construction → Backtest → Risk Review → Next Steps**

The strategy combines:
- **Momentum signal**: 12-1 month price momentum  
- **Quality proxy**: low realised volatility as a simplified quality indicator  
- **Portfolio rule**: select top-ranked stocks by the combined signal and construct an equal-weighted long-only portfolio  
- **Cost model**: transaction cost is modelled as `bps × turnover`

This project is built as part of my preparation for investment research, quantitative research, and portfolio risk roles.

---

## Research Motivation

The economic intuition behind the strategy is that stocks with strong medium-term momentum and stable price behaviour may continue to outperform in the near term.(short term) Momentum captures price trend persistence, while the low-volatility proxy attempts to tilt the portfolio toward more stable names.

The current version uses a small sample of large-cap US stocks for demonstration purposes. The focus is on building a clean and reproducible research pipeline rather than maximising backtest performance.

---

## Data

The current prototype uses daily adjusted close prices from `yfinance`.

Sample universe:

```python
["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "XOM", "JNJ", "PG"]

Sample period:

2016-01-01 to 2025-01-01

Main fields used:

Adjusted close price
Daily return
Rolling realised volatility
Momentum signal

Future versions will expand the universe and include:

Sector classification
Market capitalisation
Accounting-based quality metrics such as ROE, ROA, gross profitability, and leverage
Benchmark returns such as S&P 500 ETF / sector ETFs
Signal Construction
1. Momentum Signal

The momentum signal is constructed as a 12-1 month momentum measure:

Momentum = Price(t-21) / Price(t-252) - 1

This skips the most recent 21 trading days to reduce short-term reversal noise.

2. Quality Proxy

The current version uses negative 63-day realised volatility as a simple quality proxy:

Quality Proxy = - Rolling 63-day Volatility

Lower realised volatility receives a higher quality score.

3. Cross-sectional Processing

For each trading date, the signals are processed cross-sectionally:

Winsorisation
Extreme values are clipped at the 1st and 99th percentiles to reduce the impact of outliers.
Z-score standardisation
Each signal is standardised across stocks on the same date:
z = (x - mean) / standard deviation
Signal combination
Final Signal = 0.5 × Momentum Z-score + 0.5 × Quality Z-score
Factor Validation

The signal is evaluated using daily cross-sectional Information Coefficient (IC).

IC Definition

For each date:

IC_t = corr(Signal_i,t, Forward Return_i,t+1)

IC measures whether stocks with higher signal scores tend to have higher future returns.

Positive IC: the signal has positive predictive power
Negative IC: the signal works in the opposite direction
IC close to zero: weak ranking ability

The project also plots the 63-day rolling IC to assess signal stability over time.

Current Observation

The rolling IC is unstable and switches between positive and negative regions. This suggests that the current version of the signal is not yet robust enough for live deployment. This is expected for a prototype using a small stock universe and a simplified quality proxy.

This result is useful because it highlights the importance of:

Larger universe testing
Out-of-sample validation
Sector / style neutralisation
More robust accounting-based quality metrics
Cost and turnover sensitivity analysis
Portfolio Construction

The portfolio is constructed using a simple long-only rule:

Rank stocks by final signal score each day
Select the top 20% of stocks
Apply equal weights
Shift portfolio weights by one day to avoid look-ahead bias
Deduct transaction costs based on turnover
Look-ahead Bias Control

Portfolio weights are shifted by one trading day:

w_lag = w.shift(1)

This ensures that today’s signal is only used for tomorrow’s portfolio return.

Transaction Cost Model

Transaction cost is modelled as:

Cost_t = Cost_bps × Turnover_t

where:

Turnover_t = 0.5 × sum(|w_t - w_t-1|)

The current version uses:

Cost = 20 bps per unit turnover

This helps move the backtest closer to a realistic net performance estimate.

Backtest Outputs

The strategy produces the following outputs:

Net Asset Value (NAV)
Rolling 63-day IC
Annualised return
Annualised volatility
Sharpe ratio
Maximum drawdown
Average turnover

Charts are saved in:

reports/nav.png
reports/rolling_ic.png
NAV Curve

The NAV curve shows strong long-term growth over the sample period, but also a material drawdown around 2022. This suggests that the strategy may have benefited from exposure to large-cap growth and momentum names, especially during strong equity market regimes.

Rolling IC

The rolling IC chart shows that the signal’s predictive power is time-varying. It performs better in some regimes and weakens or reverses in others. This is an important finding and motivates further robustness testing.

How to Run
1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install -r requirements.txt
3. Run the backtest
python src/run_backtest.py
4. Check output charts
ls reports

Expected files:

nav.png
rolling_ic.png
Project Structure
equity-factor-backtest/
│
├── data/                 # Data folder or data source notes
├── docs/                 # Research notes
├── notebooks/            # Exploratory notebooks
├── reports/              # Output charts and research memo
│   ├── nav.png
│   └── rolling_ic.png
├── src/                  # Source code
│   └── run_backtest.py
├── README.md
└── requirements.txt
Current Limitations

This is a first-version prototype. Current limitations include:

Small stock universe
The current sample contains only a small set of large-cap US stocks, which makes IC less stable.
Simplified quality factor
The quality signal is currently proxied by low realised volatility. A more complete version should include ROE, ROA, gross profitability, leverage, and earnings stability.
No sector neutralisation yet
The current strategy may unintentionally load on certain sectors, such as technology.
No explicit factor exposure regression yet
The current version does not yet test whether returns are explained by market beta, size, value, momentum, or quality exposures.
No formal IS/OOS split yet
Future versions should separate the sample into in-sample and out-of-sample periods.
Next Steps

Planned improvements:

Add RankIC and IC information ratio
Add IS/OOS split
Example: 2016–2021 as in-sample and 2022–2024 as out-of-sample
Add transaction cost sensitivity analysis
Example: 10 bps, 20 bps, 50 bps
Add benchmark comparison against SPY
Add sector and size neutralisation
Add factor exposure regression using market, size, value, and momentum factors
Replace low-volatility proxy with accounting-based quality metrics
Expand the stock universe to S&P 500 constituents
Generate a one-page investment research memo
Skills Demonstrated

This project demonstrates:

Python data analysis with pandas and NumPy
Financial data cleaning and return calculation
Cross-sectional signal construction
Winsorisation and z-score standardisation
IC and rolling IC analysis
Portfolio construction and look-ahead bias control
Transaction cost modelling
Backtesting and performance evaluation
Research documentation for investment and quant roles
Relevance to Investment Research and Quantitative Research

This project is relevant to investment research, quantitative research, and portfolio risk roles because it connects investment intuition with a reproducible data workflow.

It shows how to move from a simple market hypothesis to a tested signal, evaluate its predictive power, construct a portfolio, account for trading costs, and identify limitations through risk and robustness analysis.