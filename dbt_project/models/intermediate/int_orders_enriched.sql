with orders as (

    select * from {{ ref('stg_orders') }}

),

line_amounts as (

    select
        order_id,
        sum(gross_line_amount) as gross_item_amount,
        sum(net_line_amount) as net_item_amount,
        sum(quantity) as total_items
    from {{ ref('int_order_line_amounts') }}
    group by order_id

),

payments as (

    select
        order_id,
        sum(case when payment_status = 'paid' then payment_amount else 0 end) as paid_amount,
        max(case when payment_status = 'paid' then 1 else 0 end) as has_successful_payment
    from {{ ref('stg_payments') }}
    group by order_id

)

select
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    to_date(orders.order_date) as order_date_day,
    orders.order_status,
    orders.payment_status,
    orders.region_id,
    orders.gross_amount,
    coalesce(line_amounts.gross_item_amount, orders.gross_amount) as gross_item_amount,
    coalesce(line_amounts.net_item_amount, orders.gross_amount) as net_order_amount,
    coalesce(line_amounts.total_items, 0) as total_items,
    coalesce(payments.paid_amount, 0) as paid_amount,
    coalesce(payments.has_successful_payment, 0) as has_successful_payment
from orders
left join line_amounts
    on orders.order_id = line_amounts.order_id
left join payments
    on orders.order_id = payments.order_id
