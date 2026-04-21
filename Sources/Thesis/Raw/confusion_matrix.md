---
created: 2026-04-20
source_filename: "confusion_matrix.png"
file_type: png
tags: [thesis-chart, ML, confusion-matrix, classification, run_analysis, ml_model]
generated_by: ml_model.py
---

# Confusion Matrix — ML Classification Results

## What This Chart Shows

Confusion matrix for the best ML model (Random Forest, AUC-ROC = 0.520) on the 2021–2023 test set. Shows predicted vs. actual class for binary or 4-class return direction classification.

## Expected Content

- 2×2 matrix (binary: up/down) or 4×4 matrix (4 return quartiles)
- Diagonal = correct predictions; off-diagonal = misclassifications
- Expected pattern: near-uniform distribution (model barely beats random)
- 4-class accuracy ~28% means approximately 28% of cells are on the diagonal

## Key Insights

- The near-uniform distribution visually confirms the AUC-ROC of 0.520 result
- Any systematic pattern (e.g., consistently predicting "up" regardless of features) would indicate model degeneration
- 28% accuracy (vs. 25% random baseline) is a modest but nonzero improvement
- The confusion matrix helps identify which return classes are hardest to predict (likely the extreme quartiles Q1, Q4)

## Key Concepts

- [[Machine Learning in Asset Pricing]] — confusion matrix is the standard ML evaluation tool
- [[Reddit as Financial Signal]] — the low accuracy reflects weak Reddit signals
