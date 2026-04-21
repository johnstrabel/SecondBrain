---
created: 2026-04-20
source_filename: "feature_importance.csv"
file_type: csv
tags: [thesis-results, ML, feature-importance, gradient-boosting, random-forest, signal-ranking]
---

# feature_importance.csv — ML Model Feature Importance Rankings

## What This File Contains

Feature importance scores from the gradient boosting (and random forest) ML models predicting binary return direction.

## Data Summary

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | log_price | **30.0%** |
| 2 | log_volume | **13.2%** |
| 3 | beta | **12.5%** |
| 4 | r_squared | **10.9%** |
| 5 | log_wiki | **6.2%** |
| 6 | google_trends | **5.9%** |
| 7 | avg_sentiment_score | **5.9%** |
| 8 | mention_count_90d_avg | **5.4%** |
| 9 | velocity_ratio | **3.2%** |
| 10 | log_mentions | **1.7%** |
| 11 | net_sentiment | **1.3%** |

## Key Finding

**Fundamental/technical features dominate.** log_price (30%) alone accounts for nearly a third of importance. Wikipedia and Google Trends (attention signals) outperform FinBERT sentiment features. velocity_ratio (3.2%) and net_sentiment (1.3%) are the weakest signals — consistent with H1/H2 null/partial results.

## Interpretation

- log_price dominance reflects price momentum and reversion patterns (technical analysis pillar)
- log_volume, beta, r_squared are risk/fundamental metrics
- Attention signals (Wikipedia 6.2%, Google Trends 5.9%) outperform FinBERT — domain mismatch is the likely explanation
- Reddit-specific sentiment (net_sentiment 1.3%) is the least informative feature

## Key Concepts

- [[Machine Learning in Asset Pricing]] — feature importance is the ML interpretation tool
- [[FinBERT]] — avg_sentiment_score and net_sentiment are both FinBERT-derived; together 7.2%
- [[Sentiment Velocity]] — velocity_ratio has 3.2% importance — weak but nonzero
- [[Reddit as Financial Signal]] — Reddit features (velocity, mentions, sentiment) total ~11.6%
