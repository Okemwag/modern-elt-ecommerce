with source as (

    select * from {{ source('airbyte_bronze', 'categories_raw') }}

),

typed as (

    select
        try_cast(category_id as bigint) as category_id,
        nullif(trim(category_name), '') as category_name,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(category_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by category_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    category_id,
    category_name,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
