"""
Import FinBERT scores back into PostgreSQL
==========================================
After running the Colab notebook, download the scored CSVs and
run this script to update the ticker_mentions table.

Expected input file format (from Colab output):
    id, sentiment_label, sentiment_score, sentiment_positive,
    sentiment_negative, sentiment_neutral

Usage:
    python import_finbert_scores.py                    # imports all finbert_output/*.csv
    python import_finbert_scores.py --file chunk_01_scored.csv
    python import_finbert_scores.py --preview          # show sample without importing
"""

import os
import glob
import argparse
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

INPUT_DIR = "finbert_output"

def get_engine():
    conn = (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'trading_sentiment')}"
    )
    return create_engine(conn)


def import_file(engine, filepath, preview=False):
    print(f"\nLoading {filepath}...")
    df = pd.read_csv(filepath)
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Sample:\n{df.head(3)}\n")

    # Validate expected columns
    required = {"id", "sentiment_label", "sentiment_score",
                "sentiment_positive", "sentiment_negative", "sentiment_neutral"}
    missing = required - set(df.columns)
    if missing:
        print(f"  ERROR: Missing columns: {missing}")
        return 0

    if preview:
        print("  Preview mode — skipping import")
        return 0

    # Show sentiment distribution
    print("  Sentiment distribution:")
    print(df["sentiment_label"].value_counts().to_string())
    print()

    # Bulk update in batches
    analyzed_at = datetime.now()
    batch_size  = 10_000
    total_updated = 0

    with engine.connect() as conn:
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start:start + batch_size]
            for _, row in batch.iterrows():
                conn.execute(text("""
                    UPDATE ticker_mentions SET
                        sentiment_label       = :label,
                        sentiment_score       = :score,
                        sentiment_positive    = :positive,
                        sentiment_negative    = :negative,
                        sentiment_neutral     = :neutral,
                        sentiment_analyzed_at = :analyzed_at
                    WHERE id = :id
                """), {
                    "id":          int(row["id"]),
                    "label":       row["sentiment_label"],
                    "score":       float(row["sentiment_score"]),
                    "positive":    float(row["sentiment_positive"]),
                    "negative":    float(row["sentiment_negative"]),
                    "neutral":     float(row["sentiment_neutral"]),
                    "analyzed_at": analyzed_at,
                })
            conn.commit()
            total_updated += len(batch)
            print(f"  Updated {total_updated:,} / {len(df):,} rows...")

    print(f"  Done: {total_updated:,} rows updated")
    return total_updated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",    type=str, help="Import a specific file")
    parser.add_argument("--preview", action="store_true", help="Preview without importing")
    args = parser.parse_args()

    engine = get_engine()

    if args.file:
        files = [args.file]
    else:
        files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.csv")))
        if not files:
            print(f"No CSV files found in {INPUT_DIR}/")
            print("Download scored files from Colab and place them there.")
            return

    print(f"Files to import: {len(files)}")
    grand_total = 0
    for f in files:
        grand_total += import_file(engine, f, preview=args.preview)

    print(f"\n{'='*50}")
    print(f"Total rows updated: {grand_total:,}")

    # Final verification
    if not args.preview:
        with engine.connect() as conn:
            scored = conn.execute(text(
                "SELECT COUNT(*) FROM ticker_mentions WHERE sentiment_label IS NOT NULL"
            )).scalar()
            total = conn.execute(text(
                "SELECT COUNT(*) FROM ticker_mentions"
            )).scalar()
            print(f"Scored in DB: {scored:,} / {total:,} ({scored/total*100:.1f}%)")
            print("\nSentiment breakdown:")
            dist = pd.read_sql(text("""
                SELECT sentiment_label, COUNT(*) as count,
                       ROUND(AVG(sentiment_score)::numeric, 3) as avg_confidence
                FROM ticker_mentions
                WHERE sentiment_label IS NOT NULL
                GROUP BY sentiment_label ORDER BY count DESC
            """), conn)
            print(dist.to_string(index=False))


if __name__ == "__main__":
    main()