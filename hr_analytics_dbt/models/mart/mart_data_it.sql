{{ config(materialized='view') }}

select
  f.*,
  o.occupation_name as occupation_name_norm
from {{ ref('fact_job_ads') }} f
left join {{ ref('dim_occupation') }} o
  on f.occupation_field_id = o.occupation_field_id
where f.occupation_field_id = '6Hq3_tKo_V57'

