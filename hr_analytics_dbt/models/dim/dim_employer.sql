with src_employer as (
    select * from {{ ref('src_employer') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['employer_workplace', 'workplace_city']) }} as employer_id,
    employer_workplace,
    max(employer_name) as employer_name,
    max(employer_organization_number) as employer_organization_number,
    max(workplace_street_address) as workplace_street_address,
    max(workplace_region) as workplace_region,
    max(workplace_postcode) as workplace_postcode,
    max(workplace_city) as workplace_city,
    max(workplace_country) as workplace_country
from src_employer
group by employer_workplace, workplace_city
