---
created: 2026-04-20
source_filename: "noise-a.pdf"
file_type: pdf
tags: [thesis-source, internet-message-boards, trading-volume, social-media, Antweiler-Frank]
---

# Antweiler & Frank (2002) — Is All That Talk Just Noise? The Information Content of Internet Stock Message Boards

**Full citation:** Antweiler, W. & Frank, M.Z. (2004). Is All That Talk Just Noise? The Information Content of Internet Stock Message Boards. *Journal of Finance*, 59(3), 1259–1294.

## Summary

Studies 1.5M+ messages on Yahoo! Finance and Raging Bull for 45 Dow Jones / Internet Index companies during 2000. Uses Naive Bayes and SVM computational linguistics methods to measure message bullishness. Finds message boards reflect day trader views: message volume predicts next-day trading volume and volatility; bullishness predicts returns modestly; agreement reduces volume.

## Key Arguments

1. **Message volume → trading volume:** Daily message count predicts next-day trading volume (attention-based mechanism) and volatility.
2. **Bullishness → returns:** Small but statistically significant relationship; not purely informational.
3. **Agreement → less volume:** More consensus among posters = less trading (uncertainty resolution).
4. **Day trader signal:** Message boards disproportionately reflect day traders; small-trade volume responds more than large-trade volume.
5. **Information vs. noise:** Cannot fully distinguish; evidence leans toward noise/attention rather than fundamental information.

## Key Quotes

> "An increase in the number of messages predicts a subsequent increase in trading volume and volatility; particularly marked is the surge in small size trades."

## Relevance to Thesis

- Direct predecessor to using Reddit as a financial signal source
- Methodology: NLP-based bullishness measurement parallels FinBERT sentiment scoring in thesis
- Antweiler & Frank's partial informativeness finding foreshadows thesis H1 null (Reddit sentiment p=0.72)
- Cited in Tetlock (2007) as empirical foundation for message-board sentiment research

## Key Concepts

- [[Reddit as Financial Signal]] — Yahoo! Finance boards are historical precursor to Reddit WSB
- [[FinBERT]] — NLP methods for sentiment classification, as in Antweiler & Frank's NLP approach
- [[Efficient Market Hypothesis]] — message board informativeness challenges semi-strong EMH
