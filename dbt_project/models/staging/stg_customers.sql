with source as (

    select * from {{ source('airbyte_bronze', 'customers_raw') }}

),

typed as (

    select
        try_cast(customer_id as bigint) as customer_id,
        nullif(trim(first_name), '') as first_name,
        nullif(trim(last_name), '') as last_name,
        lower(nullif(trim(email), '')) as email,
        nullif(trim(phone), '') as phone,
        nullif(trim(city), '') as city,
        upper(nullif(trim(country), '')) as country,
        try_cast(created_at as timestamp) as customer_created_at,
        try_cast(_airbyte_extracted_at as timestamp) as airbyte_extracted_at,
        try_cast(_airbyte_loaded_at as timestamp) as airbyte_loaded_at,
        _airbyte_raw_id as airbyte_raw_id
    from source
    where try_cast(customer_id as bigint) is not null

),

deduped as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by customer_id
                order by airbyte_loaded_at desc, airbyte_extracted_at desc
            ) as row_number
        from typed
    )
    where row_number = 1

)

select
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    country,
    customer_created_at,
    airbyte_extracted_at,
    airbyte_loaded_at,
    airbyte_raw_id
from deduped
