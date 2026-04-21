---
created: 2026-04-20
source_filename: "finbert_colab.ipynb"
file_type: ipynb
tags: [thesis-code, FinBERT, NLP, Google-Colab, sentiment-scoring, Jupyter]
---

# finbert_colab.ipynb

## What This Notebook Does

Jupyter notebook designed to run on **Google Colab** (GPU required) to score 2.74M Reddit mentions using the ProsusAI/finbert model. Local execution is infeasible — FinBERT inference on this dataset requires GPU acceleration.

**Workflow position:** Runs after `export_for_finbert.py` creates the input CSVs and before `import_finbert_scores.py` writes scores back to the database.

## Workflow

1. Mount Google Drive (to access input chunk CSVs uploaded from local machine)
2. `pip install transformers torch` on Colab instance
3. Load ProsusAI/finbert model from Hugging Face
4. Process each input chunk (`finbert_input/chunk_0N.csv`) in batches
5. For each `text_snippet`, output: `sentiment_label` (positive/negative/neutral), `sentiment_score`, `sentiment_positive`, `sentiment_negative`, `sentiment_neutral`
6. Save scored chunks as output CSVs (`chunk_0N_scored.csv`)
7. Download scored CSVs to local machine
8. Run `import_finbert_scores.py` to write scores to PostgreSQL

## Model Details

- **Model:** `ProsusAI/finbert` (Hugging Face)
- **Pre-training:** 4.9B tokens of financial text (filings, analyst reports, earnings call transcripts)
- **Fine-tuning:** 10,000 labelled analyst report sentences (positive/negative/neutral)
- **Inference input:** Up to 512 tokens per text snippet; longer texts truncated

## Results on Reddit Corpus

- **Neutral:** 83.6% of 2.74M mentions
- **Negative:** 8.9%
- **Positive:** 7.4%

> The high neutral rate is expected — most stock mentions in Reddit posts are factual or contextual rather than expressing clear sentiment.

## Known Limitation

Domain mismatch: FinBERT trained on formal financial text; Reddit uses slang, irony, memes, abbreviations. This attenuates sentiment signal quality; results interpreted as conservative lower bounds.

---

## Key Concepts

- [[FinBERT]] — this notebook runs the FinBERT inference pipeline
- [[Reddit as Financial Signal]] — Reddit text is the input corpus
