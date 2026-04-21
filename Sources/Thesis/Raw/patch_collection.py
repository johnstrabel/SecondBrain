"""
Patch Collection Script
=======================
Forces re-collection of specific month-subreddit pairs by removing them
from the progress file and re-running just those pairs.

Usage:
    python patch_collection.py --pairs "2020-08:wallstreetbets" "2020-08:stocks"
    python patch_collection.py --list       # show all completed pairs in progress file
    python patch_collection.py --failed     # re-run all pairs logged as errors

Safe to run while main scraper is NOT running. Do not run both simultaneously.
"""

import argparse
import logging
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from historical_reddit_collector import (
    HistoricalCollector,
    load_progress,
    save_progress,
    fetch_posts_for_month,
    build_mentions,
    save_mentions_batch,
    SUBREDDITS,
    PROGRESS_FILE,
)
from improved_ticker_extractor import ImprovedTickerExtractor

# ── logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler("patch_collection.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Patch specific month-subreddit pairs")
    parser.add_argument("--pairs", nargs="+", default=None,
                        help='Pairs to re-run e.g. "2020-08:wallstreetbets" "2020-08:stocks"')
    parser.add_argument("--list",        action="store_true",
                        help="List progress file contents and exit")
    parser.add_argument("--failed",      action="store_true",
                        help="Re-run all pairs recorded as errors")
    parser.add_argument("--no-comments", action="store_true",
                        help="Skip comments (match main run configuration)")
    return parser.parse_args()


def list_progress():
    progress  = load_progress()
    completed = progress.get("completed_months", [])
    errors    = progress.get("errors", [])
    print(f"\nProgress file: {PROGRESS_FILE}")
    print(f"Completed pairs:      {len(completed)}")
    print(f"Total mentions saved: {progress.get('total_mentions_saved', 0):,}")
    if errors:
        print(f"\nLogged errors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
    else:
        print("No errors logged.")
    print()


def remove_pairs_from_progress(pairs: list):
    progress = load_progress()
    before   = len(progress["completed_months"])
    progress["completed_months"] = [
        p for p in progress["completed_months"] if p not in pairs
    ]
    after = len(progress["completed_months"])
    save_progress(progress)
    log.info(f"Removed {before - after} pair(s) from progress file")


def run_patch(pairs: list, skip_comments: bool):
    """Re-collect specific month-subreddit pairs."""

    # Validate
    valid_pairs = []
    for pair in pairs:
        parts = pair.split(":")
        if len(parts) != 2:
            log.error(f"Invalid format '{pair}' — expected 'YYYY-MM:subreddit'")
            continue
        month_str, subreddit = parts
        try:
            datetime.strptime(month_str + "-01", "%Y-%m-%d")
        except ValueError:
            log.error(f"Invalid month '{month_str}' in '{pair}'")
            continue
        if subreddit not in SUBREDDITS:
            log.warning(f"'{subreddit}' not in standard subreddit list — continuing anyway")
        valid_pairs.append((month_str, subreddit))

    if not valid_pairs:
        log.error("No valid pairs to process.")
        return

    # Remove from progress file so they won't be skipped
    pair_keys = [f"{m}:{s}" for m, s in valid_pairs]
    remove_pairs_from_progress(pair_keys)

    # Set up shared resources
    import os
    from sqlalchemy import create_engine
    from dotenv import load_dotenv
    load_dotenv()

    conn = (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'trading_sentiment')}"
    )
    from database import get_session
    session   = get_session(conn)
    extractor = ImprovedTickerExtractor()
    progress  = load_progress()

    # Process each pair individually with correct month window
    for month_str, subreddit in valid_pairs:
        key = f"{month_str}:{subreddit}"
        log.info(f"Processing: {key}")

        # CRITICAL FIX: month_start = first of month, month_end = first of NEXT month
        month_start = datetime.strptime(month_str + "-01", "%Y-%m-%d").replace(tzinfo=timezone.utc)
        month_end   = month_start + relativedelta(months=1)

        log.info(f"  Window: {month_start.date()} to {month_end.date()}")

        posts = fetch_posts_for_month(subreddit, month_start, month_end)
        log.info(f"  Fetched {len(posts)} posts from API")

        total_saved = 0
        for post in posts:
            mentions = build_mentions(
                post, subreddit, extractor,
                include_comments=not skip_comments
            )
            if mentions:
                total_saved += save_mentions_batch(session, mentions)

        log.info(f"  Saved {total_saved} new mentions")

        # Mark as completed
        if key not in progress["completed_months"]:
            progress["completed_months"].append(key)
        progress["total_mentions_saved"] += total_saved
        save_progress(progress)

    log.info("Patch complete.")
    log.info(f"Total mentions in DB: {progress['total_mentions_saved']:,}")


def main():
    args = parse_args()

    if args.list:
        list_progress()
        return

    if args.failed:
        progress = load_progress()
        errors   = progress.get("errors", [])
        if not errors:
            log.info("No errors recorded in progress file.")
            return
        run_patch(errors, skip_comments=args.no_comments)
        return

    if args.pairs:
        run_patch(args.pairs, skip_comments=args.no_comments)
        return

    print("No action specified. Use --pairs, --list, or --failed.")
    print('Example: python patch_collection.py --pairs "2020-08:wallstreetbets" "2020-08:stocks"')


if __name__ == "__main__":
    main()