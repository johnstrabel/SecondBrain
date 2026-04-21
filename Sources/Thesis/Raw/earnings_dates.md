---
created: 2026-04-20
source_filename: "earnings_dates.csv"
file_type: csv
tags: [thesis-data, EDGAR, earnings-dates, SEC, event-study, 10-Q, 10-K]
---

# earnings_dates.csv — SEC EDGAR Earnings Announcement Dates

## What This File Contains

115,518 earnings announcement dates for S&P 500 constituents, collected from SEC EDGAR. Each row is a filing event with: CIK, company name, filing type (10-Q or 10-K), and filing date.

## Data Summary

- **N records:** 115,518 earnings events
- **Coverage:** 281 S&P 500 historical constituents (2010–2023)
- **Source:** SEC EDGAR Electronic Data Gathering, Analysis, and Retrieval system
- **Fields:** CIK, company name, filing type, filing date (= announcement date for event study)

## Key Concepts

- [[Post-Earnings Announcement Drift]] — these dates define t=0 for every event in the event study
- [[Sentiment Velocity]] — velocity is measured relative to these dates as the anchor

*See also: [[Earnings Dates]] for the Session 1 note on this dataset.*
