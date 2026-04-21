---
created: 2026-04-20
source_filename: "attention_signals_collector.py"
file_type: python
tags: [thesis-code, data-collection, google-trends, wikipedia, attention-signals]
---

# attention_signals_collector.py

## What This Script Does

Collects two supplementary attention signals for all thesis tickers:

1. **Google Trends** — weekly relative search interest (0–100 scale) via pytrends (unofficial Google Trends API)
   - Proxy for: retail investor attention, public awareness spikes
   - Reference: Da, Engelberg & Gao (2011) "In Search of Attention"
   - Output table: `google_trends` (ticker, date, search_interest 0-100, geo)

2. **Wikipedia page views** — daily article view counts via Wikimedia REST API (free, no auth)
   - Proxy for: information-seeking behaviour, attention velocity
   - Available from July 2015 onwards only
   - Output table: `wikipedia_pageviews` (ticker, date, pageviews, article_title)

**Key technical notes:**
- Google Trends returns *relative* values (0–100), not absolute volumes — normalise to z-scores before use in models
- pytrends is unofficial and gets throttled; 60-second delay between batches; 1 ticker per request
- Data collected in 5-year chunks to maintain consistent normalisation
- Wikipedia data fetched in yearly chunks per ticker
- Progress tracked in `attention_signals_progress.json` for safe resumption
- Company article titles mapped to tickers via `WIKI_TITLES` dictionary; ~80 major tickers have explicit mappings; falls back to ticker-based lookup

**Final dataset:** 158,542 Google Trends observations (227 tickers), 820,302 Wikipedia page view observations (323 tickers)

**Feature importance in ML model:** Wikipedia page views (6.2% Gini importance) and Google Trends (5.9%) outperformed raw FinBERT sentiment scores — the key finding in the ML results.

---

## Code

```python
"""
Google Trends + Wikipedia Page Views Collector
================================================
Collects two attention signals:
  1. Google Trends (pytrends, unofficial API)  → google_trends table
  2. Wikipedia Page Views (Wikimedia REST API) → wikipedia_pageviews table

Key reference: Da, Engelberg & Gao (2011) — "In Search of Attention"
"""
import time, os, json, argparse, logging, requests, pandas as pd
from sqlalchemy import create_engine, text

WIKI_BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
TRENDS_DELAY = 60     # seconds between batches (pytrends throttling)
TRENDS_BATCH = 1      # one ticker per request (safest)

class WikipediaCollector:
    """Fetches daily Wikipedia page view counts for company articles."""
    # Wikimedia only has data from July 2015 onward

class GoogleTrendsCollector:
    """Fetches weekly Google Trends search interest for stock tickers."""
    # Fetch in 5-year chunks; normalise within chunk; z-score before model use

# [Full source: Thesis Dump/attention_signals_collector.py — ~500 lines]
```

---

## Key Concepts

- [[Sentiment Velocity]] — Wikipedia and Google Trends are attention proxies complementary to Reddit velocity
- [[Reddit as Financial Signal]] — attention signals supplement Reddit-derived measures
- [[Machine Learning in Asset Pricing]] — Wikipedia and Google Trends emerge as top features in Random Forest importance
