---
created: 2026-04-20
source_filename: "import_finbert_scores.py"
file_type: py
tags: [thesis-code, FinBERT, sentiment, PostgreSQL, import, duplicate]
---

# import_finbert_scores.py — Import FinBERT Scores (Raw/ copy)

*Duplicate of [[import_finbert_scores]] in Sources/Thesis/Notes/.*

Imports FinBERT-scored CSV chunks (from finbert_colab.ipynb) back into the PostgreSQL `ticker_mentions` table, updating sentiment_label, sentiment_score, and sentiment probabilities.

See [[import_finbert_scores]] for full annotation.

## Key Concepts
- [[FinBERT]]
