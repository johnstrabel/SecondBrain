## Final Thesis — Complete Section Status

|#|Section|Status|What Changes|
|---|---|---|---|
|—|**Abstract**|🟡 Minor update|Update H2 result (t=4.67), reframe H4 as inattention-consistent, add backtest result|
|—|**Declaration / Acknowledgments / Keywords**|✅ Done|No changes|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**1**|**Introduction**|||
|1.1|Motivation and Research Gap|✅ Done|No changes|
|1.2|Research Objectives|✅ Done|No changes|
|1.3|Research Questions and Hypotheses|✅ Done|No changes|
|1.4|Scope and Delimitations|✅ Done|No changes|
|1.5|Structure of the Thesis|🟡 Minor update|One sentence to reflect new subsections in Ch. 5|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**2**|**Literature Review**|||
|2.1|Market Efficiency, Behavioural Finance, and PEAD|||
|2.1.1|The Efficient Market Hypothesis and Its Limits|✅ Done|No changes|
|2.1.2|Investor Sentiment and the Cross-Section of Returns|✅ Done|No changes|
|2.1.3|Post-Earnings Announcement Drift|✅ Done|No changes|
|2.1.4|**Investor Inattention and PEAD**|📝 **New section**|Fičura explicitly asked for this — DellaVigna & Pollet (2009), Hirshleifer et al. (2009), Hou et al. (2009). Explains the theoretical basis for H4 result|
|2.2|Social Media, Investor Attention, and Asset Prices|||
|2.2.1|Early Internet Sentiment Research|✅ Done|No changes|
|2.2.2|Reddit and the WallStreetBets Literature|✅ Done|No changes|
|2.2.3|Attention Proxies: Search Volume and Wikipedia|✅ Done|No changes|
|2.3|Machine Learning in Asset Pricing|||
|2.3.1|Gu, Kelly and Xiu (2020)|✅ Done|No changes|
|2.3.2|Murray, Xia and Xiao; Brogaard and Zareei|✅ Done|No changes|
|2.3.3|Ke, Kelly and Xiu (2021)|✅ Done|No changes|
|2.4|Financial NLP and FinBERT|✅ Done|No changes|
|2.5|Research Gap and Contribution|🟡 Minor update|Update to reflect inattention bias as theoretical anchor for H4|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**3**|**Theoretical Framework**|||
|3.1|Information Flow in Equity Markets|✅ Done|No changes|
|3.2|The Hierarchical Signal Architecture|✅ Done|No changes|
|3.2.1|Layer 1: Valuation Anchor|✅ Done|No changes|
|3.2.2|Layer 2: Sentiment and Attention|✅ Done|No changes|
|3.2.3|Layer 3: Technical Signals|✅ Done|No changes|
|3.3|The PEAD-Sentiment Interaction Model|🟡 Minor update|Add the inattention channel as a fourth mechanism alongside the three existing channels. One paragraph.|
|3.4|Signal Fusion and Machine Learning Weighting|✅ Done|No changes|
|3.5|Theoretical Predictions|🟡 Minor update|H4 prediction: reframe from "velocity amplifies drift" to "velocity modifies drift via the inattention channel" — dual directional prediction|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**4**|**Data and Methodology**|||
|4.1|Data Sources and Collection|||
|4.1.1|Equity Price Data|🟡 Minor update|Add survivorship bias diagnostic: 0 tickers end before 2020, 21 start after 2015 — explain what this means and why it creates conservative bias|
|4.1.2|Reddit Sentiment Data|✅ Done|No changes|
|4.1.3|Earnings Announcement Dates (SEC EDGAR)|🟡 Minor update|Add one paragraph on filing date ≠ announcement date — how this affects H1, H2, H3 windows, not just H4|
|4.1.4|Supplementary Attention Signals|✅ Done|No changes|
|4.2|Variable Construction|||
|4.2.1|Dependent Variable: CARs|✅ Done|No changes|
|4.2.2|Sentiment and Velocity Features|🟡 Minor update|Add: definition of the four attention level categories (zero / low / medium / high baseline tertiles)|
|4.2.3|Earnings Surprise Proxy|🟡 Minor update|Add: CAR[−4,0] alternative surprise definition and motivation|
|4.2.4|Control Variables|🟡 Minor update|Add: within-year price rank replaces raw log_price (V2); log USD volume replaces share count log_volume (V2). One paragraph explaining both fixes and why they are methodologically superior|
|4.3|Empirical Design|||
|4.3.1|Event Study: PEAD and Sentiment Interaction|✅ Done|No changes|
|4.3.2|H1, H2, and H3 Tests|🟡 Minor update|Add: description of the bivariate split methodology (attention level × velocity) and the attention-level sub-sample approach for H1|
|4.3.3|Machine Learning Return Prediction|🟡 Minor update|Add: one sentence clarifying Q2/Q3 are excluded from binary target; one sentence on hyperparameters; one sentence on Gini importance metric|
|4.4|Data Quality and Limitations|🔴 **Rewrite**|Survivorship bias paragraph (written above) is substantially new. Event date limitation needs expansion to cover H1-H3. Both are new content replacing the original paragraph.|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**5**|**Empirical Results**|||
|5.1|Descriptive Statistics|||
|5.1.1|Dataset Overview|✅ Done|No changes|
|5.1.2|Sentiment and Velocity Distribution|🟡 Minor update|Add one sentence on the four attention level group sizes (zero=54,183 / low=6,070 / medium=6,070 / high=6,071)|
|5.1.3|Temporal Patterns|✅ Done|No changes|
|5.2|H1: Sentiment Scores and Short-Term Returns|🟡 Minor update|Add one paragraph at the end on the moderate-posts finding (β=−0.0089, t=−2.56, p=0.010). Table 2 stays, prose expands slightly.|
|5.3|H2: Velocity Spikes and Abnormal Price Movements|🔴 **Major rewrite**|Bivariate table becomes the headline finding. New Table 3b. The univariate result (now t=3.13, p=0.002) becomes the preamble. Zero-attention null interpretation. The whole section restructures around the bivariate result.|
|5.4|H3: Cross-Sectional Heterogeneity|🔴 **Major rewrite**|Currently only covers sentiment cross-sectional. Add new subsection 5.4.2 on attention spike cross-sectional (small stocks p=0.003, high-beta p=0.001). The velocity spike results are now the main H3 finding; sentiment cross-sectional becomes secondary.|
|5.5|H4: Pre-Earnings Sentiment Velocity and PEAD|🔴 **Major rewrite**|Replace Table 4 with the new version including t-statistics. Add the CAR[−4,0] alternative surprise grid. Add Google Trends robustness (p=0.015). Reframe the whole section using inattention bias from the opening sentence.|
|5.6|Machine Learning Return Prediction|🔴 **Substantial rewrite**|Add V1 vs V2 feature fix comparison table. Update feature importance discussion (log_price_rank replaces log_price — result unchanged, confirms no forward bias). Add backtest paragraph (+41 bps per position, win rate 51.5%, approximate Sharpe 0.60).|
|5.7|Robustness|🟡 Minor update|Reference the new robustness checks already run (alternative surprise, Google Trends, attention-level splits, exclusion of 2021) as a consolidated paragraph|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**6**|**Discussion**|||
|6.1|Interpretation of Results|🔴 **Major rewrite**|H4 must be reframed as inattention-consistent rather than counterintuitive. H2 bivariate result needs its own paragraph. H3 cross-sectional velocity results need interpretation through Baker & Wurgler limits-to-arbitrage lens. The whole section is reorganised around the new findings.|
|6.2|Contribution to the Literature|🟡 Minor update|Update to claim the bivariate H2 finding and the inattention-consistent H4 evidence as contributions. One paragraph rework.|
|6.3|Practical Implications|🟡 Minor update|Add: bivariate signal (high baseline attention + 3× spike = contrarian sell signal). Add: ML backtest as evidence of modest implementable signal.|
|6.4|Limitations|🔴 **Rewrite**|Survivorship bias paragraph is entirely new (written above). Event date limitation expanded to cover all four hypotheses, not just H4. FinBERT domain mismatch stays.|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|**7**|**Conclusion**|||
|7.1|Summary of Findings|🔴 **Rewrite**|H2 summary upgrades to t=4.67 in high-attention stocks. H3 summary adds velocity cross-sectional results. H4 summary drops "not supported in predicted direction" and replaces with inattention-consistent framing. ML summary adds backtest.|
|7.2|Answers to the Research Questions|🟡 Minor update|H4 answer changes from qualified negative to qualified positive under inattention lens. ML answer stays.|
|7.3|Future Research Directions|🟡 Minor update|Add: proper survivorship-bias-free replication as explicit future direction. Add: intraday announcement timestamp as future direction (already hinted at).|

---

|#|Section|Status|What Changes|
|---|---|---|---|
|—|**Bibliography**|🟡 Minor update|Add DellaVigna & Pollet (2009), Hou, Peng & Xiong (2009)|
|—|**List of Tables**|🟡 Minor update|Add Table 3b (bivariate H2), Table 4b (H4 with t-stats), Table 7 (V1/V2 ML comparison), Table 8 (Backtest summary)|

---

## Summary by effort

|Category|Sections|Count|
|---|---|---|
|🔴 **Needs full rewrite**|4.4, 5.3, 5.4, 5.5, 5.6, 6.1, 6.4, 7.1|8 sections|
|📝 **New section needed**|2.1.4 (Inattention bias lit review)|1 section|
|🟡 **Minor updates**|Abstract, 1.5, 2.5, 3.3, 3.5, 4.1.1, 4.1.3, 4.2.2, 4.2.3, 4.2.4, 4.3.2, 4.3.3, 5.1.2, 5.2, 5.7, 6.2, 6.3, 7.2, 7.3, Bibliography, List of Tables|21 sections|
|✅ **No changes**|Everything else|~18 sections|

The 8 rewrites and 1 new section are the core of what remains. Which do you want to start with?