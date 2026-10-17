-- Project 2 core analysis (MySQL 8)
USE olist_marketing;

-- Q1. Overall funnel: MQLs to closed deals
SELECT COUNT(*) AS mqls,
       SUM(cd.mql_id IS NOT NULL) AS closed_deals,
       ROUND(100 * SUM(cd.mql_id IS NOT NULL) / COUNT(*), 2) AS conversion_pct
FROM marketing_qualified_leads m
LEFT JOIN closed_deals cd ON cd.mql_id = m.mql_id;

-- Q2. Conversion by lead source, ranked, with share of won deals
WITH base AS (
    SELECT m.origin, (cd.mql_id IS NOT NULL) AS won
    FROM marketing_qualified_leads m
    LEFT JOIN closed_deals cd ON cd.mql_id = m.mql_id
)
SELECT origin,
       COUNT(*) AS mqls,
       SUM(won) AS deals,
       ROUND(100 * SUM(won) / COUNT(*), 2) AS conversion_pct,
       ROUND(100 * SUM(won) / SUM(SUM(won)) OVER (), 1) AS share_of_deals_pct,
       RANK() OVER (ORDER BY SUM(won) DESC) AS deals_rank
FROM base
GROUP BY origin
ORDER BY deals DESC;

-- Q3. Landing pages with the best conversion (minimum 30 leads)
SELECT m.landing_page_id,
       COUNT(*) AS mqls,
       SUM(cd.mql_id IS NOT NULL) AS deals,
       ROUND(100 * SUM(cd.mql_id IS NOT NULL) / COUNT(*), 2) AS conversion_pct
FROM marketing_qualified_leads m
LEFT JOIN closed_deals cd ON cd.mql_id = m.mql_id
GROUP BY 1
HAVING COUNT(*) >= 30
ORDER BY conversion_pct DESC
LIMIT 10;

-- Q4. Sales cycle length: days from first contact to won
SELECT MIN(DATEDIFF(cd.won_date, m.first_contact_date)) AS fastest_days,
       ROUND(AVG(DATEDIFF(cd.won_date, m.first_contact_date)), 1) AS avg_days,
       MAX(DATEDIFF(cd.won_date, m.first_contact_date)) AS slowest_days
FROM closed_deals cd
JOIN marketing_qualified_leads m ON m.mql_id = cd.mql_id;

-- Q5. Won-deal mix: segment and lead type
SELECT business_segment, lead_type, business_type, COUNT(*) AS deals,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS share_pct
FROM closed_deals
GROUP BY 1, 2, 3
ORDER BY deals DESC;

-- Q6. Monthly funnel with conversion trend (CTE + window)
WITH monthly AS (
    SELECT DATE_FORMAT(m.first_contact_date, '%Y-%m') AS month,
           COUNT(*) AS mqls,
           SUM(cd.mql_id IS NOT NULL) AS deals
    FROM marketing_qualified_leads m
    LEFT JOIN closed_deals cd ON cd.mql_id = m.mql_id
    GROUP BY 1
)
SELECT month, mqls, deals,
       ROUND(100 * deals / mqls, 2) AS conversion_pct,
       ROUND(100 * (mqls / LAG(mqls) OVER (ORDER BY month) - 1), 1) AS mql_mom_growth_pct
FROM monthly
ORDER BY month;

-- Q7. Sales rep productivity (anonymized IDs)
SELECT sr_id, COUNT(*) AS deals_won,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_by_deals
FROM closed_deals
GROUP BY sr_id
ORDER BY deals_won DESC;
