# Findings and business recommendations

Analysis of 8,000 real marketing-qualified leads and 842 closed deals at Olist
(Jun 2017 - Nov 2018). Every number comes from `notebooks/funnel_analysis.py`.

## What the data says

1. **Overall conversion is 10.5%.** 842 of 8,000 MQLs signed (10.525%
   exactly; Python prints 10.52 and SQL ROUND prints 10.53 - same division). Volume peaked at
   1,352 MQLs in Apr 2018; conversion held near 13-14% in the best months.

2. **Channel quality varies 4x.** Paid search converts at 12.3% and organic
   search at 11.8%, while social converts at 5.6% and email at 3.0%. Leads with
   an unknown origin convert best of all (16.3%), which usually means direct or
   untracked high-intent traffic.

3. **Landing pages matter more than channels.** Across 495 landing pages, the
   best high-volume pages convert near 20% - roughly double the funnel average.

4. **The sales cycle is fast for most, long for a few.** Median 14 days to
   close, mean 48.4, p90 about 162 days, slowest 427.

5. **The won-seller profile is clear.** Resellers (70% of wins), "online_medium"
   lead type (39%), and home_decor / health_beauty / car_accessories segments
   dominate.

6. **45.1% of won leads appear in the available e-commerce sellers dataset.**
   380 of 842 won leads have a seller_id present in the Project 1 sellers
   table. That table covers orders through Oct 2018, so absence does not
   prove a seller never transacted - the honest reading is "at least 45.1%
   of signed sellers visibly transacted in the available data".

7. **Declared revenue is not usable.** 94.7% of won deals declare R$0 monthly
   revenue, and 97.4% of the declared total sits in the top 10 deals (one claims
   R$50M/month). Treat that column as missing data, not signal.

## Recommendations

1. **Search outperforms email and social - an association, not proof.** The
   dataset has no spend data, so no causal budget claim is possible. As a
   hypothesis to test with real spend figures: at current volumes, leads
   arriving via paid search close at roughly 4x email's rate (12.3% vs 3.0%).

2. **Clone the winning landing pages.** The top pages convert at ~20%. Their
   copy and audience targeting should become the template for the other 490+.

3. **Work the long tail of the pipeline actively.** Deals past 60 days rarely
   close fast afterwards; a re-engagement cadence for aged MQLs is cheaper than
   new acquisition.

4. **Fix revenue declaration at the source.** Make the field required and
   validated on the signup form; today it cannot support any sizing analysis.

5. **Follow signed sellers past signing.** Only ~45% of wins appear in the
   available e-commerce sellers data. Whether the rest churned, onboarded
   late, or never started cannot be told from this dataset alone - that gap
   is worth its own measurement.

## Limitations

- 842 closed deals is a modest base; segment-level conversion rates carry wide
  confidence intervals.
- The MQL table ends May 2018 while deals close into Nov 2018, so late-2018
  conversion is structurally understated (leads still in flight).
- One deal shows a won_date before its first_contact_date and 33 close on day 0;
  timestamps are operational records, not audited.
- `declared_monthly_revenue` is 94.7% zeros and dominated by outliers; excluded
  from conclusions.
- The 45.1% seller link is bounded by the e-commerce dataset's own window
  (orders to Oct 2018) and seller churn; it is a lower bound on presence in
  the available data, not a measure of onboarding success or failure.
