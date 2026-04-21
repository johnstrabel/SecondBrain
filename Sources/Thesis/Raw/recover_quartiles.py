"""
Recovery script — reruns ONLY the quartile assignment and DB insert.
Use this after the main pipeline crashes at the quartile step.
The event data is already in event_study_results from the partial run.

Run: python recover_quartiles.py
"""
import os, warnings, logging
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'trading_sentiment')}"
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

engine = create_engine(DB_URL)

log.info("Checking what's in event_study_results...")
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM event_study_results")).scalar()
log.info(f"Rows in table: {count:,}")

if count == 0:
    log.error("Table is empty — run build_event_study.py first")
    exit()

# The pipeline crashed before inserting — need to rerun from scratch
# but this time the table already has data from a previous partial run
# Check if data is actually there
with engine.connect() as conn:
    sample = conn.execute(text("""
        SELECT COUNT(*) FILTER (WHERE model_valid) as valid,
               COUNT(*) FILTER (WHERE surprise_day0 IS NOT NULL) as has_surprise,
               COUNT(*) FILTER (WHERE velocity_ratio IS NOT NULL) as has_velocity
        FROM event_study_results
    """)).fetchone()

log.info(f"Valid model: {sample.valid:,} | Has surprise: {sample.has_surprise:,} | Has velocity: {sample.has_velocity:,}")

if sample.has_surprise == 0:
    log.error("No data found — the pipeline crashed before inserting. Re-run build_event_study.py")
    exit()

log.info("Computing and updating quartiles...")

# Load current data
df = pd.read_sql(text("""
    SELECT id, surprise_day0, sue_value, velocity_ratio, net_sentiment
    FROM event_study_results
"""), engine)

log.info(f"Loaded {len(df):,} rows")

# Compute quartiles
for col, q_col in [
    ('surprise_day0',  'surprise_day0_quartile'),
    ('sue_value',      'sue_quartile'),
    ('velocity_ratio', 'velocity_quartile'),
    ('net_sentiment',  'sentiment_quartile'),
]:
    non_null = df[col].dropna()
    if len(non_null) < 4:
        log.info(f"Skipping {col} — insufficient data ({len(non_null)} non-null values)")
        df[q_col] = None
        continue

    df[q_col] = pd.qcut(
        df[col].rank(method='first', na_option='keep'),
        q=4, labels=[1, 2, 3, 4], duplicates='drop'
    ).astype('Int64')

    dist = df[q_col].value_counts().sort_index()
    log.info(f"{q_col}: {dict(dist)}")

# Update DB
log.info("Updating quartile columns in DB...")
with engine.connect() as conn:
    for _, row in df.iterrows():
        conn.execute(text("""
            UPDATE event_study_results SET
                surprise_day0_quartile = :s,
                sue_quartile           = :sue,
                velocity_quartile      = :v,
                sentiment_quartile     = :sent
            WHERE id = :id
        """), {
            's':    int(row['surprise_day0_quartile']) if pd.notna(row.get('surprise_day0_quartile')) else None,
            'sue':  int(row['sue_quartile']) if pd.notna(row.get('sue_quartile')) else None,
            'v':    int(row['velocity_quartile']) if pd.notna(row.get('velocity_quartile')) else None,
            'sent': int(row['sentiment_quartile']) if pd.notna(row.get('sentiment_quartile')) else None,
            'id':   int(row['id'])
        })
    conn.commit()

log.info("Done! Checking final summary...")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT
            COUNT(*) as total_events,
            COUNT(*) FILTER (WHERE model_valid) as valid_model,
            COUNT(*) FILTER (WHERE mention_count_pre > 0) as has_sentiment,
            COUNT(*) FILTER (WHERE sue_value IS NOT NULL) as has_sue,
            AVG(car_post_20) FILTER (WHERE model_valid) as avg_car_20,
            AVG(velocity_ratio) as avg_velocity,
            COUNT(*) FILTER (WHERE velocity_spike_3x) as spikes_3x,
            COUNT(*) FILTER (WHERE velocity_spike_5x) as spikes_5x
        FROM event_study_results
    """)).fetchone()

log.info("=" * 60)
log.info(f"Total events:         {result.total_events:,}")
log.info(f"Valid market model:   {result.valid_model:,}")
log.info(f"Has Reddit sentiment: {result.has_sentiment:,}")
log.info(f"Has SUE data:         {result.has_sue:,}")
log.info(f"Avg CAR(+1,+20):      {float(result.avg_car_20):.4f}" if result.avg_car_20 else "Avg CAR: N/A")
log.info(f"Avg velocity ratio:   {float(result.avg_velocity):.2f}" if result.avg_velocity else "Avg velocity: N/A")
log.info(f"3x velocity spikes:   {result.spikes_3x:,}")
log.info(f"5x velocity spikes:   {result.spikes_5x:,}")