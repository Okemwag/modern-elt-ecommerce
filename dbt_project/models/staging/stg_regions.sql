with source as (

    select * from {{ source('airbyte_bronze', 'regions_raw') }}

),

typed as (

    select
        try_cast(region_id as bigint) as region_id,
        nullif(trim(region_name), '') as region_name,
        upper(nullif(trim(country), '')) as country,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(region_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by region_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    region_id,
    region_name,
    country,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
