with
    fct_job_ads as (select * from {{ ref('fct_job_ads') }}),
    dim_occupation as (select * from {{ ref('dim_occupation') }}),
    dim_employer as (select * from {{ ref('dim_employer') }}),
    dim_auxiliary_attributes as (select * from {{ ref('dim_auxiliary_attributes') }}),
    dim_job_details as (select * from {{ ref('dim_job_details') }})
select
    f.vacancies,
    f.relevance,
    o.occupation,
    o.occupation_group,
    o.occupation_field,
    f.application_deadline,
    j.headline,
    j.description,
    j.description_html_formatted,
    j.employment_type,
    j.duration,
    j.salary_type,
    j.scope_of_work_min,
    j.scope_of_work_max,
    e.employer_name,
    e.workplace_city,
    e.employer_workplace,
    e.workplace_street_address,
    e.workplace_region,
    e.workplace_postcode,
    e.employer_organization_number,
    e.workplace_country,
    a.experience_required,
    a.driver_license,
    a.access_to_own_car
from fct_job_ads f
inner join dim_occupation o on f.occupation_id = o.occupation_id
left join dim_job_details j on f.job_details_id = j.job_details_id
left join dim_employer e on f.employer_id = e.employer_id
left join dim_auxiliary_attributes a on f.auxiliary_attributes_id = a.auxiliary_attributes_id
where o.occupation_field = 'Försäljning, inköp, marknadsföring'
