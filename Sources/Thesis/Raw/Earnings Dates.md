---
created: 2026-04-20
source_filename: "earnings_dates.csv"
file_type: csv
tags: [thesis-data, earnings-dates, EDGAR, PEAD, event-study]
---

# Earnings Dates — SEC EDGAR

**File:** `earnings_dates.csv`
**Description:** Earnings announcement dates for S&P 500 constituent companies collected from SEC EDGAR. This is the CSV backup of the `earnings_announcements` PostgreSQL table — the event anchor for the entire thesis event study.

**Total records:** 115,518 filings
**Tickers covered:** 507 unique tickers
**Date range:** January 2010 to December 2023

## Schema

| Column | Description |
|---|---|
| `id` | Auto-increment primary key |
| `ticker` | Stock ticker symbol |
| `cik` | SEC CIK number |
| `company_name` | Full company name from EDGAR |
| `announcement_date` | Filing date (t=0 in event study) |
| `fiscal_year` | Fiscal year of the filing |
| `fiscal_quarter` | Fiscal quarter (if applicable) |
| `filing_type` | 8-K, 10-Q, or 10-K |
| `form_url` | Direct EDGAR URL for the filing |
| `created_at` | When the record was collected |

## Filing Type Breakdown

| Type | Count | Notes |
|---|---|---|
| 8-K | 89,675 | Primary — Item 2.02 "Results of Operations"; most timely |
| 10-Q | 19,414 | Quarterly reports; used as fallback |
| 10-K | 6,429 | Annual reports; used as fallback |

## Data Sample

```
AA, Alcoa Corp, 2016-10-19, 8-K (CIK: 0001675149)
AA, Alcoa Corp, 2016-10-31, 8-K
```

## Key Concepts

- [[Post-Earnings Announcement Drift]] — this file defines t=0 for all 115,518 event study observations
- [[Efficient Market Hypothesis]] — filing date as public information event timestamp
