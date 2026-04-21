---
created: 2026-04-20
source_filename: "campbellshiller88.pdf"
file_type: pdf
tags: [thesis-source, stock-prices, dividends, earnings, present-value, Campbell-Shiller, JF]
---

# Campbell & Shiller (1988) — Stock Prices, Earnings, and Expected Dividends

**Full citation:** Campbell, J.Y. & Shiller, R.J. (1988). Stock Prices, Earnings, and Expected Dividends. *Journal of Finance*, 43(3), 661–676.

## Summary

Using U.S. aggregate stock market data 1871–1986, shows that long historical averages of real earnings help forecast the present value of future dividends. A VAR-based forecast of PV of dividends is roughly a weighted average of long-run earnings (2/3–3/4 weight) and current price. Demonstrates that excess volatility in stock prices is linked to predictability of multiperiod returns — both phenomena are "one and the same."

## Key Arguments

1. **Dividend-price predictability:** Dividend yield and smoothed earnings-price ratio predict long-horizon returns; one-period returns are far less predictable than multi-period returns.
2. **Excess volatility:** Stock prices are too volatile to be justified by news about fundamentals alone (supports Shiller 1981).
3. **VAR methodology:** Log-linear present-value decomposition allows decomposing return news into cash-flow news and discount-rate news.
4. **Unified result:** Excess volatility and long-horizon return predictability are not separate phenomena but two sides of the same coin.
5. **Earnings as predictor:** 10-year smoothed earnings (CAPE precursor) better reflects long-run fundamental value than current price.

## Relevance to Thesis

- Provides theoretical and empirical background for the thesis's fundamental valuation pillar
- Long-run mean reversion of prices is the "reversion to fundamentals" mechanism cited alongside Tetlock (2007) for H2's noise-trading reversion result
- Motivates use of price and volume features in the ML model (log_price, log_volume dominate feature importance)

## Key Concepts

- [[Efficient Market Hypothesis]] — excess volatility and long-horizon predictability challenge EMH
- [[Machine Learning in Asset Pricing]] — VAR-based prediction is a forerunner of ML return prediction
