---
created: 2026-04-20
source_filename: "prediction_decile_returns.png"
file_type: png
tags: [thesis-chart, ML, decile-returns, backtesting, prediction-quality, ml_model]
generated_by: ml_model.py
---

# Prediction Decile Returns — ML Model Portfolio Backtesting

## What This Chart Shows

Bar chart of mean actual returns by predicted probability decile. Events are sorted by the ML model's predicted probability of positive returns (deciles 1–10) and actual returns are computed for each decile.

## Expected Content

- X-axis: Model prediction decile (1 = lowest predicted probability → 10 = highest)
- Y-axis: Mean actual return in that decile
- Expected pattern if model has power: monotonically increasing from left (negative returns) to right (positive returns)
- Actual pattern: likely noisy with only weak monotonic trend

## Key Insights

- If the decile spread is near-zero (top decile returns ≈ bottom decile returns), the model has no practical alpha
- Given AUC-ROC = 0.520, the spread should be modest — perhaps top-minus-bottom decile of 20–50 bps
- This chart is the most practical "can you make money?" test of the ML model
- Note: Returns shown are gross of transaction costs; real strategy would be significantly worse

## Key Concepts

- [[Machine Learning in Asset Pricing]] — decile spread test is the standard ML horse race evaluation
- [[Reddit as Financial Signal]] — if spread is zero, Reddit signals have no investable alpha
