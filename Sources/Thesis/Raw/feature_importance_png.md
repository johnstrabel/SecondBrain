---
created: 2026-04-20
source_filename: "feature_importance.png"
file_type: png
tags: [thesis-chart, ML, feature-importance, bar-chart, gradient-boosting, ml_model]
generated_by: ml_model.py
---

# Feature Importance Chart — ML Model Signal Rankings

## What This Chart Shows

Horizontal bar chart visualizing feature importance from the gradient boosting model. Visual representation of the data in feature_importance.csv.

## Expected Content

- X-axis: Importance score (%)
- Y-axis: Feature names (log_price, log_volume, beta, r_squared, log_wiki, google_trends, avg_sentiment_score, mention_count_90d_avg, velocity_ratio, log_mentions, net_sentiment)
- Sorted by importance descending
- log_price bar should be ~2× longer than all others

## Key Insights

- The chart makes visually obvious that fundamental/technical features dominate sentiment features
- Wikipedia and Google Trends bars are longer than all FinBERT-derived features — key finding for the thesis's attention vs. sentiment interpretation
- velocity_ratio and net_sentiment are visually very short (~1–3% range)

## Key Concepts

- [[Machine Learning in Asset Pricing]] — the feature importance ranking is the key ML result
- [[FinBERT]] — avg_sentiment_score and net_sentiment are both near the bottom
- [[Sentiment Velocity]] — velocity_ratio at 3.2% — weak but nonzero
