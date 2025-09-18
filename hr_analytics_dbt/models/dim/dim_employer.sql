with src_employer as (
    select * from {{ ref('src_employer') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['job_id']) }} as employer_id,
    job_id,
    employer_name,
    employer_workplace,
    employer_organization_number,
    coalesce(workplace_street_address, 'Okänd') as workplace_street_address,
    workplace_region,
    workplace_postcode,
    coalesce(workplace_city, 'Okänd') as workplace_city,
    workplace_country
from src_employer
