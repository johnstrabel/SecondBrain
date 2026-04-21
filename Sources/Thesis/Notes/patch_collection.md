---
created: 2026-04-20
source_filename: "patch_collection.py"
file_type: python
tags: [thesis-code, utility, data-collection, reddit]
---

# patch_collection.py

## What This Script Does

Forces re-collection of specific month-subreddit pairs by removing them from the progress file and re-running just those pairs through the `historical_reddit_collector` pipeline. Used to fill in gaps from network errors, API timeouts, or missed months discovered during data quality checks.

**Usage:**
```
python patch_collection.py --pairs "2020-08:wallstreetbets" "2020-08:stocks"
python patch_collection.py --list       # show all completed pairs in progress file
python patch_collection.py --failed     # re-run all pairs logged as errors
```

**Important:** Do not run simultaneously with the main scraper.

---

## Code

```python
"""
Patch Collection Script — re-collects specific month-subreddit pairs.
Safe only when main scraper is NOT running.
"""
from historical_reddit_collector import (...)
# [Full source: Thesis Dump/patch_collection.py]
```
