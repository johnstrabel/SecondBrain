---
created: 2026-04-20
source_filename: "import_spy_csv.py"
file_type: python
tags: [thesis-code, utility, SPY, price-data]
---

# import_spy_csv.py

## What This Script Does

Imports SPY daily prices from `SPY.csv` into the `daily_prices` PostgreSQL table. Used as a fallback when Stooq was rate-limited during `download_prices.py` execution. Handles flexible column naming (auto-detects date and close columns).

**Input:** `SPY.csv` — Date, Close format (2010–2023 daily prices)

---

## Code

```python
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')
df = pd.read_csv('SPY.csv')
# Auto-detect date and close columns
date_col  = next((c for c in df.columns if 'date'  in c.lower()), df.columns[0])
close_col = next((c for c in df.columns if 'close' in c.lower()), df.columns[1])
# Insert into daily_prices WHERE ticker='SPY'
```
