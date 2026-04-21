---
created: 2026-04-20
source_filename: "ml_model.py"
file_type: python
tags: [thesis-code, machine-learning, gradient-boosting, random-forest, logistic-regression, feature-importance]
---

# ml_model.py

## What This Script Does

Trains and evaluates three machine learning models to predict which earnings events will fall in the top or bottom quartile of CAR[+1,+20] — i.e., the post-announcement drift outcome. Implements the signal fusion framework from Gu, Kelly & Xiu (2020) applied to the thesis's hierarchical feature set.

**Models trained:**
1. Logistic Regression (linear baseline)
2. Random Forest (200 trees, max depth 6)
3. Gradient Boosting (200 estimators, learning rate 0.05)

**Feature matrix (15 features):**
- Sentiment layer: `net_sentiment`, `avg_sentiment_score`, `pct_positive`, `pct_negative`
- Velocity layer: `velocity_ratio`, `log_mentions`, `mention_count_90d_avg`
- Attention layer: `google_trends_pre` (30-day avg before event), `log_wiki` (7-day avg before event)
- Fundamental layer: `is_8k`, `is_10q` (filing type indicators)
- Market layer: `beta`, `r_squared`, `log_price`, `log_volume`

**Two tasks:**
- **Binary:** Q1 vs Q4 CAR[+1,+20] (bottom vs top quartile post-drift)
- **4-class:** Predict all four quartiles

**Train/test split:** 2010–2020 train, 2021–2023 test (held-out; includes meme stock era + normalised conditions)

**Outputs (in `ml_results/` folder):**
- `model_comparison.csv` — accuracy, AUC-ROC, CV-AUC, precision, recall, F1
- `feature_importance.csv` and `feature_importance.png` — by signal layer (colour-coded)
- `roc_curves_binary.png`
- `confusion_matrix.png` (best model)
- `prediction_decile_returns.png` — mean CAR by model-predicted probability decile

**Key finding (reported in thesis):** Wikipedia page views (6.2% importance) and Google Trends (5.9%) outperform raw FinBERT sentiment scores. AUC-ROC of 0.520 on 2021–2023 test period — just above random.

**Run:** `python ml_model.py`

---

## Code

```python
"""
ML Model — Information Fusion Framework
=========================================
Train: 2010-2020 | Test: 2021-2023
Target: Binary Q4 vs Q1 CAR[+1,+20]
Models: Logistic Regression, Random Forest, Gradient Boosting

Features (hierarchical framework):
  Sentiment: net_sentiment, avg_sentiment_score, pct_positive, pct_negative
  Velocity:  velocity_ratio, log_mentions, mention_count_90d_avg
  Attention: google_trends_pre, log_wiki
  Fundamental: surprise_day0, is_8k, is_10q
  Market:    beta, r_squared, log_price, log_volume
"""

# [Full source: Thesis Dump/ml_model.py — ~350 lines]
# Key sections: load event study data → join Google Trends → join Wikipedia
#   → build feature matrix → define FEATURE_COLS (15 features)
#   → temporal train/test split → Pipeline(imputer, scaler, model)
#   → binary classification (Q1 vs Q4) → 4-class classification
#   → feature importance (Random Forest Gini) → charts
```

---

## Key Concepts

- [[Machine Learning in Asset Pricing]] — implements Gu, Kelly & Xiu (2020) methodology
- [[Sentiment Velocity]] — velocity_ratio and log_mentions are key features
- [[Post-Earnings Announcement Drift]] — target variable is CAR[+1,+20] quartile
- [[FinBERT]] — sentiment features derived from FinBERT-scored Reddit mentions
