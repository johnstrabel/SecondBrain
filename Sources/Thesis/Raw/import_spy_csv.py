import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/trading_sentiment')

print("Reading SPY.csv...")
df = pd.read_csv('SPY.csv')
print(f"Columns: {list(df.columns)}")
print(df.head(3))
print(f"Total rows: {len(df)}")

# Normalize column names - handle any source format
df.columns = [c.strip() for c in df.columns]

# Find date column
date_col = next((c for c in df.columns if 'date' in c.lower()), df.columns[0])
# Find close column
close_col = next((c for c in df.columns if 'close' in c.lower()), df.columns[1])

print(f"\nUsing date column: '{date_col}', close column: '{close_col}'")

df['Date']  = pd.to_datetime(df[date_col])
df['Close'] = df[close_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)

df = df.sort_values('Date')
df = df[(df['Date'] >= '2010-01-01') & (df['Date'] <= '2024-01-01')]
df['daily_return'] = df['Close'].pct_change()

print(f"Rows after filtering 2010-2024: {len(df)}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")

# Delete existing SPY rows first
with engine.connect() as conn:
    deleted = conn.execute(text("DELETE FROM daily_prices WHERE ticker='SPY'")).rowcount
    conn.commit()
    print(f"Deleted {deleted} existing SPY rows")

inserted = 0
with engine.connect() as conn:
    for _, row in df.iterrows():
        try:
            conn.execute(text("""
                INSERT INTO daily_prices (ticker, date, open, high, low, close, volume, daily_return)
                VALUES (:t, :d, :o, :h, :l, :c, :v, :r)
                ON CONFLICT (ticker, date) DO NOTHING
            """), {
                't': 'SPY',
                'd': row['Date'].date(),
                'o': round(float(row['Close']), 4),  # use close for all since we only have close
                'h': round(float(row['Close']), 4),
                'l': round(float(row['Close']), 4),
                'c': round(float(row['Close']), 4),
                'v': 0,
                'r': round(float(row['daily_return']), 6) if not pd.isna(row['daily_return']) else None
            })
            inserted += 1
        except Exception as e:
            print(f"Insert error: {e}")
    conn.commit()

print(f"\nInserted {inserted} SPY rows")

with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM daily_prices WHERE ticker='SPY'")).scalar()
    earliest = conn.execute(text("SELECT MIN(date) FROM daily_prices WHERE ticker='SPY'")).scalar()
    latest = conn.execute(text("SELECT MAX(date) FROM daily_prices WHERE ticker='SPY'")).scalar()
    print(f"SPY rows in DB: {count}")
    print(f"Date range: {earliest} to {latest}")
    if count > 3000:
        print("\nSUCCESS - run debug_pipeline.py")
    else:
        print(f"\nWARNING - only {count} rows, need back to 2010")