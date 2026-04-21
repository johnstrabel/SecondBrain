---
created: 2026-04-20
source_filename: "edgar_expanded.py"
file_type: python
tags: [thesis-code, data-collection, EDGAR, earnings-dates]
---

# edgar_expanded.py

## What This Script Does

An expanded version of the EDGAR earnings date collector that covers the full event study universe (281 tickers with complete price + earnings data). Looks up company names from the database's existing EDGAR records to build more reliable ticker-to-CIK mappings.

**Difference from `edgar_earnings_collector.py`:** This version uses CIK lookups from the already-stored `earnings_announcements` data to avoid re-doing the full initial lookup, and extends coverage to tickers that may have been missed in the first pass.

Progress tracked in `edgar_expanded_progress.json`.

---

## Code

```python
"""
EDGAR expanded collector — covers full event study universe.
Uses CIK data already in DB to build more reliable mappings.
"""
# [Full source: Thesis Dump/edgar_expanded.py]
```

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — extends earnings date coverage for full 281-ticker universe
