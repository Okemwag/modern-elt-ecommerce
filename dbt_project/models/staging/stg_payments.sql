with source as (

    select * from {{ source('airbyte_bronze', 'payments_raw') }}

),

typed as (

    select
        try_cast(payment_id as bigint) as payment_id,
        try_cast(order_id as bigint) as order_id,
        lower(nullif(trim(payment_method), '')) as payment_method,
        case
            when lower(trim(payment_status)) in ('paid', 'success', 'successful') then 'paid'
            when lower(trim(payment_status)) in ('failed', 'declined') then 'failed'
            when lower(trim(payment_status)) in ('refunded', 'refund') then 'refunded'
            else 'pending'
        end as payment_status,
        try_cast(payment_amount as decimal(18, 2)) as payment_amount,
        try_cast(paid_at as timestamp) as paid_at,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(payment_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by payment_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    payment_id,
    order_id,
    payment_method,
    payment_status,
    payment_amount,
    paid_at,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
