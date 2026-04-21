---
created: 2026-04-20
source_filename: "H2_velocity_spikes.csv"
file_type: csv
tags: [thesis-results, H2, velocity-spikes, abnormal-returns, t-test, partial-support]
---

# H2_velocity_spikes.csv — Hypothesis 2 Velocity Spike Test Results

## What This File Contains

T-test results for H2: Do velocity spikes (3×, 5×, 10× above 90-day baseline) predict abnormal returns?

## Data Summary

| Velocity Threshold | Window | t-stat | p-value | Mean CAR | N |
|-------------------|--------|--------|---------|----------|---|
| 3× spike | CAR[+1,+5] | −2.06 | 0.039* | −0.0032 (−32 bps) | 1,349 |
| 5× spike | CAR[+1,+5] | n.s. | >0.05 | — | 3,837 |
| 10× spike | CAR[+1,+5] | n.s. | >0.05 | — | 13,277 |
| No spike | (baseline) | — | — | — | 44,234 |

*p < 0.05; all other results insignificant

## Key Finding

**H2 is PARTIALLY supported.** Only the 3× velocity spike threshold shows a statistically significant effect: −32 bps in the 5-day post-event window (t=−2.06, p=0.039). The effect is negative (reversion), consistent with noise-trading hypothesis. 5× and 10× thresholds are insignificant — likely because 10× captures more legitimate attention events.

## Interpretation

- The 3× spike is the marginal noise-trading event: unusual enough to attract uninformed retail attention, not large enough to contain real information
- Negative sign: sentiment spike → price rise → subsequent reversion to fundamentals (Tetlock 2007 pattern)
- The −32 bps is statistically but not economically large after transaction costs

## Key Concepts

- [[Sentiment Velocity]] — velocity spike is the core signal being tested here
- [[Reddit as Financial Signal]] — Reddit mention velocity as the attention measure
- [[Efficient Market Hypothesis]] — noise-trading reversion is consistent with semi-strong EMH
