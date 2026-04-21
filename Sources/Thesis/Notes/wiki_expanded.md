---
created: 2026-04-20
source_filename: "wiki_expanded.py"
file_type: python
tags: [thesis-code, data-collection, wikipedia, attention-signals]
---

# wiki_expanded.py

## What This Script Does

Extended Wikipedia page view collector that covers the full event study universe. Uses company names from the SEC EDGAR database records already stored in the DB to build Wikipedia article title mappings, rather than relying solely on the pre-defined `WIKI_TITLES` dictionary in `attention_signals_collector.py`. Falls back to ticker-based search if no mapping is found.

Progress tracked in `wiki_expanded_progress.json`.

---

## Code

```python
"""
Wikipedia collector — expanded to full event study universe.
Looks up company names from SEC EDGAR data in DB to build Wikipedia titles.
Falls back to ticker-based search if no mapping found.
"""
import os, time, json, logging, requests, pandas as pd
from sqlalchemy import create_engine, text

# Uses: wikipedia_pageviews table, EDGAR company names → Wikipedia article lookup
# [Full source: Thesis Dump/wiki_expanded.py]
```

---

## Key Concepts

- [[Sentiment Velocity]] — Wikipedia page views are a complementary attention proxy
- [[Machine Learning in Asset Pricing]] — Wikipedia features ended up with 6.2% feature importance
