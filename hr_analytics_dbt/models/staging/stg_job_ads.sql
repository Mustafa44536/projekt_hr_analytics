{{ config(materialized='view') }}

with raw as (
    select *
    from {{ source('staging', 'job_ads') }}
)

select
    cast(id as varchar) as job_ad_id,
    initcap(title) as job_title,
    upper(municipality) as city,
    occupation_field,
    occupation_group,
    employment_type,
    try_cast(publication_date as date) as publication_date,
    current_timestamp() as dbt_loaded_at
from raw

