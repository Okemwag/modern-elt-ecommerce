with orders as (

    select * from {{ ref('int_orders_enriched') }}
    where order_status = 'completed'

)

select
    customer_id,
    min(order_date) as first_order_date,
    max(order_date) as last_order_date,
    count(distinct order_id) as total_orders,
    sum(net_order_amount) as lifetime_value,
    case when count(distinct order_id) >= 2 then true else false end as is_repeat_customer
from orders
group by customer_id
