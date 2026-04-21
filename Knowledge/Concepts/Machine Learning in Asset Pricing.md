---
created: 2026-04-20
tags: [concept, finance, machine-learning, asset-pricing, gradient-boosting, random-forest, return-prediction]
---

# Machine Learning in Asset Pricing

## Overview

The application of statistical learning methods to predict asset returns using large sets of financial characteristics. The field was transformed by Gu, Kelly & Xiu (2020), who demonstrated that gradient boosting and neural networks substantially outperform OLS regression in out-of-sample monthly return prediction.

## Key Papers

### Gu, Kelly & Xiu (2020) — The Methodological Anchor
*Review of Financial Studies, 33(5), 2223–2273*

- Tested ~100 stock characteristics using penalised linear regression, dimensionality reduction, regression trees, random forests, gradient boosted trees, and neural networks
- **Key finding:** Gradient boosted trees and neural networks substantially outperform OLS; improvement concentrated in **nonlinear interaction effects** among predictors
- Three aspects particularly relevant to this thesis:
  1. Temporal train-test split (2010–2020 train, 2021–2023 test) — closely mimics live trading conditions
  2. Interaction effects motivate gradient boosting to detect velocity × earnings surprise interaction (H4)
  3. Non-traditional variables (including sentiment) contribute meaningfully to predictive accuracy

### Giglio, Kelly & Xiu (2022) — Factor Models and ML
*Annual Review of Financial Economics, 14, 337–368*

- ML methods as flexible, data-driven estimates of the conditional expected return function that parametric factor models approximate
- Justifies including traditional risk controls alongside sentiment features

### Murray, Xia & Xiao (2024) — Charting by Machines
*Journal of Financial Economics, 153, 103791*

- CNNs identify return-predictive chart patterns not derivable from first principles
- Context independence (patterns generalise across time/markets) supports using ML-derived signal weights

### Brogaard & Zareei (2023) — ML and the Stock Market
*Journal of Financial and Quantitative Analysis, 58(4), 1431–1472*

- Gradient boosting generates ~1.0 Sharpe on long-short strategies; robust to transaction costs
- **Critical for thesis:** ML models perform substantially better with alternative data including sentiment — direct motivation for multi-source signal architecture

### Ke, Kelly & Xiu (2021) — Text Data and Return Prediction

- News text signals predict returns with efficiency delay varying with arbitrage costs
- Stronger effects for smaller, more volatile stocks — motivates H3

## Implementation in Thesis

**Three models trained:**
1. Logistic Regression (linear baseline)
2. Random Forest (200 trees, max depth 6, min 50 samples/leaf)
3. Gradient Boosting (200 estimators, learning rate 0.05)

**Pipeline:** `SimpleImputer(median) → StandardScaler → model`
**Target:** Binary Q4 vs Q1 CAR[+1,+20]
**Split:** Train 2010–2020, Test 2021–2023

**15 features across five signal layers:**

| Layer | Features |
|---|---|
| Sentiment | net_sentiment, avg_sentiment_score, pct_positive, pct_negative |
| Velocity | velocity_ratio, log_mentions, mention_count_90d_avg |
| Attention | google_trends_pre, log_wiki |
| Fundamental | is_8k, is_10q |
| Market | beta, r_squared, log_price, log_volume |

**Key results:**
- AUC-ROC: 0.520 on 2021–2023 test period (barely above random 0.5)
- Feature importance (Random Forest Gini): Wikipedia page views **6.2%**, Google Trends **5.9%** > FinBERT sentiment scores
- Attention signals outperform sentiment scores — novel finding contributing to literature

## Appears In

- [[Thesis_Final]] — Sections 2.3, 3.4, Chapter 5 (ML results)
- [[Thesis Proposal - John Strabel]] — ML framework described in proposal
- [[ml_model]] — implements all three models
- [[run_analysis]] — hypothesis tests (separate from ML)
- [[FinBERT]] — sentiment features in ML model
- [[Sentiment Velocity]] — velocity features in ML model
