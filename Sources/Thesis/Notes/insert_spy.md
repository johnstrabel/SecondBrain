---
created: 2026-04-20
source_filename: "insert_spy.py"
file_type: python
tags: [thesis-code, utility, SPY, price-data, stooq]
---

# insert_spy.py

## What This Script Does

Downloads SPY daily price data via Stooq/pandas_datareader and inserts it into the `daily_prices` table. Simpler alternative to `import_spy_csv.py` — fetches live from Stooq rather than reading from a CSV file. Used when the CSV import had formatting issues.

---

## Code

```python
import pandas_datareader as pdr, pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')
df = pdr.get_data_stooq('SPY', start='2010-01-01', end='2024-01-01').sort_index()
df['daily_return'] = df['Close'].pct_change()
# INSERT INTO daily_prices ... ON CONFLICT (ticker, date) DO NOTHING
```
