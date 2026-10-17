"""
Project 2: Olist Marketing Funnel - reproducible analysis pipeline.

Reads the 2 raw CSVs from ./data/ (links in README.md), validates them,
computes every funnel metric, saves charts into ./visuals/ and exports
into ./data-exports/.

Run:  python notebooks/funnel_analysis.py
Deps: pandas, numpy, matplotlib

Every number in README.md and docs/findings_and_recommendations.md comes
from this script, verified against the raw files on 17 Oct 2026.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA, VIS, EXP = ROOT / 'data', ROOT / 'visuals', ROOT / 'data-exports'
VIS.mkdir(exist_ok=True); EXP.mkdir(exist_ok=True)
INK, TEAL, GREY = '#251f21', '#73a89a', '#9a9496'
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})

# 1. Load
m = pd.read_csv(DATA / 'olist_marketing_qualified_leads_dataset.csv', parse_dates=['first_contact_date'])
d = pd.read_csv(DATA / 'olist_closed_deals_dataset.csv', parse_dates=['won_date'])

# 2. Merge, then validation checks (data quality + join integrity)
j = m.merge(d, on='mql_id', how='left', suffixes=('', '_deal'))
j['won'] = j['won_date'].notna()
j['days_to_close'] = (j['won_date'] - j['first_contact_date']).dt.days

checks = {
    'MQL rows == 8,000': len(m) == 8000,
    'closed-deal rows == 842': len(d) == 842,
    'mql_id unique in MQLs': bool(m['mql_id'].is_unique),
    'deal mql_id unique (1:1 join)': bool(d['mql_id'].is_unique),
    'no missing mql_id in MQLs': bool(m['mql_id'].notna().all()),
    'no missing mql_id in deals': bool(d['mql_id'].notna().all()),
    'every deal maps to an MQL': bool(d['mql_id'].isin(m['mql_id']).all()),
    'join keeps all 8,000 MQLs (cardinality 1:1)': len(j) == 8000,
    'first_contact_date present': bool(m['first_contact_date'].notna().all()),
    'seller_id present on every won deal': bool(d['seller_id'].notna().all()),
    'exactly 60 leads with empty origin (documented)': int(m['origin'].isna().sum()) == 60,
    'exactly 1 negative close time (documented quirk)': int((j['days_to_close'] < 0).sum()) == 1,
}
for name, ok in checks.items():
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
assert all(checks.values()), 'Validation failed. Inspect the raw files.'


# 3. Headline funnel metrics
print('\n-- Funnel --')
print('MQLs:', len(j), '| closed deals:', int(j['won'].sum()),
      '| conversion % (exact):', f"{j['won'].mean() * 100:.3f}")
print('MQL window:', m['first_contact_date'].min().date(), 'to', m['first_contact_date'].max().date())
print('Median days to close:', j['days_to_close'].median(),
      '| mean:', round(j['days_to_close'].mean(), 1), '| p90:', round(j['days_to_close'].quantile(.9)))

# 4. Conversion by origin
by_origin = j.groupby('origin').agg(mqls=('won', 'size'), won=('won', 'sum'))
by_origin['conv_pct'] = (by_origin['won'] / by_origin['mqls'] * 100).round(2)
by_origin = by_origin.sort_values('won', ascending=False)
by_origin.to_csv(EXP / 'conversion_by_origin.csv')
print('\nConversion by origin:')
print(by_origin)

# 5. Landing pages
lp = j.groupby('landing_page_id').agg(mqls=('won', 'size'), won=('won', 'sum'))
lp = lp[lp['mqls'] >= 30]
lp['conv_pct'] = (lp['won'] / lp['mqls'] * 100).round(2)
lp.sort_values('conv_pct', ascending=False).head(10).to_csv(EXP / 'top_landing_pages.csv')
print('\nLanding pages tracked:', j['landing_page_id'].nunique())

# 6. Won-deal profile
won = j[j['won']]
seg = won.groupby('business_segment').agg(deals=('won', 'size')).sort_values('deals', ascending=False)
seg.to_csv(EXP / 'won_by_segment.csv')
print('\nTop segments by closed deals:')
print(seg.head())
print('\nLead type mix of won deals:')
print(won['lead_type'].value_counts())

# 7. Declared revenue (unreliable, see limitations)
rev = won['declared_monthly_revenue']
print('\nDeclared monthly revenue: zero/blank in', round((rev == 0).mean() * 100, 1),
      '% of won deals; top 10 deals hold', round(rev.nlargest(10).sum() / rev.sum() * 100, 1), '% of the total')

# 8. Monthly funnel
mf = j.set_index('first_contact_date').resample('ME')['won'].agg(['size', 'sum'])
mf.columns = ['mqls', 'won']; mf['conv_pct'] = (mf['won'] / mf['mqls'] * 100).round(2)
mf.to_csv(EXP / 'monthly_funnel.csv')

# 8b. Expected-output checks
exp_checks = {
    'conversion_by_origin: 10 channels, won sums to 828 (14 deals have empty origin)':
        len(by_origin) == 10 and int(by_origin['won'].sum()) == 828,
    'monthly_funnel: totals reconcile to 8,000 MQLs / 842 deals':
        int(mf['mqls'].sum()) == 8000 and int(mf['won'].sum()) == 842,
    'top_landing_pages: 10 rows': len(pd.read_csv(EXP / 'top_landing_pages.csv')) == 10,
    'won_by_segment: deals sum to 841 (1 won deal has empty segment, documented)':
        int(seg['deals'].sum()) == 841,
}
print('\n-- Expected-output checks --')
for name, ok in exp_checks.items():
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
assert all(exp_checks.values()), 'Output check failed.'

# 9. Link to the e-commerce dataset (Project 1 sellers table, if present in data/)
sellers_path = DATA / 'olist_sellers_dataset.csv'
if sellers_path.exists():
    s = pd.read_csv(sellers_path)
    linked = d['seller_id'].isin(s['seller_id'])
    print('\nWon leads whose seller_id appears in the Project 1 e-commerce sellers table:',
          int(linked.sum()), 'of', len(d), f'({linked.mean() * 100:.1f}%)')

# 10. Charts
o = by_origin[by_origin['mqls'] >= 100].sort_values('conv_pct')
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(o.index, o['conv_pct'], color=[TEAL if x == o['conv_pct'].max() else GREY for x in o['conv_pct']])
for i, (v, n) in enumerate(zip(o['conv_pct'], o['mqls'])):
    ax.text(v + 0.2, i, f'{v:.1f}%  ({n:,} leads)', va='center', fontsize=9)
ax.set_title('MQL to closed-deal conversion by lead source (min 100 leads)', fontsize=13, weight='bold')
ax.set_xlabel('Conversion %'); ax.set_xlim(0, 22)
fig.tight_layout(); fig.savefig(VIS / '01_conversion_by_origin.png', dpi=150); plt.close(fig)

mm = mf.copy(); mm.index = pd.to_datetime(mm.index.to_timestamp() if hasattr(mm.index, 'to_timestamp') else mm.index)
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(mm.index, mm['mqls'], width=20, color=GREY, label='MQLs')
ax.bar(mm.index, mm['won'], width=20, color=TEAL, label='Closed deals')
ax.set_title('Marketing funnel volume by month', fontsize=13, weight='bold'); ax.legend()
fig.tight_layout(); fig.savefig(VIS / '02_monthly_funnel.png', dpi=150); plt.close(fig)

s10 = seg.head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.barh(s10.index, s10['deals'], color=[TEAL if i == len(s10) - 1 else GREY for i in range(len(s10))])
ax.set_title('Closed deals by business segment (top 10)', fontsize=13, weight='bold'); ax.set_xlabel('Deals')
fig.tight_layout(); fig.savefig(VIS / '03_won_by_segment.png', dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4.2))
ax.hist(j['days_to_close'].clip(0, 180).dropna(), bins=36, color=TEAL)
ax.axvline(j['days_to_close'].median(), color=INK, ls='--', lw=1.5)
ax.text(j['days_to_close'].median() + 3, ax.get_ylim()[1] * 0.85, f"median {j['days_to_close'].median():.0f} days")
ax.set_title('Days from first contact to closed deal (clipped at 180)', fontsize=13, weight='bold')
ax.set_xlabel('Days to close'); ax.set_ylabel('Deals')
fig.tight_layout(); fig.savefig(VIS / '04_days_to_close.png', dpi=150); plt.close(fig)

print('\nPipeline complete. Charts in visuals/, exports in data-exports/.')
