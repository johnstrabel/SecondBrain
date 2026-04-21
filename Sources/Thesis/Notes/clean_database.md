---
created: 2026-04-20
source_filename: "clean_database.py"
file_type: python
tags: [thesis-code, database, data-cleaning, false-positives]
---

# clean_database.py

## What This Script Does

Removes known false-positive ticker mentions from the `ticker_mentions` table. Run once after updating `improved_ticker_extractor.py` to apply the expanded blacklist retroactively to already-collected data.

**Workflow:**
1. Loads the current blacklist from `ImprovedTickerExtractor`
2. Queries `ticker_mentions` for records where `ticker` matches any blacklisted term
3. `--preview` flag: shows count and sample rows that would be deleted, without deleting
4. Default (no flag): performs the DELETE

**Safety:** Always run with `--preview` first to confirm what will be removed before executing the delete.

**Usage:**
```
python clean_database.py --preview    # show what would be deleted
python clean_database.py              # actually delete
```

---

## Code

```python
"""
Database Cleaner — removes false positive tickers.
Run ONCE after updating improved_ticker_extractor.py.
"""
import argparse, pandas as pd
from sqlalchemy import create_engine, text

# SELECT ticker, COUNT(*) FROM ticker_mentions WHERE ticker IN (blacklist)
# If not preview: DELETE FROM ticker_mentions WHERE ticker IN (blacklist)
# [Full source: Thesis Dump/clean_database.py]
```

---

## Key Concepts

- [[Reddit as Financial Signal]] — data quality maintenance step
- [[Sentiment Velocity]] — false tickers removed to prevent inflated velocity counts
