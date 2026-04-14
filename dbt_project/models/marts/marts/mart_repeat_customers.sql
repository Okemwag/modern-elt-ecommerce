select
    customer_id,
    full_name,
    email,
    country,
    total_orders,
    first_order_date,
    last_order_date,
    lifetime_value,
    is_repeat_customer,
    case
        when is_repeat_customer then 'repeat'
        else 'one_time_or_no_orders'
    end as customer_segment
from {{ ref('dim_customers') }}
