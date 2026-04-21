---
created: 2026-04-20
source_filename: "debug_pipeline.py"
file_type: python
tags: [thesis-code, utility, debug, event-study]
---

# debug_pipeline.py

## What This Script Does

End-to-end pipeline smoke test — runs `build_event_study.py` logic on a sample of 50 earnings events. Handles SPY download automatically if it's not already in the database. If this script prints `SUCCESS`, the full `build_event_study.py` can be run safely.

Used to validate the market model estimation, abnormal return computation, and database writes before committing hours of processing on the full 115k-event dataset.

---

## Code

```python
"""
Debug pipeline — runs 50 events end-to-end.
Handles SPY download automatically.
If this prints SUCCESS, run build_event_study.py.
"""
import os, warnings, numpy as np, pandas as pd
import pandas_datareader as pdr
from sqlalchemy import create_engine, text
from scipy import stats
# Same logic as build_event_study.py but limited to 50 events
# [Full source: Thesis Dump/debug_pipeline.py]
```
