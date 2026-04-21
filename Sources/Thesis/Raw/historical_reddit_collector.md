---
created: 2026-04-20
source_filename: "historical_reddit_collector.py"
file_type: py
tags: [thesis-code, Reddit, data-collection, Arctic-Shift-API, 15-subreddits, duplicate]
---

# historical_reddit_collector.py — Reddit Mention Collection Script (Raw/ copy)

*Duplicate of [[historical_reddit_collector]] in Sources/Thesis/Notes/. This copy is in Sources/Thesis/Raw/ alongside the collected data.*

## What This Script Does

Collects historical Reddit posts and comments mentioning S&P 500 stock tickers from 15 subreddits via the Arctic Shift API. Saves results to the PostgreSQL `ticker_mentions` table.

## Key Details

- **Subreddits:** wallstreetbets, investing, stocks, options, StockMarket, Superstonk, pennystocks, Daytrading, algotrading, securityanalysis, thetagang, ValueInvesting, dividends, ETFs, RobinHood
- **Result:** 2.74M ticker mentions (2010–2023)
- See [[historical_reddit_collector]] for full code annotation

## Key Concepts

- [[Reddit as Financial Signal]]
