import pandas_datareader as pdr
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')

# Check table structure
print("Table columns:")
with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='daily_prices' ORDER BY ordinal_position")).fetchall()
    for r in result:
        print(" ", r)

# Check current SPY count
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM daily_prices WHERE ticker='SPY'")).scalar()
    print(f"\nSPY rows currently in DB: {count}")

# Download one row
print("\nDownloading SPY test row from Stooq...")
df = pdr.get_data_stooq('SPY', start='2023-01-01', end='2023-01-10').sort_index()
print(f"Downloaded {len(df)} rows")
print(df.head(2))

row = df.iloc[0]
print(f"\nTrying to insert: date={row.name.date()} close={row.Close}")

try:
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO daily_prices (ticker, date, open, high, low, close, volume, daily_return)
            VALUES (:t, :d, :o, :h, :l, :c, :v, :r)
            ON CONFLICT (ticker, date) DO NOTHING
        """), {
            't': 'SPY',
            'd': row.name.date(),
            'o': round(float(row.Open), 4),
            'h': round(float(row.High), 4),
            'l': round(float(row.Low), 4),
            'c': round(float(row.Close), 4),
            'v': int(row.Volume),
            'r': 0.001
        })
        conn.commit()
        count = conn.execute(text("SELECT COUNT(*) FROM daily_prices WHERE ticker='SPY'")).scalar()
        print(f"SPY rows after insert: {count}")
except Exception as e:
    print(f"INSERT ERROR: {e}")