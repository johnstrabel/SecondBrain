---
created: 2026-04-20
source_filename: "database.py"
file_type: python
tags: [thesis-code, database, schema, SQLAlchemy, PostgreSQL]
---

# database.py

## What This Script Does

Defines the SQLAlchemy ORM models (database schema) for the entire thesis data pipeline. Every other script imports `get_session()` and `TickerMention` from here. Running this file directly creates all tables in the `trading_sentiment` PostgreSQL database.

**Tables defined:**

| Table | Purpose |
|---|---|
| `ticker_mentions` | Core table — every Reddit mention of an S&P ticker (2.74M rows after full collection) |
| `ticker_baselines` | Pre-computed velocity baselines per ticker per time window |
| `velocity_events` | Detected velocity spikes (3×/5×/10× threshold crossings) |
| `sentiment_bias` | Daily/weekly sentiment bias per ticker |
| `scraper_runs` | Execution monitoring and debugging log |
| `manual_trades` | Stores manual trading decisions from dashboard (not used in final analysis) |

**Key `ticker_mentions` columns:**
- `ticker` — extracted stock symbol
- `created_utc`, `timestamp` — post/comment timestamp
- `source` — POST or COMMENT (enum)
- `subreddit` — one of 15 financial subreddits
- `text_snippet` — the mention text (for FinBERT scoring)
- `reddit_id` — unique Reddit ID (prevents duplicates)
- `spam_score` — anti-spam float score
- `sentiment_label`, `sentiment_score`, `sentiment_positive`, `sentiment_negative`, `sentiment_neutral` — added by FinBERT scoring pass; NULL until `import_finbert_scores.py` runs

**Composite indexes for performance:** `(ticker, timestamp)`, `(subreddit, timestamp)`, `(ticker, subreddit)`

**Connection string:** reads from `.env` — DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME (default: `trading_sentiment`)

**Run to create tables:** `python database.py`

---

## Code

```python
"""
Database schema for Reddit sentiment scraper
"""
from sqlalchemy import (create_engine, Column, Integer, String,
                        DateTime, Float, Text, Index, Enum)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum

Base = declarative_base()

class SourceType(enum.Enum):
    POST = "post"
    COMMENT = "comment"

class TickerMention(Base):
    __tablename__ = 'ticker_mentions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False, index=True)
    # ... sentiment_label, sentiment_score, sentiment_positive,
    #     sentiment_negative, sentiment_neutral (NULL until FinBERT run)

class TickerBaseline(Base):
    __tablename__ = 'ticker_baselines'
    # velocity baseline per ticker per time window

class VelocityEvent(Base):
    __tablename__ = 'velocity_events'
    # detected spike events: ticker, multiplier, threshold_crossed ('3x'/'5x'/'10x')

def create_database(connection_string):
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)

def get_session(connection_string):
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    return Session()
```

---

## Key Concepts

- [[Sentiment Velocity]] — `velocity_events` table stores detected spikes; `ticker_baselines` stores rolling baselines
- [[FinBERT]] — sentiment columns in `ticker_mentions` populated by `import_finbert_scores.py`
- [[Reddit as Financial Signal]] — `ticker_mentions` is the primary data store for 2.74M Reddit observations
