---
created: 2026-04-20
source_filename: "electronics-14-00773.pdf"
file_type: pdf
tags: [thesis-source, sentiment-analysis, technical-indicators, RSI, trading-system, Kim-Yoo-Park, MDPI]
---

# Kim, Yoo & Park (2025) — A Rule-Based Stock Trading Recommendation System Using Sentiment Analysis and Technical Indicators

**Full citation:** Kim, Y., Yoo, S. & Park, S. (2025). A Rule-Based Stock Trading Recommendation System Using Sentiment Analysis and Technical Indicators. *Electronics*, 14(4), 773.

## Summary

Proposes a dual-layered stock trading recommendation system combining NLP-based news sentiment analysis with RSI (Relative Strength Index). Real-time financial news (up to 100 articles/day) processed for sentiment; combined with RSI for buy/sell decisions. Aims to be lightweight and accessible for individual investors, unlike computationally expensive deep learning systems.

## Key Arguments

1. **Dual-layer framework:** Sentiment layer (NLP on news) + technical layer (RSI) — combining two distinct signal types.
2. **Accessibility focus:** Designed for individual investors; low computational cost vs. GPU-based deep learning.
3. **RSI as gatekeeper:** Sentiment signal only triggers trade recommendation when RSI confirms overbought/oversold — reduces false signals.
4. **Addresses prior limitations:** Prior works use either sentiment or TA alone; this integrates both (addresses the research gap).
5. **Real-time news:** Up to 100 financial news articles processed in real time — more comprehensive than prior small-dataset studies.

## Relevance to Thesis

- Practical implementation of the multi-signal fusion concept (sentiment + TA) at the micro level
- Confirms the thesis's theoretical premise that combining signal types improves prediction
- Simple rule-based system shows even without ML, fusion improves over single-signal approaches

## Key Concepts

- [[Reddit as Financial Signal]] — news sentiment here; Reddit sentiment in thesis; same conceptual role
- [[Machine Learning in Asset Pricing]] — rule-based system as the baseline for ML-based fusion
