---
created: 2026-04-20
tags: [concept, finance, anomaly, PEAD, event-study, behavioural-finance]
---

# Post-Earnings Announcement Drift (PEAD)

## Definition

The tendency for stock prices to **continue drifting in the direction of an earnings surprise for weeks after the announcement**, rather than fully adjusting at the time of the news. One of the most extensively documented and replicated anomalies in the asset pricing literature.

A zero-investment strategy of buying positive-surprise stocks and short-selling negative-surprise stocks earned economically and statistically significant abnormal returns over the 60 trading days following announcement (Bernard & Thomas 1989).

## Core References

- **Ball & Brown (1968)** — First identified PEAD in annual earnings announcement data; prices did not instantaneously adjust to earnings information
- **Bernard & Thomas (1989)** — Definitive characterisation; demonstrated 60-day post-announcement drift with significant risk-adjusted returns
- **Hirshleifer, Lim & Teoh (2009)** — Limited attention hypothesis: investor underreaction concentrated in periods of high information load (many simultaneous announcements)
- **Jensen, Kelly & Pedersen (2023)** — PEAD has weakened substantially post-2000 as the academic literature drew attention to the anomaly (partially arbitraged away)

## Proposed Explanations

| Explanation | Summary |
|---|---|
| **Limited attention** | Investors have finite cognitive capacity; underreact when overloaded with announcements |
| **Transaction costs** | High turnover and short-selling costs eliminate apparent profit opportunity |
| **Risk premium** | PEAD reflects compensation for unidentified systematic risk (sceptical consensus) |
| **Post-2000 weakening** | Academic publication partially arbitraged the anomaly (Jensen et al. 2023) |

## Relationship to Thesis

PEAD is the **empirical anchor** for the thesis "Information Fusion in Financial Markets." Every event study calculation is structured around earnings announcement dates (t=0 from SEC EDGAR). Hypothesis H4 tests whether pre-announcement Reddit sentiment velocity **amplifies** PEAD — specifically whether the CAR[+1,+20] interaction of velocity quartile × earnings surprise quartile produces a positive interaction effect.

**Key result from thesis (H4 NOT supported):** Pre-announcement velocity does not amplify PEAD in the predicted direction. Moderate 3× velocity spikes were followed by significant *negative* returns of −32 bps — consistent with noise-trading reversion rather than informed accumulation.

## Event Windows Used in Thesis

| Window | Symbol | Days |
|---|---|---|
| Estimation | — | [-120, -21] |
| Pre-announcement | CAR_pre | [-5, -1] |
| Announcement | AR_day0 | [0] |
| Post-5 | CAR_post_5 | [+1, +5] |
| Post-10 | CAR_post_10 | [+1, +10] |
| Post-20 | CAR_post_20 | [+1, +20] |

## Appears In

- [[Thesis_Final]] — Chapter 2.1.3, Chapter 3.3 (theoretical model), Chapter 5 (hypothesis tests)
- [[Thesis Proposal - John Strabel]] — Core empirical design
- [[build_event_study]] — computes all CARs
- [[run_analysis]] — tests H1–H4 against PEAD framework
- [[Earnings Dates]] — provides t=0 dates
