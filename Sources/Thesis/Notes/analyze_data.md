---
created: 2026-04-20
source_filename: "analyze_data.py"
file_type: python
tags: [thesis-code, data-analysis, visualization, matplotlib, reddit-dataset]
---

# analyze_data.py

## What This Script Does

Generates exploratory data analysis charts and a summary statistics text file for the Reddit mention dataset. Produces 6 charts used in the descriptive statistics section of the thesis.

**Charts generated (saved to `charts/` folder):**

| Chart | Description |
|---|---|
| `01_mentions_by_year.png` | Bar chart of total Reddit mentions per year 2010–2023 (annotated with exact counts) |
| `02_mentions_by_month.png` | Monthly time series with event annotations (COVID crash, GME squeeze, Crypto boom 2017) |
| `03_top_tickers.png` | Horizontal bar chart of top 25 most-mentioned tickers; meme stocks highlighted in red (GME, AMC, BB, NOK, PLTR, BBBY, etc.) |
| `04_mentions_by_subreddit.png` | Total mentions by subreddit (15 subreddits; r/wallstreetbets dominates with 911,602) |
| `05_wsb_2021_daily.png` | Daily r/wallstreetbets mentions in 2021 with peak annotation (GME era) |
| `06_ticker_heatmap.png` | 15-ticker × 14-year heatmap showing each ticker's share of annual mentions (%) — shows GME's 2021 dominance |

**Also writes** `summary_stats.txt` with totals, top 10 tickers, and by-subreddit breakdown.

**Note:** Queries the live `trading_sentiment` PostgreSQL database — requires DB connection. Dark theme charts (background `#0f1117`).

---

## Code

```python
"""
Reddit Mention Data Analysis & Visualization
Full 2010-2023 dataset version.
"""
import os, pandas as pd, matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

STYLE_BG = "#0f1117"  # dark theme
START = "2010-01-01"
END   = "2024-01-01"

# Queries: mentions by year, monthly time series, top 25 tickers,
#   by subreddit, WSB 2021 daily, 15-ticker heatmap
# [Full source: Thesis Dump/analyze_data.py — ~265 lines]
```

---

## Key Concepts

- [[Reddit as Financial Signal]] — shows temporal distribution, subreddit composition, top meme stocks
- [[Sentiment Velocity]] — monthly time series chart shows non-stationarity requiring rolling baselines
