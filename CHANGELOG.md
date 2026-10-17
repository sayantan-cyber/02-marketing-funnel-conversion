# Change log

## 17 Oct 2026 - fixes from external audit

1. **Conversion rounding unified.** Docs previously showed 10.52% while the
   SQLite log showed 10.53. Pipeline and SQLite validation now print the exact
   value 10.525%; narrative says 10.5%. MYSQL_TESTING.md explains both 2-decimal
   roundings.
2. **45.1% seller finding reworded.** Now stated as "seller_id appears in the
   available e-commerce sellers dataset", with an explicit note that absence
   does not prove a seller never sold. "Active seller" / "onboarding" framing
   removed from README, findings, recommendations and limitations.
3. **Exact input-acquisition steps added.** data/README.md now lists the exact
   download URLs used (Kaggle source + verified GitHub mirror links), the
   Project 1 sellers file needed for the link check, and the expected
   row x column shape of every file. Raw CSVs stay out of the zip/repo by
   license policy; validation fails loudly on wrong files.
4. **One portable authoritative pipeline.** analysis.py and charts.py (which
   contained hardcoded /tmp and /home paths) are deleted. Everything is
   produced by notebooks/funnel_analysis.py, which uses repo-relative paths
   only.
5. **Validation expanded from 5 to 16 checks.** Added: missing mql_id in both
   tables, duplicate deal IDs, join cardinality (merged row count == 8,000),
   seller_id presence, empty-origin count (60), negative close-time count (1),
   plus 4 expected-output checks on the exports. The new checks surfaced one
   real fact: 1 won deal has an empty business_segment (now encoded as a
   documented expectation). SQLite validation gained the same data-quality
   checks.
6. **Budget-shift recommendation reframed.** Now explicitly an association,
   not a causal claim - the dataset has no spend data.
7. **SQLite sales-cycle average aligned with MySQL DATEDIFF semantics**
   (whole-day casts): 48.4 days everywhere, matching pandas.

Already disclosed before the audit, unchanged: MySQL 8 syntax itself untested
(no server in the author's environment - see docs/review/MYSQL_TESTING.md);
late-2018 conversion window caveat in Limitations.

Still NOT uploaded to GitHub; awaiting owner review.
