---
created: 2026-04-20
source_filename: "The Journal of Finance - 2023 - JIANG - Re80%90 Imag in ing Price Trends_0.pdf"
file_type: pdf
tags: [thesis-source, technical-analysis, CNN, image-recognition, price-charts, Jiang-Kelly-Xiu, JF]
---

# Jiang, Kelly & Xiu (2023) — (Re-)Imag(in)ing Price Trends

**Full citation:** Jiang, J., Kelly, B. & Xiu, D. (2023). (Re-)Imag(in)ing Price Trends. *Journal of Finance*, 78(6), 3193–3249.

## Summary

Reconsiders technical analysis using ML image analysis. Represents stock price histories as chart images and uses a CNN to identify return-predictive patterns. Finds patterns differing from standard momentum/reversal, achieving Sharpe ratios up to 2.4 for monthly strategies. Patterns are context-independent: short-term patterns work at longer scales; US-trained patterns work internationally.

## Key Arguments

1. **Imaging prices:** Converting price/volume to 2D images allows CNN to capture complex geometric patterns human technicians use; also normalizes scale across assets.
2. **ML-discovered patterns:** CNN finds patterns significantly different from prespecified momentum or reversal; more predictive than either.
3. **Sharpe ratio 2.4:** Weekly rebalanced equal-weight strategy achieves this; remains profitable after transaction costs at lower frequencies.
4. **Context independence:** Short-term patterns work long-term; US patterns work internationally — suggests universal behavioral or structural origin.
5. **Interpretability:** Unlike standard deep learning, image-based patterns can be visualized and interpreted.

## Relevance to Thesis

- Supports the technical analysis pillar of the hierarchical information fusion framework
- Provides state-of-the-art evidence that price chart patterns contain return-predictive information beyond classical TA
- Contrasts with the thesis's ML approach (gradient boosting on tabular features vs. CNN on images)
- Feature importance finding (log_price = 30%, log_volume = 13.2%) echoes Jiang et al.'s finding that price/volume contain strong signals

## Key Concepts

- [[Machine Learning in Asset Pricing]] — CNN is a ML approach to technical analysis
- [[Efficient Market Hypothesis]] — chart patterns predicting returns challenges weak-form EMH
