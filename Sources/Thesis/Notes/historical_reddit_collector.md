---
created: 2026-04-20
source_filename: "historical_reddit_collector.py"
file_type: python
tags: [thesis-code, data-collection, reddit, arctic-shift, web-scraping, PostgreSQL]
---

# historical_reddit_collector.py

## What This Script Does

Collects 2.74M Reddit posts and comments from 15 financial subreddits spanning 2010–2023, using the Arctic Shift archive API (no auth required — free public access to Reddit's historical database). This is how the primary sentiment dataset was assembled.

**15 subreddits collected:**
r/wallstreetbets, r/Superstonk, r/stocks, r/pennystocks, r/RobinHood, r/StockMarket, r/investing, r/options, r/Daytrading, r/dividends, r/thetagang, r/investing_discussion, r/ValueInvesting, r/algotrading, r/SecurityAnalysis

**Architecture:**
- Iterates month-by-month from 2010-01 to 2023-12 for each subreddit
- Uses `ImprovedTickerExtractor` to identify S&P constituent tickers in each post/comment
- Stores each mention (with text snippet, subreddit, score, author, timestamp, reddit_id) in the `ticker_mentions` PostgreSQL table
- Progress tracked in `historical_collection_progress.json` — safe to resume after crash
- Thread-pool wrapper with `MAX_REQUEST_SECONDS` hard kill for hung HTTP requests

**Key reliability engineering:**
- `socket.setdefaulttimeout(45)` — catches mid-transfer hangs that bypass `requests` timeout
- `timeout=(10, 30)` tuple for separate connect vs read timeouts
- `api_month_end` = first of NEXT month (fixes zero-window bug in earlier version)
- Row-level duplicate prevention via `reddit_id` UNIQUE constraint

**Usage:**
```
python historical_reddit_collector.py                     # full run 2010-2023
python historical_reddit_collector.py --start 2019-01     # resume from month
python historical_reddit_collector.py --subreddit stocks  # single subreddit
python historical_reddit_collector.py --dry-run           # estimate volume
python historical_reddit_collector.py --no-comments       # posts only
```

**Imports:** `ImprovedTickerExtractor`, `database.py` (TickerMention model)

---

## Code

```python
"""
Arctic Shift Historical Reddit Collector
=========================================
Pulls historical Reddit posts from 15 financial subreddits (2010-2023)
using the Arctic Shift API (no auth required).

Key fixes: socket.setdefaulttimeout(45), timeout=(10,30) tuple,
ThreadPoolExecutor hard kill, correct api_month_end calculation
"""
import requests, time, json, os, socket, argparse, logging
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dateutil.relativedelta import relativedelta
from improved_ticker_extractor import ImprovedTickerExtractor
from database import get_session, TickerMention, SourceType

ARCTIC_SHIFT_BASE = "https://arctic-shift.photon-reddit.com/api"

SUBREDDITS = [
    "wallstreetbets", "Superstonk", "stocks", "pennystocks", "RobinHood",
    "StockMarket", "investing", "options", "Daytrading", "dividends",
    "thetagang", "investing_discussion", "ValueInvesting", "algotrading",
    "SecurityAnalysis"
]
# [Full source: Thesis Dump/historical_reddit_collector.py — ~400 lines]
```

---

## Key Concepts

- [[Reddit as Financial Signal]] — this script assembled the 2.74M mention dataset
- [[Sentiment Velocity]] — raw mention counts collected here; velocity ratios computed in build_event_study.py
