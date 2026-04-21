---
created: 2026-04-20
source_filename: "run_analysis.py"
file_type: python
tags: [thesis-code, hypothesis-testing, event-study, statistics, OLS, t-test]
---

# run_analysis.py

## What This Script Does

Tests all four thesis hypotheses using the `event_study_results` table. This is where the actual statistical analysis happens — OLS regressions, t-tests, 4×4 interaction grids, and all the charts in the empirical section.

**Hypothesis tests:**

**H1 — Sentiment Predicts Returns:**
OLS regression: CAR[+1,+5] and CAR[+1,+20] ~ net_sentiment + beta + log_price (winsorized at 1st/99th pct). Runs for both net_sentiment and avg_sentiment_score on events with pre-announcement Reddit mentions.

**H2 — Velocity Spikes Precede Abnormal Returns:**
Groups events into No Spike / 3× / 5× / 10× spike categories. Two-sample t-tests comparing AR[0], CAR[+1,+5], CAR[+1,+20] of each spike group vs. No Spike. Also generates spike group summary table.

**H3 — Cross-Sectional Heterogeneity:**
Splits events by size proxy (log_price + log_volume) and beta quartiles. OLS: CAR ~ net_sentiment + beta within each subgroup. Compares sentiment coefficient magnitude across small vs large cap, low vs high beta groups.

**H4 — PEAD-Sentiment Interaction:**
4×4 grid of surprise_quartile × velocity_quartile. Computes mean CAR[+1,+5], [+1,+10], [+1,+20] in each of 16 cells. Key t-test: (surprise Q4, velocity Q4) vs (surprise Q4, velocity Q1) — tests whether high velocity amplifies positive drift. Also: (surprise Q1, velocity Q4) vs (surprise Q1, velocity Q1) for negative surprise case.

**Charts generated (in `analysis_results/`):**
1. `chart1_car_overview.png` — mean CARs for all events vs sentiment-subsample
2. `chart2_velocity_spikes.png` — AR[0], CAR[+1,+5], CAR[+1,+20] by spike group
3. `chart3_H4_heatmap.png` — 4×4 heatmap (surprise × velocity) for 3 CAR windows
4. `chart4_sentiment_over_time.png` — mean net sentiment by year
5. `chart5_velocity_distribution.png` — velocity ratio distribution with spike threshold lines

**Also outputs:** descriptive_stats.csv, H1–H4 CSV result tables, analysis.log

**Run:** `python run_analysis.py`

---

## Code

```python
"""
Hypothesis Testing Analysis
============================
H1: Reddit sentiment scores positively predict short-term returns
H2: Velocity spikes precede abnormal price movements (24-48hr)
H3: Sentiment predictive power varies by stock characteristics
H4: Pre-earnings sentiment velocity amplifies PEAD

Output: analysis_results/ folder
Run: python run_analysis.py
"""

# [Full source: Thesis Dump/run_analysis.py — ~400 lines]
# Key helpers: ttest(), winsorize(), stars(), ols()
# H1: OLS regression on sentiment-subsample
# H2: velocity spike group t-tests
# H3: OLS within size/beta subgroups
# H4: 4x4 grid pivot tables + key t-tests
# Charts: 5 charts saved to analysis_results/
```

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — H4 is the PEAD-velocity interaction test
- [[Sentiment Velocity]] — H2 spike analysis; H4 velocity quartile grid
- [[Efficient Market Hypothesis]] — results interpreted as evidence on limits of semi-strong EMH
