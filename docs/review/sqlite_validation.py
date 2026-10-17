"""
Validates the ANALYSIS LOGIC of sql/02_core_analysis.sql (written for MySQL 8)
by running dialect-adapted equivalents in SQLite against the same raw CSVs,
and compares them with the pandas results. MySQL itself was NOT executed in
the author's environment; see MYSQL_TESTING.md to run the real thing.
Differences vs MySQL syntax: strftime() for DATE_FORMAT, julianday() for
DATEDIFF, and 1.0* to force real division (SQLite divides integers).
"""
import sqlite3, pandas as pd
con = sqlite3.connect(':memory:')
pd.read_csv('data/olist_marketing_qualified_leads_dataset.csv').to_sql('mql', con, index=False)
pd.read_csv('data/olist_closed_deals_dataset.csv').to_sql('deals', con, index=False)

print('-- Q1 overall funnel --')
print(con.execute("""SELECT COUNT(*), SUM(cd.mql_id IS NOT NULL),
ROUND(100.0*SUM(cd.mql_id IS NOT NULL)/COUNT(*),3)
FROM mql m LEFT JOIN deals cd ON cd.mql_id=m.mql_id""").fetchall())

print('-- Q2 conversion by origin (top 5) --')
for r in con.execute("""WITH base AS (SELECT m.origin,(cd.mql_id IS NOT NULL) AS won
FROM mql m LEFT JOIN deals cd ON cd.mql_id=m.mql_id)
SELECT origin,COUNT(*),SUM(won),ROUND(100.0*SUM(won)/COUNT(*),2),
ROUND(100.0*SUM(won)/SUM(SUM(won)) OVER (),1), RANK() OVER (ORDER BY SUM(won) DESC)
FROM base GROUP BY origin ORDER BY 3 DESC LIMIT 5"""):
    print(r)

print('-- Q4 sales cycle (min, avg, max days) --')
print(con.execute("""SELECT MIN(CAST(julianday(cd.won_date)-julianday(m.first_contact_date) AS INT)),
ROUND(AVG(CAST(julianday(cd.won_date)-julianday(m.first_contact_date) AS INT)),1),
MAX(CAST(julianday(cd.won_date)-julianday(m.first_contact_date) AS INT))
FROM deals cd JOIN mql m ON m.mql_id=cd.mql_id""").fetchall())

print('-- Q7 sales rep productivity (top 3) --')
for r in con.execute("""SELECT sr_id,COUNT(*),RANK() OVER (ORDER BY COUNT(*) DESC)
FROM deals GROUP BY sr_id ORDER BY 2 DESC LIMIT 3"""):
    print(r)

print('-- data-quality checks (added after external audit) --')
print('missing mql_id in mql:', con.execute("SELECT SUM(mql_id IS NULL) FROM mql").fetchone()[0])
print('missing mql_id in deals:', con.execute("SELECT SUM(mql_id IS NULL) FROM deals").fetchone()[0])
print('duplicate deal mql_ids:', con.execute("SELECT COUNT(*)-COUNT(DISTINCT mql_id) FROM deals").fetchone()[0])
print('empty origin in mql:', con.execute("SELECT SUM(origin IS NULL) FROM mql").fetchone()[0])
print('left-join cardinality (expect 8000):', con.execute("SELECT COUNT(*) FROM mql m LEFT JOIN deals cd ON cd.mql_id=m.mql_id").fetchone()[0])
print('negative close times (documented quirk, expect 1):', con.execute("""SELECT COUNT(*) FROM deals cd JOIN mql m ON m.mql_id=cd.mql_id
WHERE julianday(cd.won_date)-julianday(m.first_contact_date) < 0""").fetchone()[0])
