with src_occupation as (
    select * from {{ ref('src_occupation') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['job_id']) }} as occupation_id,
    job_id,
    occupation,
    occupation_group,
    occupation_field
from src_occupation
group by job_id, occupation, occupation_group, occupation_field

