---
created: 2026-04-20
source_filename: "edgar_earnings_collector.py"
file_type: python
tags: [thesis-code, data-collection, EDGAR, SEC, earnings-dates, PEAD]
---

# edgar_earnings_collector.py

## What This Script Does

Collects earnings announcement dates for ~800 S&P index stocks from the SEC's EDGAR database. No API key required — SEC provides free public access. Outputs to both PostgreSQL (`earnings_announcements` table) and a CSV backup (`earnings_dates.csv`).

**What it collects:**
- **8-K filings** (Item 2.02: "Results of Operations") — the actual earnings press release date; most timely signal (89,675 filings in final dataset)
- **10-Q** (quarterly reports) — fallback where 8-K is missing (19,414 filings)
- **10-K** (annual reports) — further fallback (6,429 filings)

**Why this matters for the thesis:**
- PEAD analysis requires knowing the exact announcement date (t=0)
- Pre-earnings sentiment window: [t-5, t-1]
- Post-earnings drift window: [t+1, t+20]
- Filing date (EDGAR receipt timestamp) used as t=0 — provides precise, auditable timestamp

**Process:**
1. Loads S&P 500 historical constituent tickers
2. Uses `sec_company_tickers.json` to map tickers → CIK numbers
3. Fetches filing index from EDGAR submissions API for each CIK
4. Filters for 8-K, 10-Q, 10-K filings within the study period (2010–2023)
5. For 8-K filings: checks for "2.02" (Results of Operations) item tag to ensure it's an earnings release and not another 8-K type
6. Stores results in `earnings_announcements` table; CSV backup to `earnings_dates.csv`

**Usage:**
```
python edgar_earnings_collector.py                    # full run
python edgar_earnings_collector.py --ticker AAPL      # single ticker test
python edgar_earnings_collector.py --from-csv tickers.csv
```

---

## Code

```python
"""
EDGAR Earnings Dates Collector
================================
Pulls earnings announcement dates from SEC EDGAR.
8-K (primary) + 10-Q + 10-K (fallbacks).

Pre-earnings window: [t-5, t-1]
Post-earnings drift window: [t+1, t+20]
"""
import requests, time, os, json, argparse, logging, pandas as pd
from sqlalchemy import create_engine, text

EDGAR_BASE          = "https://data.sec.gov"
EDGAR_SUBMISSIONS   = "https://data.sec.gov/submissions"

# [Full source: Thesis Dump/edgar_earnings_collector.py — ~300 lines]
# Key logic: CIK lookup → submissions API → filter 8-K Item 2.02
#   → store to earnings_announcements table + earnings_dates.csv
```

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — t=0 for all event study calculations comes from this collector
- [[Efficient Market Hypothesis]] — EDGAR filing date as the public information event
