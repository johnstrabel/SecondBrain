---
created: 2026-04-20
source_filename: "import_spy_csv.py"
file_type: py
tags: [thesis-code, SPY, prices, PostgreSQL, import, duplicate]
---

# import_spy_csv.py — Import SPY Prices from CSV (Raw/ copy)

*Duplicate of [[import_spy_csv]] in Sources/Thesis/Notes/.*

Imports SPY.csv (daily prices) into the PostgreSQL `daily_prices` table. Used as a fallback when Stooq rate limits prevent direct download via insert_spy.py.

See [[import_spy_csv]] for full annotation.
