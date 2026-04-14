with source as (

    select * from {{ source('airbyte_bronze', 'products_raw') }}

),

typed as (

    select
        try_cast(product_id as bigint) as product_id,
        nullif(trim(product_name), '') as product_name,
        try_cast(category_id as bigint) as category_id,
        nullif(trim(brand), '') as brand,
        try_cast(unit_cost as decimal(18, 2)) as unit_cost,
        try_cast(list_price as decimal(18, 2)) as list_price,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(product_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by product_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    product_id,
    product_name,
    category_id,
    brand,
    unit_cost,
    list_price,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
