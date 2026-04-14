with customers as (

    select * from {{ ref('stg_customers') }}

),

order_history as (

    select * from {{ ref('int_customer_order_history') }}

)

select
    customers.customer_id,
    customers.first_name,
    customers.last_name,
    concat_ws(' ', customers.first_name, customers.last_name) as full_name,
    customers.email,
    customers.phone,
    customers.city,
    customers.country,
    to_date(customers.customer_created_at) as customer_created_date,
    order_history.first_order_date,
    order_history.last_order_date,
    coalesce(order_history.total_orders, 0) as total_orders,
    coalesce(order_history.lifetime_value, 0) as lifetime_value,
    coalesce(order_history.is_repeat_customer, false) as is_repeat_customer
from customers
left join order_history
    on customers.customer_id = order_history.customer_id
