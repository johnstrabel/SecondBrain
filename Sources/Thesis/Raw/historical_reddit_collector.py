"""
Arctic Shift Historical Reddit Collector
=========================================
Pulls historical Reddit posts from financial subreddits (2010-2023)
using the Arctic Shift API (no auth required).

Key fixes in this version:
  - socket.setdefaulttimeout(45) — catches mid-transfer hangs that bypass requests timeout
  - timeout=(10, 30) tuple — separate connect vs read timeouts
  - ThreadPoolExecutor wrapper — hard kills any request exceeding MAX_REQUEST_SECONDS
  - api_month_end always = first of NEXT month (fixes zero-window bug)

Usage:
    python historical_reddit_collector.py                     # full run 2010-2023
    python historical_reddit_collector.py --start 2019-01     # resume from month
    python historical_reddit_collector.py --subreddit stocks  # single subreddit
    python historical_reddit_collector.py --dry-run           # estimate volume only
    python historical_reddit_collector.py --no-comments       # posts only (recommended)

Requirements:
    pip install requests sqlalchemy psycopg2-binary python-dotenv tqdm python-dateutil
"""

import requests
import time
import json
import os
import socket
import argparse
import logging
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from tqdm import tqdm

from improved_ticker_extractor import ImprovedTickerExtractor
from database import get_session, TickerMention, SourceType

load_dotenv()

# ── CRITICAL: global socket timeout — catches mid-transfer hangs ───────────────
socket.setdefaulttimeout(45)

# ── logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler("historical_collection.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ── configuration ─────────────────────────────────────────────────────────────
ARCTIC_SHIFT_BASE   = "https://arctic-shift.photon-reddit.com/api"

SUBREDDITS = [
    "wallstreetbets",
    "stocks",
    "investing",
    "options",
    "StockMarket",
    "SecurityAnalysis",
    "dividends",
    "ValueInvesting",
    "Daytrading",
    "algotrading",
    "thetagang",
    "pennystocks",
    "Superstonk",
    "RobinHood",
    "investing_discussion",
]

DEFAULT_START       = datetime(2010, 1, 1, tzinfo=timezone.utc)
DEFAULT_END         = datetime(2023, 12, 31, tzinfo=timezone.utc)

BATCH_SIZE          = 100
REQUEST_DELAY       = 1.0   # seconds between requests
MAX_RETRIES         = 5
RETRY_BACKOFF       = 2.0
MAX_REQUEST_SECONDS = 60    # hard kill threshold

PROGRESS_FILE = "historical_collection_progress.json"


# ── progress tracking ─────────────────────────────────────────────────────────

def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {
        "completed_months":     [],
        "total_mentions_saved": 0,
        "errors":               [],
        "skipped":              [],
    }


def save_progress(progress: dict):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def month_key(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


def months_in_range(start: datetime, end: datetime):
    current = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    while current <= end:
        next_month = current + relativedelta(months=1)
        yield current, next_month   # always yield full month window
        current = next_month


# ── Arctic Shift API ──────────────────────────────────────────────────────────

def _do_request(url: str, params: dict):
    """
    Single HTTP GET. Returns list of data items on 200, or (None, status_code) otherwise.
    Uses timeout=(10, 30): 10s connect, 30s between received bytes.
    socket.setdefaulttimeout(45) catches anything that slips through.
    """
    resp = requests.get(url, params=params, timeout=(10, 30))
    if resp.status_code == 200:
        return resp.json().get("data", [])
    return (None, resp.status_code)


def fetch_batch(endpoint: str, params: dict, retries: int = MAX_RETRIES) -> list:
    """
    Fetch one page from Arctic Shift with hard timeout enforcement via ThreadPoolExecutor.
    Returns list of post/comment dicts, or [] on failure.
    """
    url = f"{ARCTIC_SHIFT_BASE}/{endpoint}"

    for attempt in range(retries):
        try:
            time.sleep(REQUEST_DELAY)

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_do_request, url, params)
                try:
                    result = future.result(timeout=MAX_REQUEST_SECONDS)
                except FuturesTimeoutError:
                    log.warning(f"Hard timeout ({MAX_REQUEST_SECONDS}s) — attempt {attempt+1}/{retries}")
                    time.sleep(RETRY_BACKOFF * (2 ** attempt))
                    continue

            # Non-200 returns a tuple
            if isinstance(result, tuple):
                _, status = result
                if status == 429:
                    wait = RETRY_BACKOFF * (2 ** attempt)
                    log.warning(f"Rate limited. Waiting {wait:.0f}s ...")
                    time.sleep(wait)
                elif status >= 500:
                    log.warning(f"Server error {status}. Retry {attempt+1}/{retries}")
                    time.sleep(RETRY_BACKOFF * (2 ** attempt))
                else:
                    log.error(f"Unexpected status {status}")
                    return []
                continue

            return result if result is not None else []

        except requests.exceptions.Timeout:
            log.warning(f"Requests timeout — attempt {attempt+1}/{retries}")
            time.sleep(RETRY_BACKOFF * (2 ** attempt))

        except requests.exceptions.ConnectionError as e:
            log.warning(f"Connection error: {e}. Retry {attempt+1}/{retries}")
            time.sleep(RETRY_BACKOFF * (2 ** attempt))

        except socket.timeout:
            log.warning(f"Socket timeout — attempt {attempt+1}/{retries}")
            time.sleep(RETRY_BACKOFF * (2 ** attempt))

        except Exception as e:
            log.warning(f"Unexpected error: {e}. Retry {attempt+1}/{retries}")
            time.sleep(RETRY_BACKOFF * (2 ** attempt))

    log.error(f"All {retries} retries exhausted for {endpoint}")
    return []


def fetch_posts_for_month(subreddit: str, month_start: datetime, month_end: datetime) -> list:
    """
    Pull all posts in [month_start, month_end) with pagination.
    month_end must be the first of the NEXT month — not the last day of the current month.
    """
    all_posts = []
    after_ts  = int(month_start.timestamp())
    before_ts = int(month_end.timestamp())

    while True:
        params = {
            "subreddit": subreddit,
            "after":     after_ts,
            "before":    before_ts,
            "limit":     BATCH_SIZE,
            "sort":      "asc",
        }

        batch = fetch_batch("posts/search", params)
        if not batch:
            break

        all_posts.extend(batch)

        if len(batch) < BATCH_SIZE:
            break

        last_ts = batch[-1].get("created_utc", 0)
        after_ts = int(float(last_ts)) + 1
        if after_ts >= before_ts:
            break

    return all_posts


def fetch_comments_for_post(post_id: str, subreddit: str) -> list:
    params = {
        "link_id":   post_id,
        "subreddit": subreddit,
        "limit":     50,
    }
    return fetch_batch("comments/search", params)


# ── mention extraction ────────────────────────────────────────────────────────

def build_mentions(post: dict, subreddit: str, extractor: ImprovedTickerExtractor,
                   include_comments: bool = True) -> list:
    mentions = []

    title        = post.get("title", "") or ""
    selftext     = post.get("selftext", "") or ""
    post_text    = f"{title} {selftext}"
    post_tickers = extractor.extract_tickers(post_text)

    created_utc = post.get("created_utc", 0)
    post_ts = datetime.fromtimestamp(float(created_utc), tz=timezone.utc)

    raw_url = post.get("url") or post.get("permalink") or ""
    if raw_url.startswith("/r/"):
        post_url = f"https://reddit.com{raw_url}"
    elif raw_url.startswith("http"):
        post_url = raw_url
    else:
        post_url = f"https://reddit.com/r/{subreddit}"

    for ticker in post_tickers:
        mentions.append({
            "ticker":       ticker,
            "timestamp":    post_ts,
            "source":       SourceType.POST,
            "subreddit":    subreddit,
            "score":        int(post.get("score", 0) or 0),
            "num_comments": int(post.get("num_comments", 0) or 0),
            "url":          post_url,
            "text_snippet": post_text[:200],
            "created_utc":  post_ts,
            "reddit_id":    post.get("id", ""),
            "author":       post.get("author", "[deleted]") or "[deleted]",
            "author_karma": 0,
        })

    if include_comments and post.get("id"):
        comments = fetch_comments_for_post(post["id"], subreddit)
        for comment in comments:
            body = comment.get("body", "") or ""
            if not body or body in ("[deleted]", "[removed]"):
                continue

            comment_tickers = extractor.extract_tickers(body)
            comment_ts = datetime.fromtimestamp(
                float(comment.get("created_utc", 0)), tz=timezone.utc
            )

            raw_cmt_url = comment.get("permalink") or ""
            cmt_url = (
                f"https://reddit.com{raw_cmt_url}"
                if raw_cmt_url.startswith("/r/")
                else post_url
            )

            for ticker in comment_tickers:
                mentions.append({
                    "ticker":       ticker,
                    "timestamp":    comment_ts,
                    "source":       SourceType.COMMENT,
                    "subreddit":    subreddit,
                    "score":        int(comment.get("score", 0) or 0),
                    "num_comments": None,
                    "url":          cmt_url,
                    "text_snippet": body[:200],
                    "created_utc":  comment_ts,
                    "reddit_id":    comment.get("id", ""),
                    "author":       comment.get("author", "[deleted]") or "[deleted]",
                    "author_karma": 0,
                })

    return mentions


# ── database persistence ──────────────────────────────────────────────────────

def save_mentions_batch(session, mentions: list) -> int:
    saved = 0
    for m in mentions:
        if not m["reddit_id"]:
            continue
        try:
            exists = session.query(TickerMention).filter_by(
                reddit_id=m["reddit_id"],
                ticker=m["ticker"]
            ).first()
            if exists:
                continue

            session.add(TickerMention(
                ticker        = m["ticker"],
                timestamp     = m["timestamp"],
                source        = m["source"],
                subreddit     = m["subreddit"],
                score         = m["score"],
                num_comments  = m["num_comments"],
                url           = m["url"],
                text_snippet  = m["text_snippet"],
                created_utc   = m["created_utc"],
                reddit_id     = m["reddit_id"],
                author        = m["author"],
                author_karma  = m["author_karma"],
            ))
            saved += 1

        except Exception as e:
            session.rollback()
            log.debug(f"Skip {m.get('reddit_id')}/{m.get('ticker')}: {e}")
            continue

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        log.error(f"Batch commit failed: {e}")
        saved = 0

    return saved


# ── main collection logic ─────────────────────────────────────────────────────

class HistoricalCollector:

    def __init__(self, start: datetime = DEFAULT_START, end: datetime = DEFAULT_END,
                 subreddits: list = SUBREDDITS, skip_comments: bool = False):
        self.start         = start
        self.end           = end
        self.subreddits    = subreddits
        self.skip_comments = skip_comments
        self.extractor     = ImprovedTickerExtractor()

        conn = (
            f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
            f"{os.getenv('DB_PASSWORD', 'postgres')}@"
            f"{os.getenv('DB_HOST', 'localhost')}:"
            f"{os.getenv('DB_PORT', '5432')}/"
            f"{os.getenv('DB_NAME', 'trading_sentiment')}"
        )
        self.session  = get_session(conn)
        self.progress = load_progress()

        log.info(f"Collector initialised - {len(subreddits)} subreddits, "
                 f"{start.strftime('%Y-%m')} to {end.strftime('%Y-%m')}")
        log.info(f"Already completed: {len(self.progress['completed_months'])} month-subreddit pairs")

    def run(self, dry_run: bool = False):
        all_months  = list(months_in_range(self.start, self.end))
        total_pairs = len(all_months) * len(self.subreddits)
        log.info(f"Total month-subreddit pairs: {total_pairs}")

        if dry_run:
            log.info("DRY RUN - no data will be written.")
            self._estimate_volume()
            return

        skipped  = self.progress.get("skipped", [])
        pair_bar = tqdm(total=total_pairs, desc="Overall progress", unit="pair")

        for month_start, month_end in all_months:
            for subreddit in self.subreddits:
                key = f"{month_key(month_start)}:{subreddit}"

                if key in self.progress["completed_months"]:
                    pair_bar.update(1)
                    continue

                if key in skipped:
                    log.info(f"Skipping previously failed pair: {key}")
                    pair_bar.update(1)
                    continue

                log.info(f"Processing: {key}")
                saved = self._process_month(subreddit, month_start, month_end)

                self.progress["completed_months"].append(key)
                self.progress["total_mentions_saved"] += saved
                save_progress(self.progress)

                pair_bar.update(1)
                log.info(f"  Saved {saved} mentions  "
                         f"(running total: {self.progress['total_mentions_saved']:,})")

        pair_bar.close()
        log.info("=" * 60)
        log.info("Historical collection complete!")
        log.info(f"Total mentions saved: {self.progress['total_mentions_saved']:,}")
        if self.progress.get("skipped"):
            log.info(f"Skipped pairs ({len(self.progress['skipped'])}): {self.progress['skipped']}")
        log.info("=" * 60)

    def _process_month(self, subreddit: str, month_start: datetime,
                       month_end: datetime) -> int:
        posts = fetch_posts_for_month(subreddit, month_start, month_end)
        if not posts:
            return 0

        total_saved = 0
        for post in posts:
            mentions = build_mentions(
                post, subreddit, self.extractor,
                include_comments=not self.skip_comments
            )
            if mentions:
                total_saved += save_mentions_batch(self.session, mentions)

        return total_saved

    def _estimate_volume(self):
        log.info("Sampling Jan 2021 from wallstreetbets ...")
        sample_start = datetime(2021, 1, 1, tzinfo=timezone.utc)
        sample_end   = datetime(2021, 2, 1, tzinfo=timezone.utc)
        posts = fetch_posts_for_month("wallstreetbets", sample_start, sample_end)
        log.info(f"  Posts found in sample month: {len(posts)}")

        ticker_count = 0
        for post in posts[:20]:
            title = post.get("title", "") or ""
            body  = post.get("selftext", "") or ""
            ticker_count += len(self.extractor.extract_tickers(f"{title} {body}"))

        avg_per_post    = ticker_count / max(20, 1)
        estimated_total = (
            avg_per_post * max(len(posts), 1)
            * len(self.subreddits)
            * (self.end.year - self.start.year + 1) * 12
        )
        log.info(f"  Avg tickers/post (sample): {avg_per_post:.1f}")
        log.info(f"  Estimated total mentions:  {estimated_total:,.0f}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Arctic Shift historical Reddit collector")
    parser.add_argument("--start",       default="2010-01",
                        help="Start month YYYY-MM (default: 2010-01)")
    parser.add_argument("--end",         default="2023-12",
                        help="End month YYYY-MM (default: 2023-12)")
    parser.add_argument("--subreddit",   default=None,
                        help="Single subreddit to collect (default: all 15)")
    parser.add_argument("--no-comments", action="store_true",
                        help="Skip comment fetching (recommended)")
    parser.add_argument("--dry-run",     action="store_true",
                        help="Estimate volume without writing to DB")
    return parser.parse_args()


def main():
    args  = parse_args()
    start = datetime.strptime(args.start + "-01", "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end   = datetime.strptime(args.end   + "-01", "%Y-%m-%d").replace(tzinfo=timezone.utc)
    subs  = [args.subreddit] if args.subreddit else SUBREDDITS

    collector = HistoricalCollector(
        start         = start,
        end           = end,
        subreddits    = subs,
        skip_comments = args.no_comments,
    )
    collector.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()