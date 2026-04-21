import os, warnings
import pandas as pd
import pandas_datareader as pdr
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

engine = create_engine(DB_URL)

# Download AAPL
print("Downloading AAPL from Stooq...")
df = pdr.get_data_stooq('AAPL', start='2023-01-01', end='2023-03-01')
df = df.sort_index()
print(f"Rows: {len(df)}")
print(df.head(3))
print(f"Dtypes:\n{df.dtypes}")

# Build result
result = pd.DataFrame()
result['ticker']       = 'AAPL'
result['date']         = [d.date() for d in df.index]
result['open']         = df['Open'].round(4).values
result['high']         = df['High'].round(4).values
result['low']          = df['Low'].round(4).values
result['close']        = df['Close'].round(4).values
result['volume']       = df['Volume'].fillna(0).astype(int).values
result['daily_return'] = df['Close'].pct_change().round(6).values

# Replace NaN with None
result = result.where(pd.notnull(result), None)

print(f"\nResult dtypes:\n{result.dtypes}")
print(f"\nFirst row: {result.iloc[0].to_dict()}")
print(f"Date type: {type(result['date'].iloc[0])}")

# Try inserting first 3 rows with full error output
print("\nAttempting inserts...")
with engine.connect() as conn:
    for i, row in result.head(3).iterrows():
        r = row.to_dict()
        print(f"  Inserting: {r}")
        try:
            conn.execute(text("""
                INSERT INTO daily_prices
                    (ticker, date, open, high, low, close, volume, daily_return)
                VALUES
                    (:ticker, :date, :open, :high, :low, :close, :volume, :daily_return)
                ON CONFLICT (ticker, date) DO NOTHING
            """), r)
            print(f"  OK")
        except Exception as e:
            print(f"  ERROR: {e}")
    conn.commit()

# Check
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM daily_prices")).scalar()
print(f"\nRows in DB: {count}")