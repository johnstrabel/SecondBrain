---
created: 2026-04-20
source_filename: "spy_diag.py"
file_type: python
tags: [thesis-code, utility, diagnostic, SPY]
---

# spy_diag.py

## What This Script Does

Diagnostic script that checks the `daily_prices` table schema, counts existing SPY rows, and downloads a single test row from Stooq. Used to diagnose whether SPY data was correctly inserted and whether the column structure matched expectations.

---

## Code

```python
import pandas_datareader as pdr, pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')

# Check table structure
result = conn.execute(text("""
    SELECT column_name, data_type FROM information_schema.columns
    WHERE table_name='daily_prices' ORDER BY ordinal_position
""")).fetchall()

# Check current SPY count
count = conn.execute(text("SELECT COUNT(*) FROM daily_prices WHERE ticker='SPY'")).scalar()

# Download one test row from Stooq
```
