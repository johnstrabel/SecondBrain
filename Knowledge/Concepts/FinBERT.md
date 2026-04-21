---
created: 2026-04-20
tags: [concept, NLP, machine-learning, sentiment-analysis, transformer, finance]
---

# FinBERT

## Definition

A BERT-based transformer language model pre-trained on financial text and fine-tuned for financial sentiment classification. Developed by Huang, Wang & Yang (2023). The state-of-the-art approach for classifying financial text as **positive / negative / neutral** sentiment.

**Implementation used in thesis:** `ProsusAI/finbert` (Hugging Face)

## Technical Details

- **Pre-training corpus:** 4.9 billion tokens from financial text — corporate filings, analyst reports, earnings call transcripts
- **Fine-tuning dataset:** 10,000 labelled analyst report sentences
- **Output:** Three probability scores per text snippet — P(positive), P(negative), P(neutral)
- **Net sentiment score:** `net_sentiment = P(positive) - P(negative)`

## Benchmark Performance

FinBERT outperforms on financial sentiment tasks:
- Loughran-McDonald dictionary (first-generation)
- Naïve Bayes, SVM, Random Forest
- CNN, LSTM
- General-purpose BERT

**Kirtac & Germano (2024)** — evaluated on ~1M financial news articles 2010–2023; FinBERT is strong second-best to larger GPT-variant (OPT) but far more computationally tractable at scale.

## Three Generations of Financial NLP

| Generation | Methods | Limitation |
|---|---|---|
| 1st | Loughran-McDonald dictionary | Misses context, sarcasm, informal language |
| 2nd | SVM, Random Forest, CNN | Requires domain-specific labelled data; poor generalization |
| 3rd (current) | FinBERT, other BERT variants | Domain mismatch with informal Reddit text |

## Application in Thesis

Applied to **2,738,767 Reddit posts and comments** from 15 financial subreddits. Workflow:
1. `export_for_finbert.py` — exports `id` + `text_snippet` in 500k-row chunks
2. `finbert_colab.ipynb` — runs on Google Colab (GPU required)
3. `import_finbert_scores.py` — writes `sentiment_label`, `sentiment_score`, `sentiment_positive`, `sentiment_negative`, `sentiment_neutral` back to `ticker_mentions` table

**Results on Reddit corpus:**
- Neutral: **83.6%** of mentions
- Negative: **8.9%**
- Positive: **7.4%**
- Consistent with documented negativity bias in retail investor discourse

## Known Limitation: Domain Mismatch

FinBERT was trained on formal financial documents (analyst reports, earnings calls), not informal Reddit discourse with slang, irony, memes, and community-specific terminology (e.g., "to the moon", "diamond hands", "bagholder"). This domain mismatch likely **attenuates** measured sentiment-return relationships toward zero — making thesis results conservative lower bounds.

## Thesis Finding

H1 (sentiment predicts returns) **not supported**. ML feature importance shows raw FinBERT sentiment scores are outperformed by attention signals (Wikipedia page views 6.2%, Google Trends 5.9%). Suggests the domain mismatch significantly degrades the signal.

## Appears In

- [[Thesis_Final]] — Section 2.4, Section 4.1.2, Chapter 5
- [[export_for_finbert]] — data export for scoring
- [[import_finbert_scores]] — scores imported back to DB
- [[database]] — sentiment columns in `ticker_mentions` schema
- [[build_event_study]] — sentiment features computed from scored mentions
- [[ml_model]] — sentiment features as model inputs
