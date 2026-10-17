# Testing the SQL on a real MySQL 8 server

The analysis SQL in sql/02_core_analysis.sql is written for MySQL 8. In the
authoring environment no MySQL server was available, so the same query LOGIC
was validated in SQLite instead (see sqlite_validation.py and
sqlite_validation_results.txt). That proves the logic and numbers; it does not
prove MySQL syntax execution. Run these steps to verify on real MySQL.

1. Install MySQL 8 (Windows: MySQL Installer; macOS: brew install mysql;
   Ubuntu: apt install mysql-server). Start the server.

2. Enable local file loading. In the server config (my.cnf / my.ini) set
   local_infile=1 under [mysqld], restart, then connect with:
   mysql --local-infile=1 -u root -p

3. Put the two raw CSVs in a folder the server can read, edit the two
   LOAD DATA LOCAL INFILE paths in sql/01_schema_and_load.sql to match,
   then run:
   mysql --local-infile=1 -u root -p < sql/01_schema_and_load.sql

4. Run the analysis script and compare against the reference numbers below:
   mysql --local-infile=1 -u root -p olist_marketing < sql/02_core_analysis.sql

Reference results (from the validated run, 17 Oct 2026):
- Q1: 8,000 MQLs, 842 deals, 10.525% exactly. Printed at 2 decimals this is
  10.53 in MySQL ROUND and 10.52 in Python (banker's rounding) - same division.
- Q2: organic_search 2,296/271/11.80%; paid_search 1,586/195/12.30%;
  unknown 1,099/179/16.29%; social 1,350/75/5.56%; direct_traffic 499/56/11.22%.
- Q4: min -1 day, avg 48.4 days, max 427 days. (MySQL DATEDIFF and the
  SQLite check both count whole days, so the averages match pandas exactly.)
- Q7 top rep: 133 deals.

5. If a number differs from the reference, do not edit the data to match;
   report the difference - that is a real finding about the dialect or load.

Known dialect notes:
- CTEs (WITH) and window functions (RANK, LAG, SUM() OVER, NTILE) require
  MySQL 8.0+. On MySQL 5.7 the script will not run.
- MySQL division is real division, so MoM growth percentages print correctly.
