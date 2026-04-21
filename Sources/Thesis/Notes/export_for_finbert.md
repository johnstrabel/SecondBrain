---
created: 2026-04-20
source_filename: "export_for_finbert.py"
file_type: python
tags: [thesis-code, FinBERT, NLP, data-export, Google-Colab]
---

# export_for_finbert.py

## What This Script Does

Exports the Reddit text snippets from the database to CSV chunks for FinBERT sentiment scoring on Google Colab. Since FinBERT requires GPU acceleration and the full 2.74M records can't be processed locally, the data is split into manageable chunks for cloud processing.

**What it exports:**
- Records from `ticker_mentions` where `sentiment_label IS NULL` (unscored)
- Date range: 2010-01-01 to 2024-01-01
- Columns exported: `id`, `text_snippet`

**Output format:**
- Files: `finbert_input/chunk_01.csv`, `chunk_02.csv`, etc.
- Chunk size: 500,000 rows per file
- 2.74M total → ~5-6 chunks, each ~200MB

**Workflow context:**
1. `export_for_finbert.py` → creates chunks
2. Upload to Google Colab
3. Run `finbert_colab.ipynb` on Colab (GPU)
4. Download scored CSVs
5. `import_finbert_scores.py` → writes scores back to DB

**Related scripts:** `export_remaining.py` (same but only NULL sentiment records), `import_finbert_scores.py` (imports scored CSVs)

---

## Code

```python
"""
Export Reddit mentions for FinBERT scoring on Google Colab.
Splits into 500k-row chunks (~200MB each).
"""
import os, pandas as pd
from sqlalchemy import create_engine, text

CHUNK_SIZE = 500_000
OUTPUT_DIR = "finbert_input"

# Queries ticker_mentions WHERE sentiment_label IS NULL
# Exports: id, text_snippet per chunk
# [Full source: Thesis Dump/export_for_finbert.py — ~60 lines]
```

---

## Key Concepts

- [[FinBERT]] — this script feeds data into the FinBERT scoring pipeline
- [[Reddit as Financial Signal]] — text snippets exported here are the raw input for sentiment classification
