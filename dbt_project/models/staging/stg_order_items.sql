with source as (

    select * from {{ source('airbyte_bronze', 'order_items_raw') }}

),

typed as (

    select
        try_cast(order_item_id as bigint) as order_item_id,
        try_cast(order_id as bigint) as order_id,
        try_cast(product_id as bigint) as product_id,
        try_cast(quantity as int) as quantity,
        try_cast(unit_price as decimal(18, 2)) as unit_price,
        coalesce(try_cast(discount_amount as decimal(18, 2)), 0.00) as discount_amount,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(order_item_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by order_item_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
