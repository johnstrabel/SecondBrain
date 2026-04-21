---
created: 2026-04-20
source_filename: "descriptive_stats_sentiment_subset.csv"
file_type: csv
tags: [thesis-results, descriptive-statistics, sentiment-subset, FinBERT, event-study]
---

# descriptive_stats_sentiment_subset.csv — Sentiment Subset Descriptive Statistics

## What This File Contains

Descriptive statistics for the 19,252-event subset with valid FinBERT sentiment scores.

## Data Summary

| Variable | Mean | Std | Min | 25th | 50th | 75th | Max |
|----------|------|-----|-----|------|------|------|-----|
| N | 19,251–19,252 | — | — | — | — | — | — |
| AR day 0 | 0.0003 | 0.036 | −0.373 | −0.0112 | 0.0002 | 0.0118 | 0.762 |
| velocity_ratio | **16.27** | 16.13 | 0.26 | 8.61 | 10.0 | 20.0 | 645.3 |
| net_sentiment | 0.013 | 0.347 | −1.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| avg_sentiment_score | 0.8495 | 0.099 | 0.342 | 0.805 | 0.878 | 0.924 | 0.978 |
| mention_count_pre | 4.71 | 15.9 | 1.0 | 1.0 | 2.0 | 4.0 | 1,704 |
| beta | 1.016 | 0.452 | −0.809 | 0.735 | 0.994 | 1.275 | 3.762 |
| price | $103.37 | 160.2 | $1.74 | $33.86 | $64.79 | $125.19 | $2,839.91 |

## Key Facts

- Sentiment subset has **much higher velocity** (mean 16.27 vs. 5.46 in full sample) — Reddit coverage is biased toward high-attention events
- Median net_sentiment = 0.0: half of all events have zero net sentiment (neutral dominance)
- avg_sentiment_score mean = 0.849: high neutral confidence scores across all mentions
- Price range: $1.74 to $2,840 — wide cross-sectional coverage including both small caps and mega caps
- Coverage bias: Events with Reddit mentions are already unusual (high velocity) — the 19K events are NOT a representative sample of the 62K event universe

## Interpretive Note

The selection bias in the sentiment subset is crucial: events included in H1 testing are systematically high-velocity events. This makes the H1 null harder to interpret — we're testing sentiment in already-unusual events.

## Key Concepts

- [[Sentiment Velocity]] — velocity ratio dramatically higher in sentiment subset than full sample
- [[FinBERT]] — avg_sentiment_score reflects FinBERT's dominant neutral classification
- [[Reddit as Financial Signal]] — Reddit coverage selection bias is an important limitation
