---
created: 2026-04-20
source_filename: "Thesis_Template_Format.docx"
file_type: docx
tags: [thesis, formatted-submission, VŠE-template, sentiment-analysis, PEAD]
---

# Information Fusion in Financial Markets
## Formatted Submission Draft (VŠE Template)

**Author:** John Strabel
**Faculty:** Faculty of Finance and Accounting, Department of Banking and Insurance
**Study Programme:** Finance and Accounting (MIFA)
**Supervisor:** Ing. Milan Fičura, Ph.D.
**Year of Defense:** 2026

> This file is the VŠE-formatted submission version of the thesis. Compare with [[Thesis_Final]] for the working draft. The structured chapters here are a more condensed version of the full argument.

---

## Abstract

This thesis investigates whether integrating social media sentiment velocity with earnings announcement timing produces statistically significant abnormal returns in U.S. equity markets. Using a novel dataset of 2,738,767 Reddit posts and comments from fifteen financial subreddits spanning 2010–2023, scored using FinBERT for sentiment polarity and matched to 115,518 SEC EDGAR earnings announcement dates for 281 S&P 500 constituents, the study conducts a post-earnings announcement drift (PEAD) event study. Four hypotheses are tested: that FinBERT sentiment scores predict short-term returns (H1); that mention velocity spikes precede abnormal price movements (H2); that sentiment effects vary systematically with stock characteristics (H3); and that pre-announcement velocity amplifies post-announcement drift (H4).

**H1 and H3 are not supported. H2 is partially supported: moderate 3× velocity spikes are followed by significant negative returns of −32 basis points, consistent with noise-trading reversion. H4 is not supported in the predicted direction. Machine learning models achieve AUC-ROC of 0.520 on the 2021–2023 test period. Feature importance analysis reveals that attention signals (Wikipedia page views, Google Trends) outperform raw FinBERT sentiment scores.**

**Keywords:** information fusion · social media sentiment · Reddit · FinBERT · post-earnings announcement drift · machine learning · attention signals · velocity spikes · event study · U.S. equities

---

## Acknowledgments

Gratitude to supervisor Ing. Milan Fičura, Ph.D. for expert guidance. Thanks to Prague University of Economics and Business for providing the academic environment.

---

## Structure Overview

| Chapter | Title |
|---|---|
| 1 | Introduction — Motivation, Research Gap, Objectives, Hypotheses, Scope |
| 2 | Literature Review — EMH/PEAD, Social Media, Machine Learning, FinBERT |
| 3 | Theoretical Framework — Hierarchical Signal Architecture, PEAD-Sentiment Interaction |
| 4 | Data and Methodology — Data Sources, Variables, Event Study Design |
| 5 | Empirical Results — Descriptive Stats, H1–H4 Tests, ML Evaluation |
| 6 | Discussion — Findings Interpretation, Practical Implications |
| 7 | Conclusions |

---

## Selected Chapter Content

### Chapter 1 — Introduction

**Central motivation:** GameStop January 2021 — GME mention velocity exceeded 10× its 90-day baseline before markets opened; price surged to $480 from $20 in 6 trading sessions. The episode was the product of measurable, observable attention acceleration — not random noise.

**Three literature gaps:**
1. Existing work measures **sentiment level** (positive/negative); not **velocity** (rate of acceleration)
2. Sentiment treated in isolation, without interaction with PEAD (fundamental information flows)
3. Transformer-based NLP (FinBERT) not yet fully exploited in PEAD literature

### Chapter 2 — Literature Review Summary

See [[Thesis_Final]] for complete literature review notes.

Key anchor papers:
- Baker & Wurgler (2006) — sentiment effects concentrated in stocks difficult to value/arbitrage
- Ball & Brown (1968); Bernard & Thomas (1989) — PEAD discovery and characterization
- Gu, Kelly & Xiu (2020) — ML asset pricing methodology anchor
- Huang, Wang & Yang (2023) — FinBERT development and validation

### Chapter 3 — Theoretical Framework

**Hierarchical signal architecture:**
- Layer 1 (Quarterly): Valuation anchor — Day-0 abnormal return as earnings surprise proxy
- Layer 2 (Daily): Sentiment & attention — FinBERT scores, velocity ratio, Google Trends, Wikipedia
- Layer 3 (High-frequency): Technical controls — beta, R² from 120-day estimation window

**PEAD-Sentiment Interaction Model:** Pre-announcement velocity modifies PEAD through three channels: (1) attention amplification, (2) sentiment direction alignment, (3) potential informed trading signal

---

## Key Concepts

- [[Post-Earnings Announcement Drift]] — core anomaly tested
- [[Sentiment Velocity]] — novel signal; 7-day/90-day rolling ratio
- [[FinBERT]] — sentiment scoring; 83.6% neutral on Reddit corpus
- [[Efficient Market Hypothesis]] — theoretical backdrop
- [[Reddit as Financial Signal]] — primary data source
- [[Machine Learning in Asset Pricing]] — Gu, Kelly & Xiu (2020) framework
