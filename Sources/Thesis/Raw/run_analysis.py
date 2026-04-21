"""
Hypothesis Testing Analysis
============================
Tests all four hypotheses from the thesis:

H1: Reddit sentiment scores positively predict short-term returns
H2: Velocity spikes precede abnormal price movements (24-48hr)
H3: Sentiment predictive power varies by stock characteristics
H4: Pre-earnings sentiment velocity amplifies PEAD

Output: analysis_results/ folder with tables and charts
Run: python run_analysis.py
"""

import os, warnings, logging
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

OUTPUT_DIR = "analysis_results"
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
        logging.FileHandler(f"{OUTPUT_DIR}/analysis.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

engine = create_engine(DB_URL)

# ─── Load Data ─────────────────────────────────────────────────────────────────

log.info("Loading event study results...")
df = pd.read_sql(text("""
    SELECT *
    FROM event_study_results
    WHERE model_valid = TRUE
"""), engine)

df['event_date'] = pd.to_datetime(df['event_date'])
df['year'] = df['event_date'].dt.year
df['post_2019'] = df['year'] >= 2019

log.info(f"Loaded {len(df):,} events with valid market model")
log.info(f"Events with sentiment: {df['mention_count_pre'].notna().sum():,}")
log.info(f"Date range: {df['event_date'].min().date()} to {df['event_date'].max().date()}")

# Subset with sentiment data
df_sent = df[df['mention_count_pre'].notna() & (df['mention_count_pre'] > 0)].copy()
log.info(f"Events with pre-announcement mentions: {len(df_sent):,}")

# ─── Helper Functions ──────────────────────────────────────────────────────────

def ttest(group1, group2, label1, label2):
    """Two-sample t-test with summary."""
    g1 = group1.dropna()
    g2 = group2.dropna()
    t, p = stats.ttest_ind(g1, g2)
    return {
        'group1': label1, 'n1': len(g1), 'mean1': g1.mean(),
        'group2': label2, 'n2': len(g2), 'mean2': g2.mean(),
        't_stat': t, 'p_value': p,
        'significant': p < 0.05
    }

def winsorize(series, pct=0.01):
    """Winsorize at 1st and 99th percentile."""
    low  = series.quantile(pct)
    high = series.quantile(1 - pct)
    return series.clip(low, high)

def stars(p):
    if p < 0.01: return '***'
    if p < 0.05: return '**'
    if p < 0.10: return '*'
    return ''

def ols(y, X, add_const=True):
    """Simple OLS using scipy — returns coef, se, t, p per column."""
    y = np.array(y, dtype=float)
    X = np.array(X, dtype=float)
    if add_const:
        X = np.column_stack([np.ones(len(X)), X])
    mask = ~(np.isnan(y) | np.isnan(X).any(axis=1))
    y, X = y[mask], X[mask]
    if len(y) < 10:
        return None
    XtX_inv = np.linalg.pinv(X.T @ X)
    coef = XtX_inv @ X.T @ y
    resid = y - X @ coef
    s2 = (resid @ resid) / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * XtX_inv))
    t = coef / se
    p = 2 * stats.t.sf(np.abs(t), df=len(y) - X.shape[1])
    return {'coef': coef, 'se': se, 't': t, 'p': p, 'n': len(y)}

# ─── Descriptive Statistics ────────────────────────────────────────────────────

log.info("\n" + "="*60)
log.info("DESCRIPTIVE STATISTICS")
log.info("="*60)

desc_cols = ['ar_day0', 'car_pre_5', 'car_post_5', 'car_post_10', 'car_post_20',
             'velocity_ratio', 'net_sentiment', 'avg_sentiment_score',
             'mention_count_pre', 'beta', 'price_at_event']
desc = df[desc_cols].describe(percentiles=[.1, .25, .5, .75, .9]).round(4)
log.info(f"\n{desc.to_string()}")
desc.to_csv(f"{OUTPUT_DIR}/descriptive_stats.csv")

# Sentiment subset
desc_sent = df_sent[desc_cols].describe(percentiles=[.1, .25, .5, .75, .9]).round(4)
desc_sent.to_csv(f"{OUTPUT_DIR}/descriptive_stats_sentiment_subset.csv")

# ─── H1: Sentiment → Returns ───────────────────────────────────────────────────

log.info("\n" + "="*60)
log.info("H1: SENTIMENT SCORES PREDICT SHORT-TERM RETURNS")
log.info("="*60)

h1_results = []
for car_col, label in [('car_post_5', 'CAR[+1,+5]'), ('car_post_20', 'CAR[+1,+20]')]:
    for sent_col, sent_label in [('net_sentiment', 'Net Sentiment'), ('avg_sentiment_score', 'Avg Score')]:
        d = df_sent[[car_col, sent_col, 'beta', 'price_at_event']].dropna()
        y = winsorize(d[car_col])
        X = np.column_stack([
            winsorize(d[sent_col]),
            d['beta'],
            np.log(d['price_at_event'].clip(0.01))
        ])
        result = ols(y, X)
        if result:
            coef1 = result['coef'][1]
            se1   = result['se'][1]
            t1    = result['t'][1]
            p1    = result['p'][1]
            log.info(f"{label} ~ {sent_label}: coef={coef1:.4f} se={se1:.4f} t={t1:.2f} p={p1:.4f} {stars(p1)} n={result['n']}")
            h1_results.append({
                'Dependent': label, 'Sentiment': sent_label,
                'Coef': round(coef1, 4), 'SE': round(se1, 4),
                't': round(t1, 2), 'p': round(p1, 4),
                'Sig': stars(p1), 'N': result['n']
            })

pd.DataFrame(h1_results).to_csv(f"{OUTPUT_DIR}/H1_sentiment_returns.csv", index=False)
log.info(f"H1 results saved")

# ─── H2: Velocity Spikes → Abnormal Returns ────────────────────────────────────

log.info("\n" + "="*60)
log.info("H2: VELOCITY SPIKES PRECEDE ABNORMAL RETURNS")
log.info("="*60)

# Define spike groups
df['spike_group'] = 'No Spike'
df.loc[df['velocity_ratio'] >= 3,  'spike_group'] = '3x Spike'
df.loc[df['velocity_ratio'] >= 5,  'spike_group'] = '5x Spike'
df.loc[df['velocity_ratio'] >= 10, 'spike_group'] = '10x Spike'

h2_results = []
no_spike = df[df['spike_group'] == 'No Spike']
for spike_label in ['3x Spike', '5x Spike', '10x Spike']:
    spike_grp = df[df['spike_group'] == spike_label]
    for car_col, car_label in [('ar_day0', 'AR[0]'), ('car_post_5', 'CAR[+1,+5]'), ('car_post_20', 'CAR[+1,+20]')]:
        result = ttest(spike_grp[car_col], no_spike[car_col], spike_label, 'No Spike')
        result['metric'] = car_label
        h2_results.append(result)
        log.info(f"{spike_label} vs No Spike | {car_label}: "
                 f"mean={result['mean1']:.4f} vs {result['mean2']:.4f} "
                 f"t={result['t_stat']:.2f} p={result['p_value']:.4f} {stars(result['p_value'])}")

h2_df = pd.DataFrame(h2_results)
h2_df.to_csv(f"{OUTPUT_DIR}/H2_velocity_spikes.csv", index=False)

# Spike group summary
spike_summary = df.groupby('spike_group')[['ar_day0', 'car_post_5', 'car_post_20']].agg(['mean', 'count']).round(4)
spike_summary.to_csv(f"{OUTPUT_DIR}/H2_spike_group_summary.csv")
log.info(f"\nSpike group summary:\n{spike_summary.to_string()}")

# ─── H3: Sentiment × Stock Characteristics ────────────────────────────────────

log.info("\n" + "="*60)
log.info("H3: SENTIMENT POWER VARIES BY STOCK CHARACTERISTICS")
log.info("="*60)

df_sent['log_price']    = np.log(df_sent['price_at_event'].clip(0.01))
df_sent['log_volume']   = np.log(df_sent['avg_volume_30d'].clip(1))
df_sent['size_proxy']   = df_sent['log_price'] + df_sent['log_volume']
df_sent['high_beta']    = (df_sent['beta'] > df_sent['beta'].median()).astype(int)
df_sent['large_cap']    = (df_sent['size_proxy'] > df_sent['size_proxy'].median()).astype(int)
df_sent['high_velocity'] = (df_sent['velocity_ratio'] > df_sent['velocity_ratio'].median()).astype(int)

h3_results = []
for group_col, group_label in [('large_cap', 'Size'), ('high_beta', 'Beta')]:
    for car_col, car_label in [('car_post_5', 'CAR[+1,+5]'), ('car_post_20', 'CAR[+1,+20]')]:
        grp0 = df_sent[df_sent[group_col] == 0]
        grp1 = df_sent[df_sent[group_col] == 1]
        label0 = f"Small {'Cap' if group_col == 'large_cap' else 'Beta'}"
        label1 = f"Large {'Cap' if group_col == 'large_cap' else 'Beta'}"

        # OLS within each group
        for grp, glabel in [(grp0, label0), (grp1, label1)]:
            d = grp[[car_col, 'net_sentiment', 'beta']].dropna()
            y = winsorize(d[car_col])
            X = np.column_stack([winsorize(d['net_sentiment']), d['beta']])
            result = ols(y, X)
            if result:
                log.info(f"{car_label} ~ Net Sentiment | {glabel}: "
                         f"coef={result['coef'][1]:.4f} t={result['t'][1]:.2f} "
                         f"p={result['p'][1]:.4f} {stars(result['p'][1])} n={result['n']}")
                h3_results.append({
                    'Metric': car_label, 'Group_Type': group_label,
                    'Group': glabel, 'Sentiment_Coef': round(result['coef'][1], 4),
                    't': round(result['t'][1], 2), 'p': round(result['p'][1], 4),
                    'Sig': stars(result['p'][1]), 'N': result['n']
                })

pd.DataFrame(h3_results).to_csv(f"{OUTPUT_DIR}/H3_heterogeneity.csv", index=False)

# ─── H4: 4×4 Grid — Surprise × Velocity ──────────────────────────────────────

log.info("\n" + "="*60)
log.info("H4: PRE-EARNINGS SENTIMENT VELOCITY AMPLIFIES PEAD")
log.info("="*60)

# Use only events with both surprise and velocity quartiles
df_h4 = df[df['surprise_day0_quartile'].notna() & df['velocity_quartile'].notna()].copy()
df_h4['surprise_q'] = df_h4['surprise_day0_quartile'].astype(int)
df_h4['velocity_q'] = df_h4['velocity_quartile'].astype(int)

log.info(f"H4 sample: {len(df_h4):,} events")

for car_col, car_label in [('car_post_5', 'CAR[+1,+5]'), ('car_post_10', 'CAR[+1,+10]'), ('car_post_20', 'CAR[+1,+20]')]:
    grid = df_h4.groupby(['surprise_q', 'velocity_q'])[car_col].agg(['mean', 'count']).round(4)
    grid.to_csv(f"{OUTPUT_DIR}/H4_grid_{car_col}.csv")

    # Pivot for readable table
    pivot_mean  = df_h4.groupby(['surprise_q', 'velocity_q'])[car_col].mean().unstack()
    pivot_count = df_h4.groupby(['surprise_q', 'velocity_q'])[car_col].count().unstack()
    pivot_mean.index  = [f'Surprise Q{i}' for i in pivot_mean.index]
    pivot_mean.columns = [f'Velocity Q{i}' for i in pivot_mean.columns]
    log.info(f"\n{car_label} — Mean CAR by Surprise × Velocity Quartile:\n{pivot_mean.round(4).to_string()}")
    pivot_mean.to_csv(f"{OUTPUT_DIR}/H4_pivot_{car_col}.csv")

# H4 t-test: High surprise + High velocity vs High surprise + Low velocity
high_surp_high_vel = df_h4[(df_h4['surprise_q'] == 4) & (df_h4['velocity_q'] == 4)]['car_post_20']
high_surp_low_vel  = df_h4[(df_h4['surprise_q'] == 4) & (df_h4['velocity_q'] == 1)]['car_post_20']
low_surp_high_vel  = df_h4[(df_h4['surprise_q'] == 1) & (df_h4['velocity_q'] == 4)]['car_post_20']
low_surp_low_vel   = df_h4[(df_h4['surprise_q'] == 1) & (df_h4['velocity_q'] == 1)]['car_post_20']

log.info(f"\nH4 Key Comparisons (CAR[+1,+20]):")
for g1, g2, label in [
    (high_surp_high_vel, high_surp_low_vel, 'High Surprise: High Vel vs Low Vel'),
    (low_surp_high_vel,  low_surp_low_vel,  'Low Surprise: High Vel vs Low Vel'),
]:
    r = ttest(g1, g2, 'High Velocity', 'Low Velocity')
    log.info(f"  {label}: {r['mean1']:.4f} vs {r['mean2']:.4f} "
             f"t={r['t_stat']:.2f} p={r['p_value']:.4f} {stars(r['p_value'])} "
             f"n={r['n1']}/{r['n2']}")

# ─── Charts ────────────────────────────────────────────────────────────────────

log.info("\nGenerating charts...")

# Chart 1: CAR event study plot (average across all events)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, subset, title in [
    (axes[0], df, 'All Events'),
    (axes[1], df_sent, 'Events with Reddit Sentiment'),
]:
    windows = ['car_pre_5', 'ar_day0', 'car_post_5', 'car_post_10', 'car_post_20']
    labels  = ['Pre[-5,-1]', 'Day 0', 'Post[+1,+5]', 'Post[+1,+10]', 'Post[+1,+20]']
    means   = [subset[w].mean() for w in windows]
    ax.bar(labels, means, color=['steelblue' if m >= 0 else 'firebrick' for m in means])
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title(title, fontsize=12)
    ax.set_ylabel('Mean Abnormal Return')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2))
    ax.tick_params(axis='x', rotation=15)

plt.suptitle('Average Abnormal Returns Around Earnings Announcements', fontsize=13)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart1_car_overview.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Chart 1 saved")

# Chart 2: CAR by velocity spike group
fig, ax = plt.subplots(figsize=(10, 5))
spike_groups = ['No Spike', '3x Spike', '5x Spike', '10x Spike']
colors = ['#aaaaaa', '#4e79a7', '#f28e2b', '#e15759']
x = np.arange(3)
width = 0.2
metrics = ['ar_day0', 'car_post_5', 'car_post_20']
metric_labels = ['AR[0]', 'CAR[+1,+5]', 'CAR[+1,+20]']

for i, (grp, col) in enumerate(zip(spike_groups, colors)):
    vals = [df[df['spike_group'] == grp][m].mean() for m in metrics]
    ax.bar(x + i*width, vals, width, label=grp, color=col)

ax.set_xticks(x + width*1.5)
ax.set_xticklabels(metric_labels)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel('Mean Abnormal Return')
ax.set_title('Abnormal Returns by Velocity Spike Group', fontsize=12)
ax.legend()
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart2_velocity_spikes.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Chart 2 saved")

# Chart 3: H4 heatmap — 4×4 grid
fig, axes = plt.subplots(1, 3, figsize=(16, 4))
for ax, car_col, car_label in zip(
    axes,
    ['car_post_5', 'car_post_10', 'car_post_20'],
    ['CAR[+1,+5]', 'CAR[+1,+10]', 'CAR[+1,+20]']
):
    pivot = df_h4.groupby(['surprise_q', 'velocity_q'])[car_col].mean().unstack()
    im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto')
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xticklabels([f'Vel Q{i+1}' for i in range(4)])
    ax.set_yticklabels([f'Surp Q{i+1}' for i in range(4)])
    ax.set_title(f'{car_label}', fontsize=11)
    ax.set_xlabel('Velocity Quartile')
    ax.set_ylabel('Surprise Quartile')
    for i in range(4):
        for j in range(4):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f'{val:.3f}', ha='center', va='center', fontsize=8)
    plt.colorbar(im, ax=ax)

plt.suptitle('Mean CAR by Earnings Surprise × Sentiment Velocity Quartile (H4)', fontsize=12)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart3_H4_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Chart 3 saved")

# Chart 4: Sentiment distribution over time
fig, ax = plt.subplots(figsize=(12, 4))
yearly = df_sent.groupby('year')['net_sentiment'].mean()
ax.bar(yearly.index, yearly.values,
       color=['#e15759' if v < 0 else '#4e79a7' for v in yearly.values])
ax.axhline(0, color='black', linewidth=0.8)
ax.set_xlabel('Year')
ax.set_ylabel('Mean Net Sentiment')
ax.set_title('Average Pre-Announcement Net Sentiment by Year', fontsize=12)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart4_sentiment_over_time.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Chart 4 saved")

# Chart 5: Velocity ratio distribution
fig, ax = plt.subplots(figsize=(10, 4))
vel_data = df['velocity_ratio'].dropna()
vel_data = vel_data[vel_data <= vel_data.quantile(0.95)]  # trim extreme outliers for viz
ax.hist(vel_data, bins=50, color='steelblue', edgecolor='white', linewidth=0.5)
ax.axvline(3,  color='orange', linestyle='--', label='3x spike')
ax.axvline(5,  color='red',    linestyle='--', label='5x spike')
ax.axvline(10, color='darkred',linestyle='--', label='10x spike')
ax.set_xlabel('Velocity Ratio (7-day / 90-day baseline)')
ax.set_ylabel('Number of Events')
ax.set_title('Distribution of Pre-Announcement Mention Velocity', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart5_velocity_distribution.png", dpi=150, bbox_inches='tight')
plt.close()
log.info("Chart 5 saved")

# ─── Summary Report ────────────────────────────────────────────────────────────

log.info("\n" + "="*60)
log.info("ANALYSIS COMPLETE")
log.info("="*60)
log.info(f"Output files in: {OUTPUT_DIR}/")
log.info("  descriptive_stats.csv")
log.info("  H1_sentiment_returns.csv")
log.info("  H2_velocity_spikes.csv")
log.info("  H2_spike_group_summary.csv")
log.info("  H3_heterogeneity.csv")
log.info("  H4_grid_*.csv")
log.info("  H4_pivot_*.csv")
log.info("  chart1_car_overview.png")
log.info("  chart2_velocity_spikes.png")
log.info("  chart3_H4_heatmap.png")
log.info("  chart4_sentiment_over_time.png")
log.info("  chart5_velocity_distribution.png")