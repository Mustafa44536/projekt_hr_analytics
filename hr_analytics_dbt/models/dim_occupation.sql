{{ config(materialized='table') }}

select distinct
    occupation_field_id,
    occupation_name
from {{ ref('fact_job_ads') }}

