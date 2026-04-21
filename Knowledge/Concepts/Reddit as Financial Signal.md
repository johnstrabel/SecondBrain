---
created: 2026-04-20
tags: [concept, finance, social-media, reddit, retail-investing, sentiment, WallStreetBets]
---

# Reddit as a Financial Signal

## Overview

Reddit financial communities — particularly r/WallStreetBets — represent a major new source of publicly observable retail investor attention and sentiment. The January 2021 GameStop short squeeze demonstrated that Reddit-driven coordinated retail action can move markets dramatically and measurably, with attention acceleration visible in data *before* price movements occurred.

## Key Literature

| Paper | Finding |
|---|---|
| Antweiler & Frank (2004) | Yahoo Finance message board volume predicted stock volatility (foundational) |
| Tetlock (2007) | WSJ media pessimism predicted downward price pressure + mean reversion (noise trading) |
| Chen, De, Hu & Hwang (2014) | Seeking Alpha sentiment predicted returns + earnings surprises; concentrated in low institutional ownership stocks |
| Betzer & Harries (2022) | WSB post volume → trading activity; no fundamental information content; pure attention effect |
| Warkulat & Pelster (2024) | WSB attention significantly *reduces* holding period returns; peak-attention positions: −8.5% avg return; driven by emotional responses |
| Bradley, Hanousek, Jame & Xiao (2024, RFS) | WSB posts predict returns via retail order flow; effect concentrated in high short interest, high retail ownership stocks |

## The Dataset in John's Thesis

| Metric | Value |
|---|---|
| Total mentions | 2,738,767 |
| Subreddits | 15 |
| Date range | January 2010 – December 2023 |
| Unique tickers mentioned | 53,523 |
| FinBERT-scored mentions | 2,738,767 (all) |

**15 subreddits covered:**
1. r/wallstreetbets (911,602) — dominant; speculative
2. r/Superstonk (362,859) — GME-focused community
3. r/stocks (290,990) — general equities
4. r/pennystocks (267,463) — small-cap speculative
5. r/RobinHood (201,217) — app-specific community
6. r/StockMarket (198,798) — general market discussion
7. r/investing (191,108) — long-term/fundamental focus
8. r/options (83,470) — derivatives
9. r/Daytrading (66,181) — short-term traders
10. r/dividends (54,275) — income investors
11. r/thetagang (43,811) — options sellers
12. r/investing_discussion (21,702)
13. r/ValueInvesting (19,781)
14. r/algotrading (14,522)
15. r/SecurityAnalysis (10,988) — most analytical community

**Top mentioned stocks:** GME (161,489), AMC (62,478), SPY (37,425), TSLA (29,472), AMD (18,708)

## Data Collection

- **Source:** Arctic Shift archive API (free, no auth required)
- **Ticker extraction:** `improved_ticker_extractor.py` with ~500-term blacklist to prevent false positives from Reddit slang (DRS, MOASS, HODL, etc.)
- **Key methodological challenge:** Volume grew from 557 mentions in 2010 to 1,070,608 in 2021 — non-stationary; rolling baselines required

## Key Limitation

FinBERT was trained on formal financial text, not informal Reddit discourse — domain mismatch attenuates measured sentiment quality. Warkulat & Pelster (2024) show Reddit-driven trading is predominantly *uninformed*, suggesting price impacts of velocity spikes may partially reverse.

## Appears In

- [[Thesis_Final]] — Sections 2.2, 4.1.2 (primary data source)
- [[Sentiment Velocity]] — Reddit mentions are the raw input for velocity calculations
- [[FinBERT]] — Reddit text is the input corpus for FinBERT scoring
- [[historical_reddit_collector]] — collected this dataset
- [[improved_ticker_extractor]] — ticker extraction from Reddit text
- [[Reddit Dataset Summary Stats]] — full descriptive statistics
