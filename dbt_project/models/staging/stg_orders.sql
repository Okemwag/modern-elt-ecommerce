with source as (

    select * from {{ source('airbyte_bronze', 'orders_raw') }}

),

typed as (

    select
        try_cast(order_id as bigint) as order_id,
        try_cast(customer_id as bigint) as customer_id,
        try_cast(order_date as timestamp) as order_date,
        case
            when lower(trim(order_status)) in ('complete', 'completed', 'success') then 'completed'
            when lower(trim(order_status)) in ('cancelled', 'canceled') then 'cancelled'
            when lower(trim(order_status)) in ('returned', 'return') then 'returned'
            else 'pending'
        end as order_status,
        case
            when lower(trim(payment_status)) in ('paid', 'success', 'successful') then 'paid'
            when lower(trim(payment_status)) in ('failed', 'declined') then 'failed'
            when lower(trim(payment_status)) in ('refunded', 'refund') then 'refunded'
            else 'pending'
        end as payment_status,
        try_cast(shipping_region_id as bigint) as region_id,
        try_cast(total_amount as decimal(18, 2)) as gross_amount,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(order_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by order_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    order_id,
    customer_id,
    order_date,
    order_status,
    payment_status,
    region_id,
    gross_amount,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
