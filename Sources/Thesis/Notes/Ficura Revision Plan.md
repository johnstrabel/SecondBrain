---
created: 2026-04-25
tags: [thesis, revisions, feedback, Ficura, VŠE, MIFA]
source: "[[Ficura's Reccommendations]]"
---

# Thesis Revision Plan — Ficura's Feedback

**Source:** [[Ficura's Reccommendations]]  
**Status:** In progress  
**Thesis:** Information Fusion in Financial Markets — ML-Based Sentiment Analysis for Equity Returns

---

## Quick Summary of What Ficura Said

- Thesis is "generally well written and methodologically sound" — baseline is good
- Main issues: survivorship bias framing, event date mismatch, missing interaction effects, ML variable concerns
- **Key reframe:** H4 result is NOT counter-intuitive — it's consistent with inattention bias literature. Promote it to a key finding.
- H2 and H4 are the two strongest results — both need strengthening, not defending

---

## Revision Tasks by Priority

---

### 🔴 PRIORITY 1 — Survivorship Bias (Sample Construction)

**Problem:** You claim the sample is survivorship-bias-free but ran analysis on 281 of 636 stocks with unclear reduction logic.

**Three specific issues to address:**

**Issue A — Missing Stooq data (301 → 281)**
- [ ] Explain *why* 335 stocks have no Stooq data
- [ ] Check: are the missing stocks predominantly delistings (bankruptcies/mergers)?
- [ ] If yes → acknowledge this likely introduces upward bias in returns; quantify or discuss magnitude

**Issue B — Full-period data requirement is non-standard**
- [ ] Remove or relax the requirement that stocks have data for the *entire* 2010–2023 period
- [ ] Acknowledge in methodology: this rule excludes stocks that started trading post-2010 and stocks that were delisted — the latter is exactly the survivorship bias concern
- [ ] Either rerun without this restriction, or add a dedicated limitation paragraph explaining the tradeoff

**Issue C — Correct survivorship-bias-free approach**
- [ ] For each earnings announcement at time *t*, include only stocks that were in the S&P 500 *at time t*
- [ ] This means a stock delisted in 2015 should appear in pre-2015 earnings events but not after
- [ ] Verify whether this filtering was actually applied in `build_event_study.py` — if not, it needs to be

---

### 🔴 PRIORITY 2 — Event Date Definition (Filing Date vs. Announcement Date)

**Problem:** SEC 8-K filing date ≠ earnings announcement date. Companies have up to 4 business days to file. Pre-announcement windows may actually be post-announcement for some stocks.

**Affects:** All four hypotheses (H1–H4) — sentiment/velocity "preceding" the announcement may actually be *concurrent with or after* the announcement for a subset of events.

**Fixes:**

- [ ] **Primary fix for H4:** Redefine "surprise return" as cumulative return from t−4 to t (guaranteed to include actual announcement date in all cases)
- [ ] **Robustness check (all hypotheses):** Identify proxy announcement date = day between t−4 and t with highest trading volume; rerun key analyses using this proxy
- [ ] Add a paragraph to the methodology section acknowledging the filing date limitation and explaining both fixes
- [ ] Report robustness results in an appendix or footnote table

---

### 🔴 PRIORITY 3 — H2 Bivariate Split (Baseline × Velocity)

**Problem:** The non-monotone result (3× spike significant and negative; 5× and 10× insignificant) is likely driven by baseline attention level confounding. Velocity=3 from 100→300 mentions is fundamentally different from 1→4. The 0.1 floor replacement makes any single mention produce velocity=10 — inflating the extreme spike group with low-attention stocks.

**Fixes:**

- [ ] Implement **bivariate split:** Baseline Attention Level (low/medium/high) × Attention Velocity (3×/5×/10×)
  - Suggested baseline splits: <10 mentions/day avg, 10–100, >100
  - Report CAR results for each cell of this grid
- [ ] Check whether the 3× spike negative result disappears or strengthens in high-baseline stocks vs low-baseline stocks — this will clarify the mechanism
- [ ] Review the 0.1 floor for zero-mention baselines — consider excluding zero-baseline events entirely or reporting results with and without them
- [ ] Run the same velocity analysis using **Google Trends** and **Wikipedia PageViews** as alternative attention metrics
  - If results are directionally consistent across all three → much stronger conclusion
  - If results diverge → informative about what the Reddit signal specifically captures

---

### 🟡 PRIORITY 4 — H4 Reframe + Inattention Literature + Statistical Significance

**Key insight from Ficura:** Low attention velocity increasing PEAD strength is *not* counter-intuitive — it is consistent with the **investor inattention / gradual information transmission** literature. This is a finding to promote, not explain away.

**Reframe tasks:**

- [ ] Add a literature review section on **investor inattention bias** — suggested papers to find and cite:
  - Hirshleifer & Teoh (2003) — limited attention and information processing
  - DellaVigna & Pollet (2009) — inattention and Friday earnings announcements
  - Hirshleifer, Lim & Teoh (2009) — already in thesis; expand the discussion
  - Hou, Peng & Xiong (2009) — limited attention and momentum
- [ ] Rewrite H4 conclusion: the result is *consistent with* inattention bias — low-velocity stocks fly under the radar → information diffuses slowly → stronger PEAD
- [ ] Promote H4 to **key finding** in abstract, introduction, and conclusions (alongside H2)

**Statistical significance fixes:**

- [ ] Add statistical significance columns (t-stats or p-values) to Table 4 (H4 grid)
- [ ] Show that low-velocity quartile CAR differences are statistically significant, not just directionally interesting

**Additional H4 analyses:**

- [ ] Add baseline attention level analysis: does the H4 inattention effect concentrate in low-baseline-attention stocks?
- [ ] Rerun H4 with alternative surprise return definitions (t−4 to t return; max-volume-day proxy)
- [ ] Add robustness: rerun H4 using Google Trends and Wikipedia velocity metrics

---

### 🟡 PRIORITY 5 — H1 Sentiment × Attention Interaction

**Problem:** Sentiment computed from 100 posts carries very different information than sentiment from 1 post. Analysing sentiment in isolation ignores this.

**Fixes:**

- [ ] Clarify in writing the exact difference between **Net Sentiment** (P(pos) − P(neg)) and **Average Sentiment Score** (mean of FinBERT confidence scores) — make this explicit in the methodology
- [ ] Split H1 analysis into sub-samples by number of posts in the sentiment window:
  - Low attention (e.g. 1–10 posts), medium (11–100), high (>100)
  - Report sentiment-return relationship separately for each group
- [ ] Test interaction term: sentiment × attention velocity in a single regression instead of separate univariate analyses
- [ ] Report whether H1 becomes significant in the high-attention sub-sample (hypothesis: it might)

---

### 🟡 PRIORITY 6 — ML Models (Technical Fixes)

**Issue A — Binary target definition is unclear**
- [ ] Clarify in writing: Q2 and Q3 observations were *excluded* from the binary classification (only Q1 and Q4 retained) — or explain how they were classified if they were included
- [ ] Add exact sample sizes for each class in the binary model

**Issue B — Log-price forward-looking bias (Critical)**
- [ ] Determine whether **split-adjusted** or **unadjusted** prices were used for log-price feature
- [ ] If split-adjusted: stocks with many historical splits will have low current adjusted prices — this encodes future price appreciation into the feature, creating forward-looking bias
- [ ] Fix: use **unadjusted price** at the time of the earnings announcement, or use price-to-index ratio instead of raw price
- [ ] Rerun feature importance after fixing — if log-price drops significantly, that confirms the bias was real

**Issue C — Volume transformation**
- [ ] Transform volume from shares traded to **USD volume** (shares × closing price) to make it comparable across stocks and over time
- [ ] Rerun model with corrected volume feature

**Issue D — Model documentation**
- [ ] Add: hyperparameter settings used for Random Forest, Gradient Boosting, Logistic Regression
- [ ] Add: metric used to assess variable importance (Gini impurity / permutation importance / SHAP?)
- [ ] Add: train/test split dates explicitly

**Issue E — Out-of-sample backtest**
- [ ] Implement a simple trading strategy based on ML model predictions (e.g. long Q4 predicted, short Q1 predicted)
- [ ] Report: equity curve over the out-of-sample period, Sharpe ratio, max drawdown, annualised return
- [ ] This transforms the ML section from "we built a model" to "here is whether it works in practice"

---

### 🟠 PRIORITY 7 — H3 Cross-Sectional Extension

**Problem:** Currently only tests cross-sectional behaviour of sentiment (which was insignificant). Needs to be broadened.

**Fixes:**

- [ ] Add cross-sectional analysis of **attention spike effects** (not just sentiment)
  - Does the H2 negative velocity effect concentrate in small-cap stocks? Low-analyst-coverage stocks? High retail ownership?
- [ ] Incorporate baseline attention level as an additional cross-sectional variable in H3
- [ ] Check whether attention spike effects interact with firm size, institutional ownership, or analyst coverage

---

## Revision Order (Suggested Sequence)

| Week | Tasks |
|---|---|
| **Week 1** | Survivorship bias writeup (clarify what happened, acknowledge limitation); Event date methodology section; H4 reframe + inattention literature search |
| **Week 2** | H2 bivariate split (code + results); H4 alternative surprise return + significance table |
| **Week 3** | ML binary target clarification; log-price bias check + rerun; volume fix |
| **Week 4** | H1 interaction analysis; H3 extension; Google Trends/Wikipedia robustness checks |
| **Week 5** | ML backtest; abstract/intro/conclusions rewrite to reflect H4 promotion; final proofread |

---

## Key Reframes to Make Throughout

| Before | After |
|---|---|
| "H4 result was counter-intuitive and unexpected" | "H4 result is consistent with investor inattention literature — low-velocity stocks diffuse information slowly, sustaining PEAD" |
| "H1 and H2 were not supported" | "H2 and H4 are the key findings; H1 non-result is informative about FinBERT domain mismatch" |
| "Sample is survivorship-bias-free" | "Sample construction involves tradeoffs; we acknowledge potential residual bias and discuss its likely direction" |
| "ML model shows AUC of 0.520" | "ML model marginally beats random — consistent with weak-form market efficiency; backtest confirms limited practical signal" |

---

## Files to Modify

- `Thesis_Final (3).docx` — main document
- `build_event_study.py` — survivorship bias filter, event date proxy
- `run_analysis.py` — H1/H2/H3/H4 bivariate splits, interaction terms
- `ml_model.py` — binary target clarification, volume fix, log-price fix, backtest
