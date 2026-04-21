---
created: 2026-04-20
source_filename: "test_insert.py"
file_type: python
tags: [thesis-code, utility, diagnostic, price-data]
---

# test_insert.py

## What This Script Does

Tests the price data download and insert pipeline for a single ticker (AAPL) using Stooq via pandas_datareader. Verifies that the DB connection, data format, and insert logic work correctly before running `download_prices.py` on the full universe. Used during development to debug column mapping and data type issues.

---

## Code

```python
import os, warnings, pandas as pd
import pandas_datareader as pdr
from sqlalchemy import create_engine, text

# Download AAPL from Stooq
# Calculate daily_return
# Test insert into daily_prices
# Verify row count
# [Full source: Thesis Dump/test_insert.py]
```
