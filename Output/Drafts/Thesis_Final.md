---
created: 2026-04-20
source_filename: "Thesis_Final (3).docx"
file_type: docx
tags: [thesis, final-draft, sentiment-analysis, PEAD, machine-learning, reddit, finbert, event-study]
---

# Information Fusion in Financial Markets
## A Hierarchical Framework for Combining Social Sentiment, Fundamental Valuation, and Technical Analysis

**Author:** John Strabel
**Institution:** Prague University of Economics and Business — Faculty of Finance and Accounting
**Supervisor:** Ing. Milan Fičura, Ph.D.
**Year of Defense:** 2026
**Length:** ~50 pages

---

## Abstract

This thesis investigates whether integrating social media sentiment velocity with earnings announcement timing produces statistically significant abnormal returns in U.S. equity markets. Using a novel dataset of 2,738,767 Reddit posts and comments from fifteen financial subreddits spanning 2010–2023, scored using FinBERT for sentiment polarity and matched to 115,518 SEC EDGAR earnings announcement dates for 281 S&P 500 constituents, the study conducts a post-earnings announcement drift (PEAD) event study.

**Results:**
- **H1** (sentiment predicts returns): Not supported
- **H2** (velocity spikes precede abnormal returns): Partially supported — moderate 3× velocity spikes followed by significant **negative** returns of −32 bps (noise-trading reversion, not predicted direction)
- **H3** (cross-sectional heterogeneity): Not supported
- **H4** (velocity amplifies PEAD): Not supported in predicted direction
- **ML models:** AUC-ROC of 0.520 on 2021–2023 test period
- **Feature importance:** Wikipedia page views (6.2%) and Google Trends (5.9%) outperform raw FinBERT sentiment scores

---

## Chapter 1 — Introduction

### 1.1 Motivation and Research Gap

Opens with the January 2021 GameStop short squeeze: mention velocity for GME exceeded 10× its 90-day baseline before markets opened; price surged from ~$20 to $480 intraday peak, inflicting ~$20B losses on institutional short sellers. This was a measurable, observable, predictable acceleration in social media attention preceding price movement by hours or days.

**Three gaps in existing literature:**
1. Existing work focuses on **sentiment level** (positive/negative tone), not **sentiment velocity** (rate of acceleration). A sustained positive signal may already be priced; a velocity spike represents novel, not-yet-incorporated information.
2. Sentiment signals are typically treated in isolation, without interaction with **fundamental information flows** (PEAD). Pre-announcement retail engagement may amplify or attenuate drift depending on alignment with the fundamental signal.
3. FinBERT and transformer-based NLP have not been fully exploited in the PEAD literature; dictionary-based approaches fail to capture contextual meaning in informal social media discourse.

### 1.2 Research Objectives

1. Construct a novel large-scale dataset integrating historical Reddit sentiment with earnings dates and equity prices
2. Empirically test four hypotheses about the predictive content of Reddit sentiment signals
3. Apply ML methods (Gu, Kelly & Xiu 2020) to determine optimal signal combination
4. Situate findings within market efficiency, behavioural finance, and ML asset pricing literature

### 1.3 Research Questions and Hypotheses

**Primary question:** Does integrating social media sentiment velocity with earnings announcement timing produce statistically significant abnormal returns in U.S. equity markets, and can ML methods determine optimal signal weights across stock characteristics?

| # | Hypothesis |
|---|---|
| H1 | Reddit FinBERT sentiment scores predict short-term equity returns (baseline) |
| H2 | Velocity spikes (7-day count / 90-day avg ≥ 3×, 5×, 10×) precede abnormal returns within 24–48hr |
| H3 | Sentiment predictive power is stronger in retail-dominated, smaller-cap, higher-volatility stocks |
| H4 | Stocks in top velocity quartile before announcements show amplified PEAD vs. top surprise quartile alone |

### 1.4 Scope and Delimitations

- **Universe:** Historical S&P 500 constituents 2010–2023 (survivorship-bias-free; 636 unique tickers, 301 with sufficient price data)
- **Sentiment source:** Reddit only (15 subreddits from r/wallstreetbets to r/SecurityAnalysis); Arctic Shift archive API
- **NLP model:** ProsusAI/finbert — known domain mismatch with informal Reddit text (trained on formal financial documents); results are conservative lower bounds
- **No live trading strategy, no transaction costs, no intraday execution**

---

## Chapter 2 — Literature Review

### 2.1 Market Efficiency and PEAD

- **EMH (Fama 1970):** Semi-strong form prices reflect all public information
- **Adaptive Markets Hypothesis (Lo 2004):** Markets evolve; mispricings persist until arbitraged away
- **Limits to arbitrage (Shleifer & Vishny 1997; De Long et al. 1990):** Noise trader risk prevents instantaneous price correction; allows sentiment-driven deviations to persist
- **Baker & Wurgler (2006):** Sentiment effects concentrated in stocks hard to value/arbitrage — small, volatile, unprofitable, non-dividend-paying
- **PEAD (Ball & Brown 1968; Bernard & Thomas 1989):** Prices continue drifting in direction of earnings surprise for 60 days post-announcement; mechanism is investor underreaction (Hirshleifer, Lim & Teoh 2009); weakening post-2000 (Jensen, Kelly & Pedersen 2023)
- **Piotroski (2000):** Financial statement signals predict returns, further evidence of incomplete price adjustment to public information

### 2.2 Social Media and Asset Prices

- **Antweiler & Frank (2004):** Yahoo Finance message board volume predicted stock volatility
- **Tetlock (2007):** Wall Street Journal pessimism predicted downward price pressure followed by mean reversion (noise trading)
- **Chen, De, Hu & Hwang (2014):** Seeking Alpha article sentiment predicted returns and earnings surprises; effect concentrated in low institutional ownership stocks
- **Betzer & Harries (2022):** WSB post volume predicted trading activity; no fundamental information — attention effect only
- **Warkulat & Pelster (2024):** WSB attention reduces holding period returns; positions at peak attention: −8.5% average return; driven by emotional responses (anger, disgust)
- **Bradley, Hanousek, Jame & Xiao (2024, RFS):** WSB posts predict returns through retail order flow, not fundamental information
- **Da, Engelberg & Gao (2011):** Google Trends ASVI predicts retail attention; top ASVI quintile followed by price run-up then reversal
- **Moat et al. (2013):** Wikipedia page views for financial topics precede stock market moves

### 2.3 Machine Learning in Asset Pricing

- **Gu, Kelly & Xiu (2020):** Gradient boosting and neural networks dominate OLS in out-of-sample return prediction; improvement concentrated in nonlinear interaction effects among predictors
- **Giglio, Kelly & Xiu (2022):** ML methods provide flexible estimates of conditional expected return function
- **Murray, Xia & Xiao (2024):** CNN-identified price patterns highly predictive; context independence across time scales/markets
- **Brogaard & Zareei (2023):** Gradient boosting generates ~1.0 Sharpe on long-short strategies; performance substantially higher with alternative data including sentiment
- **Ke, Kelly & Xiu (2021):** News text signals predict returns with efficiency delay varying with arbitrage costs — stronger for smaller, more volatile stocks

### 2.4 Financial NLP and FinBERT

**Three generations:**
1. Dictionary-based (Loughran & McDonald 2011) — interpretable but misses context, sarcasm, informal language
2. Supervised ML (SVM, random forest, CNN) — higher accuracy but requires domain-specific labelled data
3. Transformer-based — FinBERT (Huang, Wang & Yang 2023): pre-trained on 4.9B tokens of financial text, fine-tuned on 10,000 analyst report sentences; outperforms all prior methods

**FinBERT results on 2.74M Reddit mentions:** 83.6% neutral, 7.4% positive, 8.9% negative — consistent with documented negativity bias in retail investor discourse. Domain mismatch (trained on formal text, applied to informal Reddit) attenuates estimates toward zero; results are conservative lower bounds.

---

## Chapter 3 — Theoretical Framework

### 3.1 Information Flow in Equity Markets

Three categories of signal with distinct temporal footprints:
- **Fundamental** (low frequency): Earnings surprises at discrete announcement dates; long half-life (PEAD)
- **Technical** (high frequency): Continuous price momentum, volume patterns; encodes aggregated supply/demand history
- **Social sentiment/attention** (medium frequency): Near-real-time retail discourse; velocity (rate of change) more informative than level because sustained signals may already be priced

### 3.2 Hierarchical Signal Architecture

| Layer | Frequency | Signal |
|---|---|---|
| 1 — Valuation Anchor | Quarterly | Day-0 abnormal return (earnings surprise proxy = AR at announcement) |
| 2 — Sentiment/Attention | Daily | FinBERT net sentiment, mention velocity ratio, Google Trends, Wikipedia page views |
| 3 — Technical | Daily/Weekly | Beta, R² from 120-day pre-event market model (control variables) |

### 3.3 PEAD-Sentiment Interaction Model (H4)

Three channels through which pre-announcement velocity modifies PEAD:
1. **Attention amplification:** More retail investors attentive → more complete price adjustment at announcement → compressed PEAD underreaction
2. **Sentiment direction:** Bullish sentiment + positive surprise = amplified drift; bullish sentiment + negative surprise = sharper negative drift (forced revision)
3. **Informed trading:** Velocity spikes before earnings may partially reflect informed positioning ahead of positive news

**Formal prediction:** CAR[+1,+20] is increasing in both velocity quartile V(i,t) and surprise quartile S(i,t), with positive interaction (V=4, S=4 cell > V=1, S=4 cell)

### 3.4 Signal Fusion via Machine Learning

ML allows optimal signal weights to be learned from data rather than imposed a priori, capturing nonlinear interactions (e.g., velocity × earnings surprise). Gradient boosting: natural for interaction effects; feature importance reveals which signal layer contributes most.

---

## Chapter 4 — Data and Methodology

### 4.1 Data Sources

**Equity prices:** Daily OHLCV for 302 historical S&P 500 constituents via Stooq/pandas_datareader; 1,022,569 observations; survivorship-bias-free

**Reddit sentiment:** 2,738,767 mentions from 15 subreddits via Arctic Shift archive API; custom ticker extraction with 496-term blacklist; temporal range 2010–2023; non-stationary volume (557 mentions in 2010 → 1,070,608 peak in 2021 → 221,102 in 2023); velocity ratios computed at ticker level over rolling 90-day windows

**Top subreddits by mentions:** r/wallstreetbets (911,602), r/Superstonk (362,859), r/stocks (290,990), r/pennystocks (267,463), r/RobinHood (201,217)

**Earnings dates:** 115,518 filings from SEC EDGAR (CIK-to-ticker mapping); 8-K (89,675), 10-Q (19,414), 10-K (6,429); filing date used as t=0

**Google Trends:** 158,542 observations; weekly relative search interest (0–100); collected via pytrends in 5-year chunks; Finance category, US geography

**Wikipedia:** 820,302 daily page view observations via Wikimedia REST API; available from July 2015; company article titles matched to tickers via EDGAR company names

### 4.2 Variable Construction

**Dependent variable:** CAR[+1,+20] — Cumulative Abnormal Return over 20 trading days post-announcement; computed using market model (SPY as benchmark) estimated over 120-day pre-event window [-120, -21] relative to announcement date

**Key independent variables:**
- `velocity_ratio` = 7-day rolling mention count / 90-day baseline daily avg; thresholds: 3×, 5×, 10×
- `net_sentiment` = (% positive mentions − % negative mentions) in [-7, -1] pre-announcement window
- `surprise_day0` = AR on day 0 (market-based earnings surprise proxy; no analyst forecast data)

### 4.3 Empirical Design

**Event study:** CAR measured across pre-[-5,-1], announcement [0], and post-[+1,+5], [+1,+10], [+1,+20] windows

**H4 test:** 4×4 grid of surprise quartile × velocity quartile; t-tests comparing high-surprise/high-velocity vs. high-surprise/low-velocity cells

**ML approach:** Logistic regression, random forest, gradient boosting; train 2010–2020, test 2021–2023; 15 features across sentiment, velocity, attention, fundamental, and market layers; binary target (Q4 vs Q1 CAR[+1,+20])

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — central anomaly; event study anchor; H4 tests velocity interaction
- [[Sentiment Velocity]] — key novel signal; 7-day/90-day ratio; 3×/5×/10× spike thresholds
- [[FinBERT]] — sentiment scoring for 2.74M Reddit mentions; 83.6% neutral, domain mismatch caveat
- [[Efficient Market Hypothesis]] — theoretical context; AMH (Lo 2004) predicts exploitable mispricings
- [[Reddit as Financial Signal]] — primary data source; 15 subreddits; Arctic Shift archive
- [[Machine Learning in Asset Pricing]] — Gu, Kelly & Xiu (2020) framework; gradient boosting; feature importance analysis
