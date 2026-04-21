---
created: 2026-04-20
source_filename: "H2_spike_group_summary.csv"
file_type: csv
tags: [thesis-results, H2, velocity-spikes, group-summary, CAR]
---

# H2_spike_group_summary.csv — H2 Velocity Spike Group Summary Statistics

## What This File Contains

Summary statistics for each velocity spike group: event counts and mean cumulative abnormal returns.

## Data Summary

| Group | N events | CAR[+1,+5] | CAR[+1,+20] |
|-------|----------|------------|-------------|
| 3× spike | 1,349 | −0.0032 (−32 bps) | −0.0058 (−58 bps) |
| 5× spike | 3,837 | — | — |
| 10× spike | 13,277 | — | — |
| No spike | 44,234 | — | — |

## Key Finding

3× velocity spikes represent 1,349 events (~2.2% of the 62,697-event dataset). The mean 20-day CAR is −58 bps, confirming the reversion pattern is not just a 5-day artifact but extends to −58 bps over 20 days. This makes economic sense: noise-trading pressure inflates prices briefly, then gradually reverts.

## Key Concepts

- [[Sentiment Velocity]] — group classification by velocity spike threshold
- [[Post-Earnings Announcement Drift]] — opposite direction: PEAD is positive drift, here we see negative reversion
