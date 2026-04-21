---
created: 2026-04-20
source_filename: "ml_model.py"
file_type: py
tags: [thesis-code, machine-learning, gradient-boosting, random-forest, logistic-regression, AUC-ROC, duplicate]
---

# ml_model.py — ML Classification Models (Raw/ copy)

*Duplicate of [[ml_model]] in Sources/Thesis/Notes/. This copy is in Sources/Thesis/Raw/ alongside the output files.*

## What This Script Does

Trains logistic regression, random forest, and gradient boosting models on the event study features to predict binary return direction. Generates feature importance, confusion matrix, ROC curves, and prediction decile returns.

## Key Outputs

- `model_comparison.csv` — AUC-ROC comparison (best: RF = 0.520)
- `feature_importance.csv` — feature importance rankings
- `confusion_matrix.png`, `roc_curves_binary.png`, `feature_importance.png`, `prediction_decile_returns.png`

See [[ml_model]] for full code annotation.

## Key Concepts

- [[Machine Learning in Asset Pricing]]
