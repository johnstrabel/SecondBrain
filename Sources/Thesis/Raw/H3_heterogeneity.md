---
created: 2026-04-20
source_filename: "H3_heterogeneity.csv"
file_type: csv
tags: [thesis-results, H3, heterogeneity, size, beta, subgroup-analysis, null-result]
---

# H3_heterogeneity.csv — Hypothesis 3 Cross-Sectional Heterogeneity Results

## What This File Contains

Regression coefficients testing H3: Does the sentiment→returns relationship vary cross-sectionally by firm size or beta?

## Data Summary

All 8 sentiment coefficients (across size quartiles and beta quartiles) are statistically insignificant (p > 0.05).

| Subgroup | Sentiment Coeff | p-value |
|----------|----------------|---------|
| Small firms | insig. | >0.05 |
| Large firms | insig. | >0.05 |
| Low beta | insig. | >0.05 |
| High beta | insig. | >0.05 |
| (all 8 groups) | all insig. | all >0.05 |

## Key Finding

**H3 is NOT supported.** The null from H1 persists even when the sample is segmented by size and beta. The absence of cross-sectional heterogeneity in sentiment response is consistent with H1's overall null — if there's no aggregate effect, there can be no differential effect.

## Interpretation

- Baker & Wurgler (2006) predict that sentiment effects should be stronger for small, volatile stocks — this is not observed
- Possible explanation: The thesis's velocity signal (H2) captures attention, not sentiment; size/beta moderate sentiment but not attention
- Alternatively: The 5-year Reddit data coverage may not span enough sentiment cycles for the cross-sectional pattern to emerge

## Key Concepts

- [[Sentiment Velocity]] — H3 tests sentiment levels, not velocity — different signal
- [[Reddit as Financial Signal]] — Reddit coverage biased toward large, high-attention stocks
- [[Efficient Market Hypothesis]] — no differential sentiment sensitivity across firm types
