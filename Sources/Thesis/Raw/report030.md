---
created: 2026-04-20
source_filename: "report030.pdf"
file_type: pdf
tags: [thesis-source, Reddit, NLP, stock-prediction, Stanford, CNN, sentence-embedding]
---

# Xu (2021) — NLP for Stock Market Prediction with Reddit Data

**Full citation:** Xu, M. (2021). NLP for Stock Market Prediction with Reddit Data. Stanford CS224N Custom Project.

## Summary

Stanford NLP course project using Reddit/WSB text to forecast market movement. Explores sentence embedding, document embedding (CNN, averaging, Doc2Vec), and sentiment analysis. Tests multiple classifier architectures. Performance shows only slight improvement over the naive forecasting baseline (previous day's direction). The model architecture uses CNN on sentence samples with VADER sentiment.

## Key Arguments

1. **Multiple embedding approaches:** Sentence embedding (averaged word vectors), document CNN on sampled sentences, Doc2Vec, BERT embeddings.
2. **Sentiment integration:** VADER and TextBlob sentiment combined with semantic features.
3. **ACF/PACF analysis:** Shows market prices are highly autocorrelated — naive baseline is strong.
4. **Limited improvement:** Model slightly beats naive forecast — consistent with the thesis's AUC-ROC of 0.520.
5. **Data challenge:** Daily Reddit volume varies hugely; sampling approach to normalize input size.

## Relevance to Thesis

- Independent confirmation that Reddit NLP for stock prediction achieves modest results above chance
- Similar scale of expected performance (slight improvement over naive baseline ~ AUC 0.51–0.52)
- VADER sentiment used here vs. FinBERT in thesis — motivates domain-adapted approach

## Key Concepts

- [[Reddit as Financial Signal]] — direct Reddit NLP for return prediction
- [[Machine Learning in Asset Pricing]] — NLP + ML classifier as the approach
- [[FinBERT]] — BERT-family sentiment; VADER here, FinBERT in thesis
