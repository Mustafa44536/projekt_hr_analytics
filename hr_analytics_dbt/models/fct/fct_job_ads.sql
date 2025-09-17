{{ config(materialized='view') }}

with ads as (
  select
    occupation__label,
    vacancies,
    relevance,
    application_deadline
  from {{ ref('src_job_ads') }}
),
d_occ as (
  select occupation_id, occupation
  from {{ ref('dim_occupation') }}
)
select
  {{ dbt_utils.generate_surrogate_key([
      'ads.occupation__label',
      "to_char(application_deadline, 'YYYY-MM-DD')",
      'coalesce(cast(vacancies as varchar), '''')',
      'coalesce(cast(relevance as varchar), '''')'
  ]) }} as job_ads_id,
  d_occ.occupation_id,
  ads.vacancies,
  ads.relevance,
  ads.application_deadline as posted_at
from ads
left join d_occ
  on ads.occupation__label = d_occ.occupation
