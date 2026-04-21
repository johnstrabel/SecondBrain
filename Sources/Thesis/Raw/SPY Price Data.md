---
created: 2026-04-20
source_filename: "SPY.csv"
file_type: csv
tags: [thesis-data, price-data, SPY, S&P500, benchmark]
---

# SPY Price Data

**File:** `SPY.csv`
**Description:** Daily closing prices for the SPDR S&P 500 ETF Trust (SPY) — used as the market benchmark for all market model estimations in the event study.

**Date range:** January 4, 2010 through late 2023
**Rows:** ~3,521 trading days
**Format:** Date (MM/DD/YYYY HH:MM), Close price

## Data Sample

| Date | Close |
|---|---|
| 1/4/2010 16:00 | 113.33 |
| 1/5/2010 16:00 | 113.63 |
| 1/6/2010 16:00 | 113.71 |
| 1/7/2010 16:00 | 114.19 |

## Usage in Thesis

- Market benchmark for OLS market model: `AR = actual_return - (α + β × SPY_return)`
- Imported into `daily_prices` table via `import_spy_csv.py` or `insert_spy.py`
- Fallback source when Stooq was rate-limited during `download_prices.py`
- Used in `build_event_study.py` as `load_market_returns()` — SPY returns used for every CAR calculation

## Key Concepts

- [[Post-Earnings Announcement Drift]] — SPY is the benchmark for all abnormal return calculations
- [[Machine Learning in Asset Pricing]] — beta (from SPY regression) is a feature in the ML model
