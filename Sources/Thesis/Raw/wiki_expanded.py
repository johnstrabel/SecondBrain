"""
Wikipedia collector — expanded to full event study universe.
Looks up company names from SEC EDGAR data in DB to build Wikipedia titles.
Falls back to ticker-based search if no mapping found.

Run: python wiki_expanded.py
"""

import os, time, json, logging, requests
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'trading_sentiment')}"
)

WIKI_BASE       = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
WIKI_USER_AGENT = "ThesisResearch/1.0 (strj39@vse.cz)"
PROGRESS_FILE   = "wiki_expanded_progress.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("wiki_expanded.log"), logging.StreamHandler()])
log = logging.getLogger(__name__)

engine = create_engine(DB_URL)

# ── Get tickers + company names from DB ────────────────────────────────────────
log.info("Loading tickers from event_study_results...")
with engine.connect() as conn:
    tickers = [r[0] for r in conn.execute(text(
        "SELECT DISTINCT ticker FROM event_study_results ORDER BY ticker"
    )).fetchall()]

# Get company names from earnings_announcements table
log.info("Loading company names from earnings_announcements...")
with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT DISTINCT ticker, company_name
        FROM earnings_announcements
        WHERE company_name IS NOT NULL
        ORDER BY ticker
    """)).fetchall()
company_names = {r[0]: r[1] for r in rows}
log.info(f"Got company names for {len(company_names)} tickers")

# ── Progress tracking ──────────────────────────────────────────────────────────
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return set(json.load(f).get("completed", []))
    return set()

def save_progress(completed):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({"completed": list(completed)}, f)

# ── Fetch Wikipedia pageviews ──────────────────────────────────────────────────
session = requests.Session()
session.headers.update({"User-Agent": WIKI_USER_AGENT})

def fetch_wiki(article_title, year):
    encoded = requests.utils.quote(article_title.replace(" ", "_"), safe="")
    url = f"{WIKI_BASE}/en.wikipedia/all-access/all-agents/{encoded}/daily/{year}0101/{year}1231"
    try:
        time.sleep(0.3)
        resp = session.get(url, timeout=15)
        if resp.status_code == 200:
            items = resp.json().get("items", [])
            if items:
                df = pd.DataFrame(items)
                df['date'] = pd.to_datetime(df['timestamp'], format="%Y%m%d%H").dt.date
                df['pageviews'] = df['views'].astype(int)
                return df[['date', 'pageviews']]
        return pd.DataFrame()
    except Exception as e:
        log.debug(f"Wiki fetch error: {e}")
        return pd.DataFrame()

def try_article_titles(ticker):
    """Generate candidate Wikipedia titles to try for a ticker."""
    candidates = []
    
    # From company name in DB
    name = company_names.get(ticker, "")
    if name:
        candidates.append(name)
        # Clean version: remove Inc, Corp, etc.
        clean = name.replace(", Inc.", "").replace(" Inc.", "").replace(" Corp.", "")
        clean = clean.replace(", LLC", "").replace(" Ltd.", "").strip()
        if clean != name:
            candidates.append(clean)

    # Common fallbacks
    candidates.append(f"{ticker}")  # just the ticker symbol

    return candidates

def save_to_db(ticker, article_title, df):
    if df.empty:
        return 0
    saved = 0
    with engine.connect() as conn:
        for _, row in df.iterrows():
            try:
                conn.execute(text("""
                    INSERT INTO wikipedia_pageviews (ticker, date, pageviews, article_title)
                    VALUES (:ticker, :date, :pageviews, :article_title)
                    ON CONFLICT (ticker, date) DO NOTHING
                """), {
                    'ticker': ticker, 'date': row['date'],
                    'pageviews': int(row['pageviews']), 'article_title': article_title
                })
                saved += 1
            except Exception:
                pass
        conn.commit()
    return saved

# ── Main ───────────────────────────────────────────────────────────────────────
completed = load_progress()

# Also mark tickers already in wikipedia_pageviews table
with engine.connect() as conn:
    existing = {r[0] for r in conn.execute(text(
        "SELECT DISTINCT ticker FROM wikipedia_pageviews"
    )).fetchall()}
completed |= existing
log.info(f"Already have Wikipedia data for {len(completed)} tickers")

remaining = [t for t in tickers if t not in completed]
log.info(f"Remaining: {len(remaining)} tickers")

total_saved = 0
for ticker in tqdm(remaining, desc="Wikipedia"):
    candidates = try_article_titles(ticker)
    ticker_saved = 0
    found_title = None

    for title in candidates:
        # Try fetching 2023 as a test year
        test_df = fetch_wiki(title, 2023)
        if not test_df.empty:
            found_title = title
            break

    if found_title:
        # Fetch all years 2015-2023
        for year in range(2015, 2024):
            df = fetch_wiki(found_title, year)
            ticker_saved += save_to_db(ticker, found_title, df)
        log.debug(f"{ticker} ({found_title}): {ticker_saved} rows")
    else:
        log.debug(f"{ticker}: no Wikipedia article found")

    total_saved += ticker_saved
    completed.add(ticker)

    if len(completed) % 20 == 0:
        save_progress(completed)

save_progress(completed)

log.info(f"Done. Total rows saved: {total_saved:,}")
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*), COUNT(DISTINCT ticker) FROM wikipedia_pageviews")).fetchone()
    log.info(f"Wikipedia table: {count[0]:,} rows, {count[1]} tickers")