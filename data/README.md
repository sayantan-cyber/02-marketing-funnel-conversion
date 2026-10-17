# Data

The raw CSVs are NOT committed to this repository (CC BY-NC-SA 4.0 license
hygiene). To reproduce every number, download exactly these files:

## This project's dataset: Marketing Funnel by Olist

- Original source (Kaggle, published by Olist, license CC BY-NC-SA 4.0):
  https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist
- Direct download used for this analysis (GitHub mirror, verified byte counts
  703,836 and 171,352 on 17 Oct 2026):
  - https://raw.githubusercontent.com/dujiaying/olist/master/data/olist_marketing_qualified_leads_dataset.csv
  - https://raw.githubusercontent.com/dujiaying/olist/master/data/olist_closed_deals_dataset.csv

Place in this folder as:
olist_marketing_qualified_leads_dataset.csv   (expect 8,000 rows x 4 cols)
olist_closed_deals_dataset.csv                (expect 842 rows x 14 cols)

## For the 45.1% seller link check only

Also download olist_sellers_dataset.csv from Project 1's dataset,
"Brazilian E-Commerce Public Dataset by Olist" (same license):
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
(expect 3,095 rows x 4 cols). Without it the pipeline still runs; it just
skips the seller-link line.

The pipeline's validation checks fail loudly if the files do not match these
shapes, so a wrong or corrupted download cannot silently produce numbers.

License: CC BY-NC-SA 4.0. Credit Olist and keep the same license on anything
derived that you share.
