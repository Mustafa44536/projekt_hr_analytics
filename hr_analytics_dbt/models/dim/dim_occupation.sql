{{ config(materialized='view') }}

with src as (
  select * from {{ ref('src_occupation') }}
)
select
  {{ dbt_utils.generate_surrogate_key(['occupation']) }} as occupation_id,
  occupation,
  max(occupation_group) as occupation_group,
  max(occupation_field) as occupation_field
from src
group by occupation
