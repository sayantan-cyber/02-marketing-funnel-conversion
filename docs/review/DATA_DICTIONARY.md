# Data dictionary (measured from the raw files, 17 Oct 2026)

## olist_marketing_qualified_leads_dataset.csv - 8,000 rows x 4 columns

| Column | Type | Nulls | Unique | Meaning |
| --- | --- | --- | --- | --- |
| mql_id | string (32-char hash) | 0 | 8,000 | Lead ID, primary key |
| first_contact_date | date | 0 | 336 | Day the lead first made contact (2017-06-14 to 2018-05-31) |
| landing_page_id | string (32-char hash) | 0 | 495 | Which signup landing page the lead arrived on |
| origin | string | 60 | 10 | Acquisition channel. Values: organic_search 2,296; paid_search 1,586; social 1,350; unknown 1,099; direct_traffic 499; email 493; referral 284; other 150; display 118; other_publicities 65. Note: "unknown" is a literal recorded value; 60 rows have a truly empty origin and fall out of per-channel breakdowns (they stay in the overall 8,000). |

## olist_closed_deals_dataset.csv - 842 rows x 14 columns

| Column | Type | Nulls | Unique | Meaning |
| --- | --- | --- | --- | --- |
| mql_id | string | 0 | 842 | Lead that closed; joins marketing_qualified_leads 1:1 (100% coverage) |
| seller_id | string | 0 | 842 | Seller ID created at signing; joins the e-commerce dataset's sellers table |
| sdr_id | string | 0 | 32 | Sales development rep (anonymized) |
| sr_id | string | 0 | 22 | Sales rep who closed (anonymized) |
| won_date | datetime | 0 | 824 | When the deal was won (2017-12-05 to 2018-11-14) |
| business_segment | string | 1 | 33 | Market segment of the lead's business |
| lead_type | string | 6 | 8 | Lead classification: online_medium 332; online_big 126; industry 123; offline 104; online_small 77; online_beginner 57; online_top 14; other 3 |
| lead_behaviour_profile | string | 177 | 9 | Olist's behavioural label (cat, eagle, wolf, shark, plus 5 combos) |
| has_company | string | 779 | 2 | Has a registered company; 92.5% empty |
| has_gtin | string | 778 | 2 | Products have barcodes; 92.4% empty |
| average_stock | string | 776 | 6 | Stock size bucket; 92.2% empty |
| business_type | string | 10 | 3 | reseller 587; manufacturer 242; other 3 |
| declared_product_catalog_size | number | 773 | 33 | Self-declared catalog size; 91.8% empty |
| declared_monthly_revenue | number | 0 | 27 | Self-declared monthly revenue in R$; 94.7% of rows are 0, and 97.4% of the non-zero total sits in 10 deals. Treated as unreliable, excluded from conclusions. |

Empty optional fields (has_company, has_gtin, average_stock, declared_product_catalog_size)
were collected only in later signup form versions, which is why they are mostly blank.
