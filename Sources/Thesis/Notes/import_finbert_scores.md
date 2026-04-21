---
created: 2026-04-20
source_filename: "import_finbert_scores.py"
file_type: python
tags: [thesis-code, FinBERT, NLP, data-import, sentiment-scoring]
---

# import_finbert_scores.py

## What This Script Does

Imports FinBERT sentiment scores from Colab-scored CSV files back into the `ticker_mentions` PostgreSQL table. This is the final step in the sentiment pipeline — after running the Jupyter notebook on Colab, the scored data gets written back to the DB where `build_event_study.py` can use it.

**Expected input format** (from Colab output CSV):
- `id` — matches `ticker_mentions.id`
- `sentiment_label` — 'positive', 'negative', 'neutral'
- `sentiment_score` — confidence score (0–1)
- `sentiment_positive`, `sentiment_negative`, `sentiment_neutral` — full probability distributions

**What it does:**
1. Reads all scored CSVs from `finbert_output/*.csv` (or a specified file)
2. Performs UPDATE on `ticker_mentions` by `id` to write all 5 sentiment columns
3. Batch processes with commit intervals to avoid memory issues
4. `--preview` flag shows sample rows without importing

**Usage:**
```
python import_finbert_scores.py                    # imports all finbert_output/*.csv
python import_finbert_scores.py --file chunk_01_scored.csv
python import_finbert_scores.py --preview          # show sample without importing
```

**Workflow position:** Runs after `finbert_colab.ipynb` completes and before `build_event_study.py`.

---

## Code

```python
"""
Import FinBERT scores back into PostgreSQL.
Updates sentiment_label, sentiment_score, sentiment_positive,
sentiment_negative, sentiment_neutral in ticker_mentions by id.
"""
import os, glob, argparse, pandas as pd
# UPDATE ticker_mentions SET sentiment_label=?, ... WHERE id=?
# [Full source: Thesis Dump/import_finbert_scores.py]
```

---

## Key Concepts

- [[FinBERT]] — this script writes FinBERT outputs back to the database
- [[Reddit as Financial Signal]] — after this runs, all 2.74M mentions have sentiment labels
