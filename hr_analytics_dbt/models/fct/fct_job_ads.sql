{{ config(materialized='table') }}

select
    '6Hq3_tKo_V57' as occupation_field_id,
    'NYW6_mP6_vwf' as occupation_field_id_business,
    'MVqp_eS8_kDZ' as occupation_field_id_health,
    'Data/IT' as occupation_name,
    current_date as created_at

