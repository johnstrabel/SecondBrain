---
created: 2026-04-20
source_filename: "debug_edgar.py"
file_type: python
tags: [thesis-code, utility, debug, EDGAR]
---

# debug_edgar.py

## What This Script Does

One-off debug script to test the EDGAR API connection and inspect the filing structure for a known ticker (MSFT). Verifies that the CIK lookup, pagination of submissions, and form-type filtering work correctly. Not part of the main pipeline — used during development to diagnose API response format issues.

---

## Code

```python
import requests, json, os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
load_dotenv()

headers = {"User-Agent": "thesis-research john@example.com"}

# Load MSFT CIK from sec_company_tickers.json
data = json.load(open("sec_company_tickers.json"))
msft = next(v for v in data.values() if v["ticker"] == "MSFT")
cik = str(msft["cik_str"]).zfill(10)

# Fetch archive page 1 from EDGAR
url = f"https://data.sec.gov/submissions/CIK{cik}-submissions-001.json"
r = requests.get(url, headers=headers)
d = r.json()
forms = d.get("form", [])
```
