---
created: 2026-04-20
source_filename: "recover_quartiles.py"
file_type: python
tags: [thesis-code, utility, event-study, database]
---

# recover_quartiles.py

## What This Script Does

Recovery script for when `build_event_study.py` crashes during the quartile assignment step. Since event data is INSERT-first and quartiles are a separate UPDATE pass, this script reruns only the quartile assignment without reprocessing all events — preserving the hours of computation already done.

**Recomputes and writes back:** `surprise_day0_quartile`, `sue_quartile`, `velocity_quartile`, `sentiment_quartile`

---

## Code

```python
"""
Recovery — reruns ONLY quartile assignment and DB insert.
Use after main pipeline crashes at the quartile step.
Event data is already in event_study_results.
"""
import numpy as np, pandas as pd
from sqlalchemy import create_engine, text
# SELECT id, surprise_day0, sue_value, velocity_ratio, net_sentiment
# → pd.qcut into 4 quartiles → UPDATE event_study_results SET *_quartile WHERE id
# [Full source: Thesis Dump/recover_quartiles.py]
```
