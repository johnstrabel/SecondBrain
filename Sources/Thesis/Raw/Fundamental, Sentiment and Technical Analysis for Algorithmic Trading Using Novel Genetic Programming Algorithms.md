---
created: 2026-04-20
source_filename: "Fundamental, Sentiment and Technical Analysis for Algorithmic Trading Using Novel Genetic Programming Algorithms.pdf"
file_type: pdf
tags: [thesis-source, genetic-programming, fundamental-analysis, technical-analysis, sentiment, algorithmic-trading, Christodoulaki, PhD-thesis]
---

# Christodoulaki (2024) — Fundamental, Sentiment and Technical Analysis for Algorithmic Trading Using Novel Genetic Programming Algorithms

**Full citation:** Christodoulaki, E.P. (2024). Fundamental, Sentiment and Technical Analysis for Algorithmic Trading Using Novel Genetic Programming Algorithms. PhD thesis, University of Essex, School of Computer Science and Electronic Engineering.

## Summary

PhD thesis exploring genetic programming (GP) applications in algorithmic trading, combining FA, SA, and TA indicators within novel GP frameworks. Proposes novel fitness functions and GP operators that encourage active trading at low risk. Tests on 42 international companies. Demonstrates that integrating all three analysis types improves financial profitability compared to using each type alone.

## Key Arguments

1. **Tri-signal GP framework:** Novel GP variants that simultaneously evolve rules using FA, SA, and TA features.
2. **Novel fitness function:** Rewards both high returns and high trading activity at low risk — balances profitability and activity.
3. **Novel GP operator:** Injects trees into GP population that perform many trades while maintaining profitability.
4. **Empirical result:** Combined FA+SA+TA GP outperforms all single-analysis and pairwise-combination variants.
5. **International scope:** 42 companies across multiple countries — broader than US-focused studies.

## Relevance to Thesis

- Provides direct empirical support for the thesis's "hierarchical information fusion" framework
- The same three analysis types (FA, SA, TA) are combined in the thesis using ML (gradient boosting) rather than GP
- GP and gradient boosting are both ensemble/optimization approaches — conceptual parallel

## Key Concepts

- [[Machine Learning in Asset Pricing]] — GP as an ML approach to signal fusion
- [[Reddit as Financial Signal]] — SA pillar in Christodoulaki parallels FinBERT sentiment in thesis
- [[Sentiment Velocity]] — sentiment signal in the context of a combined framework
