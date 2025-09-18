with src_job_ads as (
    select * from {{ ref('src_job_ads') }}
),
dim_job_details as (
    select * from {{ ref('dim_job_details') }}
),
dim_employer as (
    select * from {{ ref('dim_employer') }}
),
dim_auxiliary_attributes as (
    select * from {{ ref('dim_auxiliary_attributes') }}
),
dim_occupation as (
    select * from {{ ref('dim_occupation') }}
)

select
    o.occupation_id,
    d.job_details_id,
    e.employer_id,
    a.auxiliary_attributes_id,
    j.vacancies,
    j.relevance,
    j.application_deadline
from src_job_ads j
left join dim_job_details d
    on j.job_id = d.job_id
left join dim_employer e
    on j.job_id = e.job_id
left join dim_auxiliary_attributes a
    on j.job_id = a.job_id
left join dim_occupation o
    on j.job_id = o.job_id

