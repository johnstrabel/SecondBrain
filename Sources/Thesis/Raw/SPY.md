---
created: 2026-04-20
source_filename: "SPY.csv"
file_type: csv
tags: [thesis-data, SPY, market-benchmark, prices, daily, 2010-2023]
---

# SPY.csv — Daily SPY Price Data (2010–2023)

## What This File Contains

Daily closing prices for the SPDR S&P 500 ETF Trust (SPY), used as the market benchmark for computing cumulative abnormal returns (CARs) in the event study.

## Data Summary

- **Coverage:** 2010–2023 (aligned with Reddit collection period)
- **Fields:** Date, Open, High, Low, Close, Volume (standard OHLCV)
- **Source:** Downloaded via Stooq (primary) or imported from CSV fallback (import_spy_csv.py)
- **Purpose:** Market return benchmark for CAR = stock return − SPY return

## Key Concepts

- [[Post-Earnings Announcement Drift]] — SPY is the market benchmark for computing abnormal returns
- [[Sentiment Velocity]] — CARs relative to SPY are the dependent variable in all hypothesis tests

*See also: [[SPY Price Data]] for the Session 1 note on this same dataset.*
