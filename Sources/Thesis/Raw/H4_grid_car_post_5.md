---
created: 2026-04-20
source_filename: "H4_grid_car_post_5.csv"
file_type: csv
tags: [thesis-results, H4, PEAD, velocity, earnings-surprise, interaction, CAR-5]
---

# H4_grid_car_post_5.csv — H4 Interaction Grid: CAR[+1,+5] by Surprise × Velocity Quartiles

## What This File Contains

4×4 grid of mean CAR[+1,+5] for each combination of earnings surprise quartile (1=most negative, 4=most positive) and velocity ratio quartile.

## Data Summary

| Surprise Q | Velocity Q1 | Velocity Q2 | Velocity Q3 | Velocity Q4 |
|------------|------------|------------|------------|------------|
| Q1 (neg) | +0.0013 | +0.0001 | −0.0001 | +0.0004 |
| Q2 | +0.0001 | −0.0020 | −0.0008 | −0.0007 |
| Q3 | +0.0005 | −0.0013 | +0.0001 | −0.0013 |
| Q4 (pos) | +0.0012 | +0.0012 | +0.0009 | +0.0018 |

Cell counts: ~3,300–4,200 per cell (balanced design).

## Key Finding

No clear amplification pattern. For Q4 (positive surprise), CARs are positive across all velocity quartiles (0.0009–0.0018) — no monotonic increase with velocity. For Q1 (negative surprise), CARs are mostly near zero or slightly positive — again no amplification. H4 is not supported.

## Interpretation

- H4 predicted: High velocity + Positive surprise → Higher PEAD; High velocity + Negative surprise → More negative PEAD
- Observed: Pattern is irregular; if anything, Q4+Q4 (best surprise, highest velocity) shows +18 bps — a hint of amplification but not significant
- Velocity quartiles are determined by the within-event distribution, not by spike thresholds — different from H2's threshold approach

## Key Concepts

- [[Post-Earnings Announcement Drift]] — PEAD is the target being tested in H4
- [[Sentiment Velocity]] — velocity quartiles as the moderator variable
