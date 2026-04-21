---
created: 2026-04-20
source_filename: "improved_ticker_extractor.py"
file_type: python
tags: [thesis-code, NLP, ticker-extraction, false-positive-filtering, regex]
---

# improved_ticker_extractor.py

## What This Script Does

Extracts stock ticker symbols from Reddit post/comment text with aggressive false-positive filtering. Used by `historical_reddit_collector.py` during data collection to identify which S&P constituent tickers are mentioned in each post.

**Core logic:**
1. Regex pattern matches any 1–5 uppercase letter sequence (`\b[A-Z]{1,5}\b`)
2. Filters against a ~500-term blacklist (common words, financial abbreviations, Reddit slang, regulatory bodies, currencies, etc.)
3. Rejects single-letter matches unless they are valid single-ticker stocks (only: `F` for Ford, `C` for Citigroup)
4. Rejects all-vowel sequences

**The blacklist was built iteratively** from 2.5M mention dataset analysis — identifies words that match ticker patterns but aren't stocks (e.g., DRS, MOASS, DTCC from GME-era Reddit; TA, FA, PA for trading concepts; IT, GO, OR as common English words). Updated March 2026 with GME/Superstonk-specific jargon.

**Why this matters for thesis validity:** Poor ticker extraction → inflated false-positive mention counts → noisy velocity and sentiment signals → attenuated hypothesis test results. The blacklist prevents over-counting of mentions where community slang accidentally matches ticker symbols.

**Usage:**
```python
from improved_ticker_extractor import ImprovedTickerExtractor
extractor = ImprovedTickerExtractor()
tickers = extractor.extract_tickers("I bought AAPL and TSLA. TO THE MOON!")
# → {'AAPL', 'TSLA'}
```

---

## Code

```python
"""
Improved Ticker Extractor with Expanded False Positive Filtering
Updated March 2026 — added GME-era Reddit jargon and common false positives
identified from 2.5M mention dataset analysis.
"""
import re

class ImprovedTickerExtractor:
    def __init__(self):
        self.blacklist = {
            # Single letters (except valid tickers)
            'A', 'B', 'C', ..., 'Z',
            # Common words/abbreviations: CEO, ETF, IPO, USA, FOR, AND, THE...
            # Reddit/Internet slang: WSB, DD, YOLO, FD, MOASS, DRS...
            # Financial terms: PUT, CALL, RSI, MACD, GDP, CPI, VIX...
            # Regulatory: SEC, FTC, FDA, FINRA, ESMA...
            # Time/media: EST, PST, WSJ, CNN, CNBC...
            # GME-era jargon: DRS, MOASS, DTCC, PFOF, FTD, HODL...
            # ~500 total terms
        }
        self.valid_single_letters = {'F', 'C'}  # Ford, Citigroup
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')

    def extract_tickers(self, text):
        if not text:
            return set()
        potential_tickers = self.ticker_pattern.findall(text)
        valid_tickers = set()
        for ticker in potential_tickers:
            if ticker in self.blacklist:
                continue
            if len(ticker) == 1 and ticker not in self.valid_single_letters:
                continue
            if all(c in 'AEIOU' for c in ticker):
                continue
            valid_tickers.add(ticker)
        return valid_tickers
```

---

## Key Concepts

- [[Reddit as Financial Signal]] — data quality depends on accurate ticker extraction
- [[Sentiment Velocity]] — false positives in mention counts would inflate velocity ratios; blacklist prevents this
