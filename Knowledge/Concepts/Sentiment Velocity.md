---
created: 2026-04-20
tags: [concept, finance, sentiment-analysis, social-media, novel-signal, thesis]
---

# Sentiment Velocity

## Definition

The **rate of change of social media attention**, measured as the ratio of recent mention activity to a rolling historical baseline. Distinct from *sentiment level* (positive/negative tone): a sustained positive signal may already be priced, while an **acceleration** in attention signals emerging interest not yet incorporated.

## Formula

```
velocity_ratio = (7-day rolling mention count) / (90-day rolling baseline daily avg)
```

**Spike thresholds:**
- **3×** — moderate acceleration
- **5×** — significant acceleration
- **10×** — extreme event (characteristic of meme stock events)

## Motivation

The January 2021 GameStop episode illustrates the concept: GME had sustained positive sentiment for months, but the **velocity spike** (10× baseline acceleration in days before the price explosion) was the actionable event. Level-based signals would not have captured this.

**Theoretical basis:**
- **Barber & Odean (2008)** — retail investors disproportionately buy attention-grabbing stocks, regardless of sentiment direction → velocity predicts retail buying pressure through the attention mechanism
- **Baker & Wurgler (2006)** — sentiment effects concentrated in stocks most susceptible to noise trading

## Implementation in Thesis

Computed in `build_event_study.py` for each earnings event, looking at the 7-day window [-7, -1] before announcement date:

```python
count_7d      = len(mentions in last 7 days)
daily_avg_90d = len(mentions over prior 90 days) / 90
velocity_ratio = count_7d / max(daily_avg_90d, 0.1)

velocity_spike_3x  = velocity_ratio >= 3
velocity_spike_5x  = velocity_ratio >= 5
velocity_spike_10x = velocity_ratio >= 10
```

**Why rolling baselines matter:** Reddit mention volume grew from 557 in 2010 to 1,070,608 in 2021 — absolute counts are non-stationary. Rolling baselines make velocity ratios comparable across years.

## Thesis Results (H2 — Partially Supported)

- **3× velocity spikes → −32 bps CAR[+1,+20]** (significant, but *negative* — noise-trading reversion)
- H4 (velocity amplifies PEAD) not supported in predicted direction
- Feature importance: `velocity_ratio` and `log_mentions` appear in the ML model but attention proxies (Wikipedia, Google Trends) outperform raw Reddit velocity

## Appears In

- [[Thesis_Final]] — Sections 1.1, 2.2, 3.2, 3.3, Chapter 4-5
- [[Thesis Proposal - John Strabel]] — Central novel signal
- [[build_event_study]] — computes velocity_ratio and spike flags
- [[run_analysis]] — H2 spike analysis, H4 interaction grid
- [[ml_model]] — velocity_ratio and log_mentions as features
- [[Reddit Dataset Summary Stats]] — shows 2021 non-stationarity
