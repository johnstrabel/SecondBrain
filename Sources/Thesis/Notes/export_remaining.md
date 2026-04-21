---
created: 2026-04-20
source_filename: "export_remaining.py"
file_type: python
tags: [thesis-code, FinBERT, data-export, resume]
---

# export_remaining.py

## What This Script Does

Same as `export_for_finbert.py`, but exports ONLY records where `sentiment_label IS NULL` — used to pick up where a previous Colab FinBERT run left off after a partial scoring pass.

After the initial run scored ~1.8M of 2.74M records, this script exported the remaining ~926k records (2 chunks) for a second Colab pass.

**Output:** `finbert_input_remaining/chunk_01.csv`, `chunk_02.csv` (500k rows each)

---

## Code

```python
"""
Export UNSCORED records for FinBERT re-run.
Only exports WHERE sentiment_label IS NULL.
Output: finbert_input_remaining/chunk_01.csv...
(926k records = 2 chunks)
"""
# [Full source: Thesis Dump/export_remaining.py]
```

---

## Key Concepts

- [[FinBERT]] — continuation of the FinBERT scoring workflow
