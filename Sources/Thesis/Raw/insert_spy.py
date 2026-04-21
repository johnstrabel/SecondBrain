import pandas_datareader as pdr
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')

print("Downloading SPY via Stooq...")
try:
    df = pdr.get_data_stooq('SPY', start='2010-01-01', end='2024-01-01').sort_index()
except Exception as e:
    print(f"Stooq failed: {e}")
    print("Still rate limited — wait 15-20 min and try again")
    exit()

df['daily_return'] = df['Close'].pct_change()
print(f"Downloaded {len(df)} rows")

inserted = 0
with engine.connect() as conn:
    for date, row in df.iterrows():
        try:
            conn.execute(text("""
                INSERT INTO daily_prices (ticker, date, open, high, low, close, volume, daily_return)
                VALUES (:t, :d, :o, :h, :l, :c, :v, :r)
                ON CONFLICT (ticker, date) DO NOTHING
            """), {
                't': 'SPY',
                'd': date.date(),
                'o': round(float(row.Open), 4),
                'h': round(float(row.High), 4),
                'l': round(float(row.Low), 4),
                'c': round(float(row.Close), 4),
                'v': int(row.Volume),
                'r': round(float(row.daily_return), 6) if not pd.isna(row.daily_return) else None
            })
            inserted += 1
        except Exception as e:
            print(f"Insert error: {e}")
    conn.commit()

print(f"Inserted {inserted} SPY rows")

with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM daily_prices WHERE ticker='SPY'")).scalar()
    print(f"SPY rows in DB: {count}")