---
created: 2026-04-20
source_filename: "H1_sentiment_returns.csv"
file_type: csv
tags: [thesis-results, H1, sentiment, returns, OLS, regression, null-result]
---

# H1_sentiment_returns.csv — Hypothesis 1 Regression Results

## What This File Contains

OLS regression output testing H1: Does Reddit sentiment (net_sentiment, avg_sentiment_score) predict abnormal returns around earnings announcements?

## Data Summary

| Metric | CAR[+1,+5] | CAR[+1,+20] |
|--------|------------|-------------|
| Net Sentiment coefficient | 0.0003 | −0.0016 |
| p-value | 0.72 | 0.33 |
| N | 19,251 | 19,251 |

All coefficients statistically insignificant (p >> 0.05).

## Key Finding

**H1 is NOT supported.** Reddit sentiment (FinBERT-scored, as net positive/negative ratio) does not predict post-earnings abnormal returns at any conventional significance level. The p=0.72 for the 5-day window is essentially random noise.

## Interpretation

- FinBERT domain mismatch (Reddit slang vs. formal financial text) likely attenuates true signal
- 83.6% neutral rate in FinBERT output means very little variation in sentiment scores
- Consistent with Antweiler & Frank (2004) — internet message board sentiment has modest informativeness

## Key Concepts

- [[Sentiment Velocity]] — H1 tests sentiment levels (not velocity); contrast with H2 results
- [[FinBERT]] — the sentiment measure used; domain mismatch is the main limitation
- [[Reddit as Financial Signal]] — null result for direct sentiment→returns link
