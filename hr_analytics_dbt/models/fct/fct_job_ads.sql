with job_ads as (
  select * from {{ ref('src_job_ads') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['occupation__label']) }} as occupation_id,
    {{ dbt_utils.generate_surrogate_key(['occupation__label','application_deadline']) }} as job_details_id,
    {{ dbt_utils.generate_surrogate_key(['occupation__label']) }} as employer_id,
    {{ dbt_utils.generate_surrogate_key(['occupation__label']) }} as auxilliary_attributes_id,
    vacancies,
    relevance,
    application_deadline
from job_ads
