---
created: 2026-04-20
updated: 2026-04-20
tags: [atlas, thesis, map, index, John-Strabel, VSE]
---

# Thesis Map — Information Fusion in Financial Markets

**Author:** John Strabel | **Institution:** Prague University of Economics and Business (VŠE)
**Title:** Information Fusion in Financial Markets: A Hierarchical Framework for Combining Social Sentiment, Fundamental Valuation, and Technical Analysis
**Supervisor:** Ing. Milan Fičura, Ph.D. | **Year:** 2026

> Master map linking all imported thesis files. Use this to navigate the full project.

---

## Thesis Documents

| File | Description |
|---|---|
| [[Thesis_Final]] | Full thesis draft — all 7 chapters; comprehensive argument with complete literature review |
| [[Thesis Proposal - John Strabel]] | Original thesis proposal with title, methodology, bibliography |
| [[Thesis_Template_Format]] | VŠE-formatted submission version with official abstract and confirmed results |
| [[Sources/Thesis/Notes/Thesis_Final (2)]] | Earlier draft 2 of thesis (docx in Notes/) |
| [[Sources/Thesis/Raw/Thesis_Final (2)]] | Earlier draft 2 duplicate (docx in Raw/) |

---

## Core Pipeline Scripts (Sources/Thesis/Notes/)

| File | Description |
|---|---|
| [[database]] | SQLAlchemy ORM schema — `ticker_mentions`, `velocity_events`, `daily_prices` tables |
| [[historical_reddit_collector]] | Collects 2.74M Reddit mentions from 15 subreddits via Arctic Shift API |
| [[improved_ticker_extractor]] | Extracts stock tickers from Reddit text with ~500-term false-positive blacklist |
| [[edgar_earnings_collector]] | Pulls 115,518 earnings announcement dates from SEC EDGAR |
| [[download_prices]] | Downloads daily OHLCV for 636 historical S&P 500 tickers via Stooq |
| [[export_for_finbert]] | Exports Reddit text chunks for FinBERT scoring on Google Colab |
| [[finbert_colab]] | Jupyter notebook for GPU-accelerated FinBERT inference on 2.74M mentions |
| [[import_finbert_scores]] | Imports FinBERT-scored CSVs back into PostgreSQL |
| [[attention_signals_collector]] | Collects Google Trends (158k obs) and Wikipedia page views (820k obs) |
| [[build_event_study]] | Core pipeline — builds `event_study_results` table with CARs + sentiment features |
| [[run_analysis]] | Tests H1–H4 with OLS, t-tests, 4×4 interaction grids; generates all charts |
| [[ml_model]] | Trains logistic regression, random forest, gradient boosting; feature importance |

---

## Extended / Utility Scripts (Sources/Thesis/Notes/)

| File                         | Description                                                                               |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| [[analyze_data]]             | Generates 6 exploratory charts for the Reddit dataset (mentions by year, subreddit, etc.) |
| [[edgar_expanded]]           | Extended EDGAR collector covering full 281-ticker event study universe                    |
| [[wiki_expanded]]            | Extended Wikipedia collector using EDGAR company names for better article matching        |
| [[expand_attention_tickers]] | One-time setup: updates ticker list in attention collector to full universe               |
| [[export_remaining]]         | Re-exports only NULL-sentiment records for second FinBERT pass (926k mentions)            |
| [[patch_collection]]         | Re-collects specific month-subreddit pairs missed in initial collection                   |
| [[recover_quartiles]]        | Reruns only the quartile assignment step after pipeline crash                             |
| [[clean_database]]           | Removes false-positive tickers from `ticker_mentions` table                               |
| [[check_db]]                 | Diagnostic: checks SPY and total row counts in `daily_prices`                             |
| [[debug_edgar]]              | Development diagnostic: tests EDGAR API connection and response format                    |
| [[debug_pipeline]]           | Smoke test: runs 50-event pipeline to validate before full execution                      |
| [[import_spy_csv]]           | Imports SPY prices from CSV (Stooq rate-limit fallback)                                   |
| [[insert_spy]]               | Downloads and inserts SPY prices from Stooq directly                                      |
| [[spy_diag]]                 | Checks `daily_prices` table schema and SPY row count                                      |
| [[test_insert]]              | Tests price download + insert pipeline for single ticker (AAPL)                           |

---

## Data Files (Sources/Thesis/Raw/)

| File | Description |
|---|---|
| [[SPY Price Data]] | Daily SPY closing prices 2010–2023 — market benchmark for all CARs |
| [[Earnings Dates]] | 115,518 EDGAR earnings announcement dates — t=0 for event study |
| [[SP500 Tickers Historical]] | 636 historical S&P 500 constituent tickers (survivorship-bias-free) |
| [[Reddit Dataset Summary Stats]] | Descriptive statistics: 2.74M mentions, top tickers, by subreddit/year |
| [[Sources/Thesis/Raw/SPY]] | SPY.csv companion note |
| [[Sources/Thesis/Raw/earnings_dates]] | earnings_dates.csv companion note |
| [[Sources/Thesis/Raw/sp500_tickers_2010_2023]] | sp500_tickers_2010_2023.csv companion note |
| [[Sources/Thesis/Raw/summary_stats]] | summary_stats.txt companion note |

---

## Analysis Results (Sources/Thesis/Raw/)

### Hypothesis Test Results (CSVs)

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/H1_sentiment_returns]] | H1 OLS results — sentiment→returns null (p=0.72) |
| [[Sources/Thesis/Raw/H2_velocity_spikes]] | H2 t-test results — 3× spike only significant (−32 bps, p=0.039) |
| [[Sources/Thesis/Raw/H2_spike_group_summary]] | H2 group counts and mean CARs by spike threshold |
| [[Sources/Thesis/Raw/H3_heterogeneity]] | H3 cross-sectional subgroup results — all null |
| [[Sources/Thesis/Raw/H4_grid_car_post_5]] | H4 4×4 grid: CAR[+1,+5] by surprise × velocity quartile |
| [[Sources/Thesis/Raw/H4_grid_car_post_10]] | H4 4×4 grid: CAR[+1,+10] |
| [[Sources/Thesis/Raw/H4_grid_car_post_20]] | H4 4×4 grid: CAR[+1,+20] — counter-directional velocity effect |
| [[Sources/Thesis/Raw/H4_pivot_car_post_5]] | H4 pivot table: CAR[+1,+5] |
| [[Sources/Thesis/Raw/H4_pivot_car_post_10]] | H4 pivot table: CAR[+1,+10] |
| [[Sources/Thesis/Raw/H4_pivot_car_post_20]] | H4 pivot table: CAR[+1,+20] |
| [[Sources/Thesis/Raw/descriptive_stats]] | Full event study descriptive stats (62,700 events) |
| [[Sources/Thesis/Raw/descriptive_stats_sentiment_subset]] | Sentiment subset stats (19,252 events; mean velocity 16.27) |
| [[Sources/Thesis/Raw/feature_importance_csv]] | ML feature importance: log_price=30%, log_volume=13.2%, wiki=6.2% |
| [[Sources/Thesis/Raw/model_comparison]] | ML AUC-ROC comparison: RF=0.520, LR=0.520, GB=0.516 |

### Exploratory Charts (PNGs — analyze_data.py)

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/01_mentions_by_year]] | Reddit mentions by year 2010–2023; 2021 spike |
| [[Sources/Thesis/Raw/02_mentions_by_month]] | Monthly mentions; Jan 2021 GME peak |
| [[Sources/Thesis/Raw/03_top_tickers]] | Top tickers by mention count; GME dominates |
| [[Sources/Thesis/Raw/04_mentions_by_subreddit]] | Mentions by subreddit; WSB majority |
| [[Sources/Thesis/Raw/05_wsb_2021_daily]] | Daily WSB mentions in 2021; GME squeeze detail |
| [[Sources/Thesis/Raw/06_ticker_heatmap]] | Ticker-subreddit co-occurrence heatmap |

### Results Charts (PNGs — run_analysis.py)

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/chart1_car_overview]] | CAR event window overview for full sample |
| [[Sources/Thesis/Raw/chart2_velocity_spikes]] | H2 velocity spike CAR comparison |
| [[Sources/Thesis/Raw/chart3_H4_heatmap]] | H4 surprise × velocity interaction heatmap |
| [[Sources/Thesis/Raw/chart4_sentiment_over_time]] | Reddit sentiment time series 2010–2023 |
| [[Sources/Thesis/Raw/chart5_velocity_distribution]] | Velocity ratio distribution (right-skewed) |

### ML Output Charts (PNGs — ml_model.py)

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/confusion_matrix]] | Confusion matrix — near-uniform, AUC 0.520 |
| [[Sources/Thesis/Raw/feature_importance_png]] | Feature importance bar chart — price/volume dominate |
| [[Sources/Thesis/Raw/prediction_decile_returns]] | Actual returns by predicted probability decile |
| [[Sources/Thesis/Raw/roc_curves_binary]] | ROC curves for LR/RF/GB — all near diagonal |

---

## Academic Sources (Sources/Thesis/Raw/)

### Core Thesis References

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/Tetlock_Media_Sentiment_JF]] | Tetlock (2007) JF — media pessimism → noise-trading reversion |
| [[Sources/Thesis/Raw/wurgler_baker_cross_section]] | Baker & Wurgler (2006) JF — sentiment and cross-section of returns |
| [[Sources/Thesis/Raw/2007-investor-sentiment-in-the-stock-market]] | Baker & Wurgler (2007) JEP — investor sentiment review |
| [[Sources/Thesis/Raw/1-s2.0-S0165410198000263-main]] | Frankel & Lee (1998) JAE — V/P ratio and cross-sectional returns |
| [[Sources/Thesis/Raw/noise-a]] | Antweiler & Frank (2002) JF — internet message board informativeness |
| [[Sources/Thesis/Raw/ssrn-3910214]] | Huang et al. (2022/2023) — FinBERT paper |
| [[Sources/Thesis/Raw/ssrn-3389884]] | Ke, Kelly & Xiu (2021) — predicting returns with text data |
| [[Sources/Thesis/Raw/BFI_WP_201969]] | Ke, Kelly & Xiu (2019) — working paper version |
| [[Sources/Thesis/Raw/value_investing_the_use_of_historical_financial_statement_information]] | Piotroski (2000) — F-SCORE value investing |
| [[Sources/Thesis/Raw/The Journal of Finance - 2020 - COHEN - Lazy Prices]] | Cohen et al. (2020) JF — 10-K text changes predict returns |

### Asset Pricing / Theory

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/campbellshiller88]] | Campbell & Shiller (1988) JF — earnings predict dividends |
| [[Sources/Thesis/Raw/cochrane_2011_afa]] | Cochrane (2011) JF — discount rates as organizing principle |
| [[Sources/Thesis/Raw/The Journal of Finance - 2023 - JENSEN - Is There a Replication Crisis in Finance]] | Jensen et al. (2023) JF — most factors replicate |
| [[Sources/Thesis/Raw/The Journal of Finance - 2023 - JIANG - Re80%90 Imag in ing Price Trends_0]] | Jiang et al. (2023) JF — CNN price chart prediction |
| [[Sources/Thesis/Raw/ImplWACC]] | Gebhardt et al. (2001) JAR — implied cost of capital |
| [[Sources/Thesis/Raw/eastoncoc]] | Easton (2007) FTA — cost of capital survey |
| [[Sources/Thesis/Raw/ssrn-1343516]] | Hou, van Dijk & Zhang (2009) — ICC without analyst forecasts |
| [[Sources/Thesis/Raw/Ohlson 1995 earnings bv div in eq valuation]] | Ohlson (1995) CAR — residual income valuation |
| [[Sources/Thesis/Raw/BrockLakonishokLeBaron1992]] | Brock et al. (1992) JF — technical trading rules |

### Technical Analysis

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/AgMAS04_04]] | Park & Irwin (2004) — profitability of technical analysis: review |
| [[Sources/Thesis/Raw/dp303]] | Sullivan et al. (1999) JF — data snooping and technical trading |
| [[Sources/Thesis/Raw/SSRN-id962461]] | Faber (2007/2013) — quantitative tactical asset allocation |
| [[Sources/Thesis/Raw/2111.13364v2]] | Prasad et al. (2021) — NSGA-II optimal technical indicators |
| [[Sources/Thesis/Raw/cbsrv5i1art15]] | Mukund Harsha (2024) — SMA+OBV+CCI combinations |
| [[Sources/Thesis/Raw/rp346]] | Hong & Wu (2014) — momentum enhances fundamental analysis |

### Reddit / Social Media

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/11408_2022_Article_407]] | Betzer & Harries (2022) — GameStop Reddit trading activity |
| [[Sources/Thesis/Raw/1-s2.0-S1057521924006537-main]] | Warkulat & Pelster (2024) — WSB attention harms retail returns |
| [[Sources/Thesis/Raw/2021.finnlp-1.4]] | Wang & Luo (2021) — GME price prediction from WSB sentiment |
| [[Sources/Thesis/Raw/s41598-022-17925-2]] | Mancini et al. (2022) — Reddit consensus in GameStop squeeze |
| [[Sources/Thesis/Raw/report030]] | Xu (2021 Stanford) — NLP for stock prediction with Reddit |

### NLP / Machine Learning

| File | Description |
|---|---|
| [[Sources/Thesis/Raw/1-s2.0-S1544612324002575-main]] | Kirtac & Germano (2024) — GPT outperforms FinBERT for trading |
| [[Sources/Thesis/Raw/2306.02136v3]] | Zeng & Jiang (2023) — FinBERT+LSTM stock movement prediction |
| [[Sources/Thesis/Raw/electronics-14-00773]] | Kim et al. (2025) — rule-based system: sentiment + RSI |
| [[Sources/Thesis/Raw/130252753]] | Buinevici (2019 Charles Uni) — fundamental + TA combined strategy |
| [[Sources/Thesis/Raw/Fundamental, Sentiment and Technical Analysis for Algorithmic Trading Using Novel Genetic Programming Algorithms]] | Christodoulaki (2024 PhD) — FA+SA+TA genetic programming |

---

## Lecture Sources (Sources/Lectures/Raw/)

| File | Description |
|---|---|
| [[1_2011-Sapir-European_economic_integration]] | Sapir (2011) JEL — European integration review |
| [[2_2010-Green-Problem_of_War_and_the_EU]] | Green (2010) — Has Europe solved the problem of war? |

---

## Key Concepts

| Concept | Description |
|---|---|
| [[Post-Earnings Announcement Drift]] | Core anomaly; event study anchor; target of H4 interaction test |
| [[Sentiment Velocity]] | Novel signal: 7-day/90-day mention ratio; 3×/5×/10× thresholds |
| [[FinBERT]] | Transformer sentiment model; applied to 2.74M Reddit mentions |
| [[Efficient Market Hypothesis]] | Theoretical context; AMH and limits-to-arbitrage as backdrop |
| [[Reddit as Financial Signal]] | Primary data source; 15 subreddits; 2010–2023 dataset characterization |
| [[Machine Learning in Asset Pricing]] | Gu, Kelly & Xiu (2020) framework; gradient boosting; feature importance |

---

## Key Findings Summary

| Hypothesis | Result |
|---|---|
| H1: Sentiment → Returns | **Not supported** (p=0.72) |
| H2: Velocity spikes → Abnormal returns | **Partially supported** — 3× spike → **−32 bps** (noise-trading reversion) |
| H3: Cross-sectional heterogeneity | **Not supported** (all 8 subgroup coefficients insignificant) |
| H4: Velocity amplifies PEAD | **Not supported** in predicted direction (counter-directional at 20-day horizon) |
| ML AUC-ROC (2021–2023) | **0.520** (barely above random) |
| Top ML features | log_price (30%), log_volume (13.2%), beta (12.5%), r_squared (10.9%) |
| Top attention features | Wikipedia page views (6.2%), Google Trends (5.9%) > FinBERT sentiment |

---

*See [[Import Log]] for the complete processing record.*
