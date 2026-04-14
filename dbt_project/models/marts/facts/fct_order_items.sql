with line_amounts as (

    select * from {{ ref('int_order_line_amounts') }}

),

orders as (

    select
        order_id,
        customer_id,
        order_date_day,
        order_status,
        region_id
    from {{ ref('fct_orders') }}

)

select
    line_amounts.order_item_id,
    line_amounts.order_id,
    orders.customer_id,
    line_amounts.product_id,
    orders.order_date_day,
    orders.order_status,
    orders.region_id,
    line_amounts.quantity,
    line_amounts.unit_price,
    line_amounts.discount_amount,
    line_amounts.gross_line_amount,
    line_amounts.net_line_amount
from line_amounts
left join orders
    on line_amounts.order_id = orders.order_id
