---
created: 2026-04-20
source_filename: "descriptive_stats.csv"
file_type: csv
tags: [thesis-results, descriptive-statistics, event-study, full-sample, summary]
---

# descriptive_stats.csv — Event Study Full Sample Descriptive Statistics

## What This File Contains

Descriptive statistics for the full event study dataset (all 62,697–62,708 events).

## Data Summary

| Variable | Mean | Std | Min | 25th | 50th | 75th | Max |
|----------|------|-----|-----|------|------|------|-----|
| Events (N) | ~62,700 | — | — | — | — | — | — |
| AR day 0 | 0.0002 | 0.036 | −0.373 | −0.0112 | 0.0002 | 0.0118 | 0.762 |
| velocity_ratio | 5.46 | — | — | — | — | — | — |
| price | $82.55 | — | — | — | — | — | — |
| car_pre_5 | −0.0004 | 0.051 | — | −0.020 | 0.0001 | 0.020 | 0.647 |
| car_post_5 | 0.0004 | 0.049 | — | −0.022 | −0.001 | 0.021 | 0.667 |

## Key Facts

- Full event study universe: **62,697–62,708 earnings events** for 281 S&P 500 stocks (2010–2023)
- Sentiment subset: 19,252 events with FinBERT sentiment scores (31% coverage)
- Mean velocity ratio of **5.46** (7-day/90-day ratio) — dataset skewed toward high-attention events
- Mean day-0 AR near zero (0.02%): earnings announcements are partially anticipated
- Symmetric pre/post return distributions: no overall PEAD visible in raw means

## Key Concepts

- [[Post-Earnings Announcement Drift]] — full event study provides the PEAD testing ground
- [[Sentiment Velocity]] — velocity_ratio is the core signal; mean 5.46 indicates elevated baseline
- [[Reddit as Financial Signal]] — events with sentiment data are a 31% subset (Reddit coverage)
