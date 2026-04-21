---
created: 2026-04-20
source_filename: "insert_spy.py"
file_type: py
tags: [thesis-code, SPY, prices, Stooq, PostgreSQL, duplicate]
---

# insert_spy.py — Download and Insert SPY Prices (Raw/ copy)

*Duplicate of [[insert_spy]] in Sources/Thesis/Notes/.*

Downloads SPY daily prices from Stooq and inserts directly into the PostgreSQL `daily_prices` table. Primary method (before rate limiting required the CSV fallback).

See [[insert_spy]] for full annotation.
