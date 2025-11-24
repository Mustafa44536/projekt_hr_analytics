USE ROLE SECURITYADMIN;

-- skapa roll för ETL (dlt)
CREATE ROLE IF NOT EXISTS ETL_DLT_ROLE;

-- roll för dbt-transform
CREATE ROLE IF NOT EXISTS TRANSFORM_DBT_ROLE;

-- roll för BI / dashboard / read-only
CREATE ROLE IF NOT EXISTS BI_ROLE;
