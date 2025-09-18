with src_auxiliary_attributes as (
    select * from {{ ref('src_auxiliary_attributes') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['job_id']) }} as auxiliary_attributes_id,
    job_id,
    experience_required,
    driver_license,
    access_to_own_car
from src_auxiliary_attributes