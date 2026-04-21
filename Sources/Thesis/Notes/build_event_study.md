---
created: 2026-04-20
source_filename: "build_event_study.py"
file_type: python
tags: [thesis-code, event-study, PEAD, market-model, CAR, pipeline]
---

# build_event_study.py

## What This Script Does

The core empirical pipeline for the thesis. Builds the `event_study_results` table in PostgreSQL — the primary dataset used for all hypothesis testing. Processes ~115,000 earnings announcement events across 281 S&P 500 constituents from 2010–2024.

**Pipeline steps:**
1. Loads price data, SPY market returns, earnings announcement dates, and FinBERT-scored Reddit sentiment from the database
2. For each earnings event, estimates a market model (OLS regression: stock return ~ SPY return) over a 120-day estimation window [-120, -21] before the announcement
3. Computes abnormal returns and CARs across pre-announcement [-5,-1], day-0, and post-announcement [+1,+5], [+1,+10], [+1,+20] windows
4. Computes sentiment velocity features from Reddit data in the [-7,-1] pre-announcement window: 7-day count / 90-day baseline avg = velocity ratio; 3×/5×/10× spike thresholds
5. Attempts to fetch SUE (Standardised Unexpected Earnings) from yfinance as supplementary data
6. Inserts all results to `event_study_results` table, then assigns quartiles (surprise, velocity, sentiment, SUE) via a separate UPDATE pass — so data is safe before quartile computation

**Key configuration:**
- Estimation window: -120 to -21 trading days (min 60 days required for valid model)
- Pre-event: -5 to -1; Post-event: +1 to +20
- Market benchmark: SPY
- Study period: 2010-01-01 to 2024-01-01

**Output table columns include:** `ticker`, `event_date`, `filing_type`, `alpha`, `beta`, `r_squared`, `model_valid`, `car_pre_5`, `ar_day0`, `car_post_5/10/20`, `surprise_day0`, `sue_value`, `mention_count_7d`, `velocity_ratio`, `velocity_spike_3x/5x/10x`, `net_sentiment`, `pct_positive/negative/neutral`, velocity/surprise/sentiment/sue quartiles

**Robustness detail:** Results are INSERT-first, then quartile UPDATE — a crash during quartile assignment cannot lose the underlying CAR data.

**Run:** `python build_event_study.py`

---

## Code

```python
"""
PEAD Event Study Pipeline
==========================
Builds the core empirical dataset for the thesis:
"Information Fusion in Financial Markets"

Output table: event_study_results
Run: python build_event_study.py
"""

import os, warnings, logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from scipy import stats
import yfinance as yf

warnings.filterwarnings("ignore")
load_dotenv()

ESTIMATION_START    = -120
ESTIMATION_END      = -21
PRE_EVENT_START     = -5
PRE_EVENT_END       = -1
POST_EVENT_START    = 1
POST_EVENT_END      = 20
MIN_ESTIMATION_DAYS = 60
MARKET_TICKER       = 'SPY'
STUDY_START         = '2010-01-01'
STUDY_END           = '2024-01-01'

# [Full source: Thesis Dump/build_event_study.py — ~500 lines]
# Key functions: setup_db(), load_prices(), load_market_returns(),
#   load_earnings(), load_sentiment(), estimate_market_model(),
#   compute_car(), compute_sentiment_features(), run_pipeline()
```

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — this script builds the dataset for all PEAD hypothesis tests
- [[Sentiment Velocity]] — velocity ratio and spike thresholds computed here
- [[Market Model]] — OLS estimation over 120-day pre-event window; SPY as benchmark
