{{ config(materialized='view') }}

select *
from {{ ref('fact_job_ads') }}
where occupation_field_id = 'NYW6_mP6_vwf'

