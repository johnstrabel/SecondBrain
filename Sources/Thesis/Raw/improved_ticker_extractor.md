---
created: 2026-04-20
source_filename: "improved_ticker_extractor.py"
file_type: py
tags: [thesis-code, ticker-extraction, NLP, blacklist, false-positives, duplicate]
---

# improved_ticker_extractor.py — Ticker Extraction (Raw/ copy)

*Duplicate of [[improved_ticker_extractor]] in Sources/Thesis/Notes/.*

Extracts stock tickers from Reddit text using regex + a ~500-term false-positive blacklist. Filters common English words that match ticker symbols (e.g., "A", "IT", "GO"). Applied to 2.74M mentions.

See [[improved_ticker_extractor]] for full annotation.

## Key Concepts
- [[Reddit as Financial Signal]]
