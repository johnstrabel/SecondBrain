---
created: 2026-04-20
source_filename: "download_prices.py"
file_type: python
tags: [thesis-code, data-collection, price-data, stooq, S&P500]
---

# download_prices.py

## What This Script Does

Downloads daily OHLCV price data for the full survivorship-bias-free S&P 500 historical universe (2010–2024) using Stooq via `pandas_datareader`. No API key required, no rate limiting, free historical data back to 2010.

**Process:**
1. Builds the ticker universe from a GitHub repo tracking historical S&P 500 index composition and changes (includes all additions/deletions → survivorship-bias-free, 636 tickers)
2. Creates `daily_prices` table in PostgreSQL if it doesn't exist
3. Downloads each ticker with a short delay (0.3s between requests)
4. Calculates `daily_return` as pct_change of Close prices
5. Stores: `ticker`, `date`, `open`, `high`, `low`, `close`, `volume`, `daily_return`
6. Tracks progress in `price_download_progress.json` — safe to resume after crash

**Why Stooq over Yahoo Finance/Alpha Vantage:**
- Free, no API key, relatively reliable for historical data
- Consistent adjusted price data back to 2010
- pandas_datareader has native Stooq support

**Final dataset:** ~1,022,569 daily price observations across 302 securities (including SPY benchmark)

**Output table:** `daily_prices`

**Run:** `python download_prices.py`

---

## Code

```python
"""
S&P Universe Price Downloader (Stooq)
=======================================
Downloads daily price data via pandas_datareader.
No API key, no rate limiting, free historical data back to 2010.
"""
import pandas_datareader as pdr
from sqlalchemy import create_engine

START_DATE = "2010-01-01"
END_DATE   = "2024-01-01"
DELAY      = 0.3

# Builds universe from: github.com/fja05680/sp500 (historical S&P composition)
# Downloads OHLCV + daily_return per ticker → daily_prices table
# [Full source: Thesis Dump/download_prices.py]
```

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — price data is the foundation for all CAR calculations
- [[Efficient Market Hypothesis]] — survivorship-bias-free universe prevents overestimating returns
