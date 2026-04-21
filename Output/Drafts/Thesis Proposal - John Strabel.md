---
created: 2026-04-20
source_filename: "Thesis Proposal - John Strabel (4).docx"
file_type: docx
tags: [thesis, proposal, sentiment-analysis, PEAD, machine-learning, reddit, finbert]
---

# Thesis Proposal — John Strabel

**Prague University of Economics and Business**
Faculty of Business Administration | Masters in Finance and Accounting (MIFA) | Trading and Valuation
Supervisor: Ing. Milan Fičura, Ph.D.

---

## Proposed Title

**Information Fusion in Financial Markets: A Hierarchical Framework for Combining Social Sentiment, Fundamental Valuation, and Technical Analysis**

---

## Brief Topic

**Theoretical:** Develops a hierarchical framework integrating social sentiment, fundamental valuation, and technical signals for equity trading, where each signal serves a distinct role in the decision process.

**Methodological:** Combines multiple sentiment sources (Reddit, Seeking Alpha, Google Trends, StockTwits) with earnings announcement data; applies machine learning to determine optimal signal weights across stock characteristics.

**Empirical:** Uses S&P index constituents (including delisted stocks) from 2010–2023. Model trained on 2010–2020, validated on 2021–2023 — tests whether sentiment velocity spikes predict abnormal returns.

---

## Research Questions

- Do Reddit-derived sentiment velocity signals contain predictive information about post-earnings announcement drift?
- Can machine learning methods determine optimal signal weights across stock characteristics?

---

## Key Hypotheses

| Hypothesis | Claim |
|---|---|
| H1 | FinBERT Reddit sentiment scores predict short-term equity returns |
| H2 | Mention velocity spikes (7-day vs 90-day baseline: 3×/5×/10×) precede abnormal returns in 24–48hr window |
| H3 | Sentiment predictive power is stronger in smaller-cap, higher-volatility, retail-dominated stocks |
| H4 | Pre-announcement velocity amplifies post-earnings announcement drift (PEAD) |

---

## Dataset

- **Reddit mentions:** 2.74M posts/comments from 15 financial subreddits (2010–2023)
- **Sentiment scoring:** FinBERT (ProsusAI/finbert via HuggingFace)
- **Earnings dates:** 115,518 filings from SEC EDGAR (8-K, 10-Q, 10-K)
- **Price data:** S&P 500 historical constituents (survivorship-bias-free), 281 tickers
- **Attention proxies:** Google Trends (158,542 obs), Wikipedia page views (820,302 obs)

---

## Bibliography (Key References)

- Gu, S., Kelly, B., & Xiu, D. (2020). Empirical Asset Pricing via Machine Learning. *Review of Financial Studies*, 33(5), 2223–2273.
- Murray, S., Xia, Y., & Xiao, H. (2024). Charting by Machines. *Journal of Financial Economics*, 153, 103791.
- Brogaard, J., & Zareei, A. (2023). Machine Learning and the Stock Market. *Journal of Financial and Quantitative Analysis*, 58(4), 1431–1472.
- Giglio, S., Kelly, B., & Xiu, D. (2022). Factor Models, Machine Learning, and Asset Pricing. *Annual Review of Financial Economics*, 14, 337–368.
- Huang, A.H., Wang, H., & Yang, Y. (2023). FinBERT: A Large Language Model for Extracting Information from Financial Text. *Contemporary Accounting Research*, 40(2), 1311–1350.
- Chen, H., De, P., Hu, Y.J., & Hwang, B.H. (2014). Wisdom of Crowds: The Value of Stock Opinions Transmitted Through Social Media. *Review of Financial Studies*, 27(5), 1367–1403.

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — the empirical anchor for H4; PEAD as a baseline anomaly
- [[Sentiment Velocity]] — rate of change of Reddit mention volume (7-day/90-day ratio); central novel signal
- [[FinBERT]] — transformer model for financial text sentiment scoring
- [[Efficient Market Hypothesis]] — theoretical context; thesis tests limits of semi-strong form
- [[Reddit as Financial Signal]] — primary data source; WallStreetBets and 14 other subreddits
- [[Machine Learning in Asset Pricing]] — framework from Gu, Kelly & Xiu (2020); gradient boosting for signal fusion
