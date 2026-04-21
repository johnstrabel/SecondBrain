---
created: 2026-04-20
source_filename: "check_db.py"
file_type: python
tags: [thesis-code, utility, database, diagnostic]
---

# check_db.py

## What This Script Does

Minimal diagnostic script that checks the row counts in the `daily_prices` table — specifically how many SPY rows exist vs total rows. Used to verify that price data collection is complete or to quickly confirm database connectivity.

---

## Code

```python
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')
with engine.connect() as conn:
    spy   = conn.execute(text("SELECT COUNT(*) FROM daily_prices WHERE ticker='SPY'")).scalar()
    total = conn.execute(text("SELECT COUNT(*) FROM daily_prices")).scalar()
    print('SPY rows:', spy)
    print('Total rows:', total)
```
