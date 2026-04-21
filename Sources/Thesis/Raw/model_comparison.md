---
created: 2026-04-20
source_filename: "model_comparison.csv"
file_type: csv
tags: [thesis-results, ML, model-comparison, AUC-ROC, logistic-regression, random-forest, gradient-boosting]
---

# model_comparison.csv — ML Model Performance Comparison

## What This File Contains

AUC-ROC and accuracy metrics for three ML classifiers (logistic regression, random forest, gradient boosting) predicting binary/multi-class return direction.

## Data Summary

| Model | AUC-ROC | 4-class Accuracy |
|-------|---------|-----------------|
| Random Forest | **0.5200** (best) | ~28% |
| Logistic Regression | 0.5198 | ~28% |
| Gradient Boosting | 0.5160 | ~28% |
| Random baseline (binary) | 0.500 | 25% (4-class) |

## Key Finding

**All models achieve AUC-ROC ≈ 0.520.** This is barely above random (0.500). 4-class accuracy of ~28% beats the 25% random baseline marginally. The predictive content of the combined signal set is minimal.

## Interpretation

- AUC-ROC of 0.520 means the model correctly ranks positive above negative returns only 52% of the time — economically meaningless after transaction costs
- Random Forest and Logistic Regression perform nearly identically — the signals are too weak for complex models to add value
- The 2021–2023 test period may be particularly challenging (post-COVID market regime change)
- Result is consistent with Ke, Kelly & Xiu's finding that pre-specified sentiment scores (not return-adapted) have limited predictive power

## Key Concepts

- [[Machine Learning in Asset Pricing]] — Gu, Kelly & Xiu (2020) find much higher AUC with return-adapted ML; difference reflects signal quality
- [[Reddit as Financial Signal]] — Reddit signals alone produce AUC 0.520; attention signals are the best contributors
- [[Efficient Market Hypothesis]] — 0.520 AUC is consistent with near-efficient markets
