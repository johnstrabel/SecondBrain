---
created: 2026-04-20
source_filename: "expand_attention_tickers.py"
file_type: python
tags: [thesis-code, utility, attention-signals]
---

# expand_attention_tickers.py

## What This Script Does

One-time setup utility. Updates the `TICKERS` list in `attention_signals_collector.py` to include all 281 tickers from the event study universe (pulled from the database), replacing the initial hard-coded list. Also deletes the old `attention_signals_progress.json` so the collector re-runs for the expanded ticker set.

**Run once before** `attention_signals_collector.py` if the event study universe has changed.

---

## Code

```python
"""
Run ONCE before attention_signals_collector.py.
Updates TICKERS list to use all 281 event study tickers.
Deletes old progress file so collection re-runs.
"""
from sqlalchemy import create_engine, text
# SELECT DISTINCT ticker FROM event_study_results → update TICKERS list
# [Full source: Thesis Dump/expand_attention_tickers.py]
```
