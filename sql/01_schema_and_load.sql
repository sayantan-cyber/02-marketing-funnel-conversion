-- Project 2: Marketing Funnel (Olist) - schema and load, MySQL 8
CREATE DATABASE IF NOT EXISTS olist_marketing CHARACTER SET utf8mb4;
USE olist_marketing;

CREATE TABLE marketing_qualified_leads (
    mql_id CHAR(32) PRIMARY KEY,
    first_contact_date DATE NOT NULL,
    landing_page_id CHAR(32),
    origin VARCHAR(40),
    INDEX idx_mql_origin (origin),
    INDEX idx_mql_date (first_contact_date)
);

CREATE TABLE closed_deals (
    mql_id CHAR(32) PRIMARY KEY,
    seller_id CHAR(32),
    sdr_id CHAR(32),
    sr_id CHAR(32),
    won_date DATETIME,
    business_segment VARCHAR(60),
    lead_type VARCHAR(40),
    lead_behaviour_profile VARCHAR(60),
    has_company VARCHAR(10),
    has_gtin VARCHAR(10),
    average_stock VARCHAR(40),
    business_type VARCHAR(40),
    declared_product_catalog_size DOUBLE NULL,
    declared_monthly_revenue DOUBLE NULL,
    INDEX idx_deals_segment (business_segment),
    INDEX idx_deals_seller (seller_id)
);

LOAD DATA LOCAL INFILE 'data/olist_marketing_qualified_leads_dataset.csv'
INTO TABLE marketing_qualified_leads FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA LOCAL INFILE 'data/olist_closed_deals_dataset.csv'
INTO TABLE closed_deals FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
