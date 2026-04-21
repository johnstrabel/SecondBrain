"""
ML Model — Information Fusion Framework
=========================================
Trains and evaluates multiple ML models to predict post-earnings return quartile.

Features (the "hierarchical framework"):
  - Sentiment layer:    net_sentiment, avg_sentiment_score, pct_positive, pct_negative
  - Velocity layer:     velocity_ratio, mention_count_7d, mention_count_90d_avg
  - Attention layer:    google_trends_pre (avg search interest pre-event)
                        wiki_pageviews_pre (avg pageviews pre-event)
  - Fundamental layer:  surprise_day0 (earnings surprise proxy), filing_type
  - Market layer:       beta, r_squared, price_at_event, avg_volume_30d

Target: Binary — top quartile CAR[+1,+20] vs bottom quartile (Q4 vs Q1)
        Also: 4-class quartile prediction

Train: 2010-2020
Test:  2021-2023

Models:
  1. Logistic Regression (baseline)
  2. Random Forest
  3. Gradient Boosting (XGBoost-style via sklearn)

Output: ml_results/ folder
Run: python ml_model.py
"""

import os, warnings, logging
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import timedelta

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, roc_auc_score,
                              confusion_matrix, RocCurveDisplay)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
import sklearn.metrics as skmetrics

warnings.filterwarnings("ignore")
load_dotenv()

OUTPUT_DIR = "ml_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DB_URL = (
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'trading_sentiment')}"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(f"{OUTPUT_DIR}/ml.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)
engine = create_engine(DB_URL)

# ─── Load Event Study Data ─────────────────────────────────────────────────────

log.info("Loading event study results...")
df = pd.read_sql(text("""
    SELECT e.*
    FROM event_study_results e
    WHERE e.model_valid = TRUE
      AND e.car_post_20 IS NOT NULL
      AND e.surprise_day0 IS NOT NULL
"""), engine)
df['event_date'] = pd.to_datetime(df['event_date'])
log.info(f"Base sample: {len(df):,} events")

# ─── Join Google Trends ────────────────────────────────────────────────────────

log.info("Joining Google Trends data...")
trends = pd.read_sql(text("""
    SELECT ticker, date, search_interest
    FROM google_trends
    ORDER BY ticker, date
"""), engine)
trends['date'] = pd.to_datetime(trends['date'])

def get_trends_pre(ticker, event_date, trends_df, window_days=30):
    """Get average Google Trends search interest in 30 days before event."""
    t = trends_df[trends_df['ticker'] == ticker]
    if t.empty:
        return np.nan
    pre = t[(t['date'] >= event_date - timedelta(days=window_days)) &
            (t['date'] < event_date)]
    return pre['search_interest'].mean() if len(pre) > 0 else np.nan

# Pre-group for speed
trends_by_ticker = {t: g for t, g in trends.groupby('ticker')}

def get_trends_fast(ticker, event_date, window_days=30):
    grp = trends_by_ticker.get(ticker)
    if grp is None:
        return np.nan
    pre = grp[(grp['date'] >= event_date - timedelta(days=window_days)) &
              (grp['date'] < event_date)]
    return pre['search_interest'].mean() if len(pre) > 0 else np.nan

# ─── Join Wikipedia ────────────────────────────────────────────────────────────

log.info("Joining Wikipedia pageviews data...")
wiki = pd.read_sql(text("""
    SELECT ticker, date, pageviews
    FROM wikipedia_pageviews
    ORDER BY ticker, date
"""), engine)
wiki['date'] = pd.to_datetime(wiki['date'])
wiki_by_ticker = {t: g for t, g in wiki.groupby('ticker')}

def get_wiki_fast(ticker, event_date, window_days=7):
    grp = wiki_by_ticker.get(ticker)
    if grp is None:
        return np.nan
    pre = grp[(grp['date'] >= event_date - timedelta(days=window_days)) &
              (grp['date'] < event_date)]
    return pre['pageviews'].mean() if len(pre) > 0 else np.nan

# ─── Build Feature Matrix ──────────────────────────────────────────────────────

log.info("Building feature matrix (this takes a few minutes)...")

df['google_trends_pre'] = df.apply(
    lambda r: get_trends_fast(r['ticker'], r['event_date']), axis=1)
df['wiki_pageviews_pre'] = df.apply(
    lambda r: get_wiki_fast(r['ticker'], r['event_date']), axis=1)

log.info(f"Google Trends coverage: {df['google_trends_pre'].notna().sum():,} / {len(df):,}")
log.info(f"Wikipedia coverage:     {df['wiki_pageviews_pre'].notna().sum():,} / {len(df):,}")

# Encode filing type
df['is_8k']  = (df['filing_type'] == '8-K').astype(int)
df['is_10q'] = (df['filing_type'] == '10-Q').astype(int)

# Log transform volume and pageviews
df['log_volume']    = np.log1p(df['avg_volume_30d'].fillna(0))
df['log_wiki']      = np.log1p(df['wiki_pageviews_pre'].fillna(0))
df['log_mentions']  = np.log1p(df['mention_count_7d'].fillna(0))
df['log_price']     = np.log1p(df['price_at_event'].fillna(0))

# ─── Define Features ──────────────────────────────────────────────────────────

FEATURE_COLS = [
    # Sentiment signals (pre-announcement only — no leakage)
    'net_sentiment',
    'avg_sentiment_score',
    'pct_positive',
    'pct_negative',
    # Velocity signals (pre-announcement)
    'velocity_ratio',
    'log_mentions',
    'mention_count_90d_avg',
    # Attention signals (pre-announcement)
    'google_trends_pre',
    'log_wiki',
    # Fundamental signals (filing type only — no price info from event day)
    'is_8k',
    'is_10q',
    # Market/stock characteristics (estimated from pre-event window)
    'beta',
    'r_squared',
    'log_price',
    'log_volume',
]

log.info(f"Features: {FEATURE_COLS}")

# ─── Define Target ────────────────────────────────────────────────────────────

# Compute CAR[+1,+20] quartiles as target (NOT surprise_day0 quartile — that causes leakage)
df['car_post_20_q'] = pd.qcut(
    df['car_post_20'].rank(method='first'),
    q=4, labels=[1,2,3,4], duplicates='drop'
).astype('Int64')

# Binary: Q4 (top) vs Q1 (bottom) CAR[+1,+20]
df_binary = df[df['car_post_20_q'].isin([1, 4])].copy()
df_binary['target_binary'] = (df_binary['car_post_20_q'] == 4).astype(int)

# 4-class: all quartiles
df['target_4class'] = df['car_post_20_q'].astype(int)

log.info(f"Binary sample (Q1 vs Q4): {len(df_binary):,}")
log.info(f"4-class sample: {len(df):,}")

# ─── Train/Test Split ─────────────────────────────────────────────────────────

TRAIN_END = '2020-12-31'
TEST_START = '2021-01-01'

train_b = df_binary[df_binary['event_date'] <= TRAIN_END]
test_b  = df_binary[df_binary['event_date'] >= TEST_START]

train_4 = df[df['event_date'] <= TRAIN_END]
test_4  = df[df['event_date'] >= TEST_START]

log.info(f"Binary  — Train: {len(train_b):,} | Test: {len(test_b):,}")
log.info(f"4-class — Train: {len(train_4):,} | Test: {len(test_4):,}")

def get_Xy(data, target_col, features):
    d = data[features + [target_col]].copy()
    X = d[features].values
    y = d[target_col].values
    return X, y

X_train_b, y_train_b = get_Xy(train_b, 'target_binary', FEATURE_COLS)
X_test_b,  y_test_b  = get_Xy(test_b,  'target_binary', FEATURE_COLS)
X_train_4, y_train_4 = get_Xy(train_4, 'target_4class', FEATURE_COLS)
X_test_4,  y_test_4  = get_Xy(test_4,  'target_4class', FEATURE_COLS)

# ─── Models ───────────────────────────────────────────────────────────────────

def make_pipeline(model):
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler',  StandardScaler()),
        ('model',   model),
    ])

models = {
    'Logistic Regression': make_pipeline(
        LogisticRegression(max_iter=1000, random_state=42, C=0.1)
    ),
    'Random Forest': make_pipeline(
        RandomForestClassifier(n_estimators=200, max_depth=6,
                               min_samples_leaf=50, random_state=42, n_jobs=-1)
    ),
    'Gradient Boosting': make_pipeline(
        GradientBoostingClassifier(n_estimators=200, max_depth=4,
                                   learning_rate=0.05, min_samples_leaf=50,
                                   random_state=42)
    ),
}

# ─── Train & Evaluate ─────────────────────────────────────────────────────────

results = []

log.info("\n" + "="*60)
log.info("BINARY CLASSIFICATION: Q1 vs Q4 CAR[+1,+20]")
log.info("="*60)

fig_roc, ax_roc = plt.subplots(figsize=(8, 6))

for name, pipe in models.items():
    log.info(f"\nTraining {name}...")
    pipe.fit(X_train_b, y_train_b)

    y_pred  = pipe.predict(X_test_b)
    y_proba = pipe.predict_proba(X_test_b)[:, 1]

    acc  = skmetrics.accuracy_score(y_test_b, y_pred)
    auc  = roc_auc_score(y_test_b, y_proba)
    prec = skmetrics.precision_score(y_test_b, y_pred, zero_division=0)
    rec  = skmetrics.recall_score(y_test_b, y_pred, zero_division=0)
    f1   = skmetrics.f1_score(y_test_b, y_pred, zero_division=0)

    # Cross-val on training set
    cv_auc = cross_val_score(pipe, X_train_b, y_train_b, cv=5,
                              scoring='roc_auc', n_jobs=-1).mean()

    log.info(f"  Accuracy:  {acc:.4f}")
    log.info(f"  AUC-ROC:   {auc:.4f}  (CV train AUC: {cv_auc:.4f})")
    log.info(f"  Precision: {prec:.4f}")
    log.info(f"  Recall:    {rec:.4f}")
    log.info(f"  F1:        {f1:.4f}")
    log.info(f"\n{classification_report(y_test_b, y_pred)}")

    results.append({
        'Model': name, 'Task': 'Binary',
        'Accuracy': round(acc, 4), 'AUC_ROC': round(auc, 4),
        'CV_AUC': round(cv_auc, 4),
        'Precision': round(prec, 4), 'Recall': round(rec, 4), 'F1': round(f1, 4),
        'N_train': len(y_train_b), 'N_test': len(y_test_b)
    })

    # ROC curve
    RocCurveDisplay.from_predictions(
        y_test_b, y_proba, name=f"{name} (AUC={auc:.3f})", ax=ax_roc)

ax_roc.plot([0,1],[0,1],'k--', label='Random (AUC=0.500)')
ax_roc.set_title('ROC Curves — Binary Classification (Q1 vs Q4 CAR[+1,+20])')
ax_roc.legend(loc='lower right')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/roc_curves_binary.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("ROC curve saved")

# ─── 4-Class ──────────────────────────────────────────────────────────────────

log.info("\n" + "="*60)
log.info("4-CLASS: PREDICTING CAR QUARTILE")
log.info("="*60)

for name, _ in models.items():
    pipe4 = make_pipeline(
        models[name].named_steps['model'].__class__(
            **{k: v for k, v in models[name].named_steps['model'].get_params().items()
               if k != 'n_jobs'}
        )
    )
    log.info(f"\nTraining {name} (4-class)...")
    pipe4.fit(X_train_4, y_train_4)
    y_pred4 = pipe4.predict(X_test_4)
    acc4 = skmetrics.accuracy_score(y_test_4, y_pred4)
    log.info(f"  Accuracy: {acc4:.4f}")
    log.info(f"\n{classification_report(y_test_4, y_pred4)}")
    results.append({
        'Model': name, 'Task': '4-Class',
        'Accuracy': round(acc4, 4), 'AUC_ROC': None,
        'CV_AUC': None, 'Precision': None, 'Recall': None, 'F1': None,
        'N_train': len(y_train_4), 'N_test': len(y_test_4)
    })

# ─── Feature Importance ───────────────────────────────────────────────────────

log.info("\nComputing feature importance...")

# Use Random Forest from binary task
rf_pipe = models['Random Forest']
rf_model = rf_pipe.named_steps['model']
importances = rf_model.feature_importances_

feat_imp = pd.DataFrame({
    'feature': FEATURE_COLS,
    'importance': importances
}).sort_values('importance', ascending=False)

log.info(f"\nTop 10 features:\n{feat_imp.head(10).to_string(index=False)}")
feat_imp.to_csv(f"{OUTPUT_DIR}/feature_importance.csv", index=False)

# Feature importance chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = []
feature_groups = {
    'net_sentiment': 'Sentiment', 'avg_sentiment_score': 'Sentiment',
    'pct_positive': 'Sentiment', 'pct_negative': 'Sentiment',
    'velocity_ratio': 'Velocity', 'log_mentions': 'Velocity',
    'mention_count_90d_avg': 'Velocity',
    'google_trends_pre': 'Attention', 'log_wiki': 'Attention',
    'surprise_day0': 'Fundamental', 'is_8k': 'Fundamental', 'is_10q': 'Fundamental',
    'beta': 'Market', 'r_squared': 'Market', 'log_price': 'Market', 'log_volume': 'Market',
}
group_colors = {
    'Sentiment': '#4e79a7', 'Velocity': '#f28e2b',
    'Attention': '#59a14f', 'Fundamental': '#e15759', 'Market': '#76b7b2'
}
bar_colors = [group_colors.get(feature_groups.get(f, 'Market'), '#aaaaaa')
              for f in feat_imp['feature']]

ax.barh(feat_imp['feature'], feat_imp['importance'], color=bar_colors)
ax.set_xlabel('Feature Importance (Gini)')
ax.set_title('Random Forest Feature Importance\nColored by Signal Layer', fontsize=12)
ax.invert_yaxis()

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=v, label=k) for k, v in group_colors.items()]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/feature_importance.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Feature importance chart saved")

# ─── Confusion Matrix for Best Model ──────────────────────────────────────────

best_model_name = max(
    [r for r in results if r['Task'] == 'Binary'],
    key=lambda x: x['AUC_ROC']
)['Model']

log.info(f"\nBest model: {best_model_name}")
best_pipe = models[best_model_name]
cm = confusion_matrix(y_test_b, best_pipe.predict(X_test_b))

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cm, cmap='Blues')
ax.set_xticks([0,1]); ax.set_yticks([0,1])
ax.set_xticklabels(['Pred Q1', 'Pred Q4'])
ax.set_yticklabels(['True Q1', 'True Q4'])
for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i,j]), ha='center', va='center', fontsize=14)
ax.set_title(f'Confusion Matrix — {best_model_name}')
plt.colorbar(im)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/confusion_matrix.png", dpi=150, bbox_inches='tight')
plt.close()

# ─── Predicted Probability vs Actual Returns ──────────────────────────────────

log.info("Generating predicted probability decile chart...")
test_b_copy = test_b.copy()
test_b_copy['pred_proba'] = best_pipe.predict_proba(X_test_b)[:, 1]
test_b_copy['proba_decile'] = pd.qcut(test_b_copy['pred_proba'], 10,
                                       labels=range(1, 11), duplicates='drop')
decile_returns = test_b_copy.groupby('proba_decile')['car_post_20'].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(decile_returns.index, decile_returns.values,
       color=['#e15759' if v < 0 else '#4e79a7' for v in decile_returns.values])
ax.axhline(0, color='black', linewidth=0.8)
ax.set_xlabel('Predicted Probability Decile (1=lowest, 10=highest)')
ax.set_ylabel('Mean CAR[+1,+20]')
ax.set_title(f'Mean CAR by Model Prediction Decile\n({best_model_name})', fontsize=12)
import matplotlib.ticker as mticker
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/prediction_decile_returns.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Decile chart saved")

# ─── Save Results ─────────────────────────────────────────────────────────────

results_df = pd.DataFrame(results)
results_df.to_csv(f"{OUTPUT_DIR}/model_comparison.csv", index=False)

log.info("\n" + "="*60)
log.info("ML MODEL COMPLETE")
log.info("="*60)
log.info(f"\nModel comparison:\n{results_df[results_df['Task']=='Binary'][['Model','Accuracy','AUC_ROC','CV_AUC','F1']].to_string(index=False)}")
log.info(f"\nOutput files in: {OUTPUT_DIR}/")
log.info("  model_comparison.csv")
log.info("  feature_importance.csv")
log.info("  feature_importance.png")
log.info("  roc_curves_binary.png")
log.info("  confusion_matrix.png")
log.info("  prediction_decile_returns.png")