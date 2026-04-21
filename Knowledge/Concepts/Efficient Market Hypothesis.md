---
created: 2026-04-20
tags: [concept, finance, market-efficiency, theory, EMH, behavioural-finance]
---

# Efficient Market Hypothesis (EMH)

## Definition

The EMH (Fama 1970) asserts that financial asset prices **fully and instantaneously incorporate all available information**. Under the **semi-strong form** (most relevant to this thesis), prices reflect all publicly available information including historical prices, accounting data, and published news — making it impossible to earn abnormal returns by trading on public information.

## Three Forms

| Form | What Prices Reflect |
|---|---|
| Weak | Historical price data only |
| Semi-strong | All publicly available information |
| Strong | All information (including private/insider) |

## Challenges and Extensions

**Anomaly literature** accumulated from the 1980s onward documenting patterns inconsistent with strict efficiency:
- Size effect (Banz 1981)
- Value premium (Fama & French 1992)
- Short-term momentum (Jegadeesh & Titman 1993)
- **Post-Earnings Announcement Drift** (Ball & Brown 1968; Bernard & Thomas 1989) — most relevant to thesis

**Adaptive Markets Hypothesis (Lo 2004):** Markets become more efficient as participants learn and arbitrage opportunities are exploited, but new mispricings emerge as the investor population and information landscape evolve. Predicts that attention-driven mispricings can persist for periods sufficient to be exploitable without markets being "fundamentally irrational."

**Limits to Arbitrage (Shleifer & Vishny 1997; De Long et al. 1990):** Even when rational investors identify mispricings, **noise trader risk** (the risk that mispricing worsens before correcting) imposes constraints on rational arbitrage, allowing sentiment-driven deviations to persist — especially in stocks that are costly to short, difficult to value, or predominantly held by retail investors.

## Relevance to Thesis

The thesis tests **limits of the semi-strong EMH** in the specific context of Reddit-driven retail attention and earnings announcements. The core question: if social media sentiment velocity signals are publicly observable, do they contain predictive information about subsequent abnormal returns?

**If H2 (velocity predicts abnormal returns) were strongly supported**, it would suggest prices do not immediately incorporate attention acceleration signals — consistent with the Adaptive Markets Hypothesis and limits-to-arbitrage framework. The actual result (3× velocity → −32 bps, consistent with noise-trading reversion) suggests markets do incorporate and *correct* attention-driven mispricings, but with a lag.

## Key Papers

- Fama, E.F. (1970). Efficient Capital Markets: A Review of Theory and Empirical Work. *Journal of Finance*, 25(2), 383–417.
- Lo, A.W. (2004). The Adaptive Markets Hypothesis. *Journal of Portfolio Management*, 30(5), 15–29.
- Shleifer, A., & Vishny, R.W. (1997). The Limits of Arbitrage. *Journal of Finance*, 52(1), 35–55.

## Appears In

- [[Thesis_Final]] — Section 2.1 (full theoretical treatment)
- [[Post-Earnings Announcement Drift]] — PEAD is the canonical anomaly inconsistent with semi-strong EMH
- [[Reddit as Financial Signal]] — attention signals as test of information incorporation speed
