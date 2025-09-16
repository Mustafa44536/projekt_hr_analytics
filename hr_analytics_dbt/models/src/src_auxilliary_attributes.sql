with stg_job_ads as (select * from {{ source ('job_ads', 'stg_ads')}})

select 
        experience_required,
        DRIVING_LICENSE_REQUIRED as driver_license,
        ACCESS_TO_OWN_CAR
from stg_job_ads