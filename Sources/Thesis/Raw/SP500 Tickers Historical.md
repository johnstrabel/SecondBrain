---
created: 2026-04-20
source_filename: "sp500_tickers_2010_2023.csv"
file_type: csv
tags: [thesis-data, S&P500, universe, survivorship-bias-free]
---

# S&P 500 Historical Tickers (2010–2023)

**File:** `sp500_tickers_2010_2023.csv`
**Description:** Survivorship-bias-free list of all historical S&P 500 constituent tickers from 2010 to 2023 — includes companies that were added and later removed (delisted, merged, dropped from index).

**Total tickers:** 636 unique tickers (all additions/deletions tracked)
**Final usable universe:** 301 tickers with sufficient price data available via Stooq; 281 tickers with both price and earnings data (used in event study)

## Why Survivorship-Bias-Free Matters

Restricting analysis to *current* S&P 500 members would overweight firms that survived the full 2010–2023 period, introducing upward bias in historical returns. By including delisted, merged, and dropped firms, the dataset provides an unbiased representation of the information environment available to investors at each point in time.

**Examples of excluded-from-current-index firms that ARE in this dataset:** BBBY (Bed Bath & Beyond, delisted 2023), LB (L Brands), NOK (Nokia), BB (BlackBerry)

## Data Sample

```
ticker
A
AABA
AAL
AAP
AAPL
ABBV
ABT
...
```

## Key Concepts

- [[Post-Earnings Announcement Drift]] — defines the stock universe for all event study calculations
- [[Efficient Market Hypothesis]] — survivorship-bias-free design prevents overstating anomaly magnitude
