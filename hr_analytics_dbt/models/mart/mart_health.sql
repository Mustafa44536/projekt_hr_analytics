{{ config(materialized='view') }}

select *
from {{ ref('fact_job_ads') }}
where occupation_field_id = 'MVqp_eS8_kDZ'

