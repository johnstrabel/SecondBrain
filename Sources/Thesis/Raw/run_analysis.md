---
created: 2026-04-20
source_filename: "run_analysis.py"
file_type: py
tags: [thesis-code, hypothesis-testing, OLS, t-test, CAR, event-study, duplicate]
---

# run_analysis.py — Hypothesis Testing Script (Raw/ copy)

*Duplicate of [[run_analysis]] in Sources/Thesis/Notes/. This copy is in Sources/Thesis/Raw/ alongside the output files.*

## What This Script Does

Tests H1–H4 using OLS regressions, t-tests, and 4×4 interaction grids. Generates all analysis charts and CSV outputs.

## Key Outputs

- `H1_sentiment_returns.csv`, `H2_velocity_spikes.csv`, `H2_spike_group_summary.csv`, `H3_heterogeneity.csv`
- `H4_grid_car_post_5/10/20.csv`, `H4_pivot_car_post_5/10/20.csv`
- `descriptive_stats.csv`, `descriptive_stats_sentiment_subset.csv`
- `chart1_car_overview.png` through `chart5_velocity_distribution.png`

See [[run_analysis]] for full code annotation.

## Key Concepts

- [[Post-Earnings Announcement Drift]]
- [[Sentiment Velocity]]
