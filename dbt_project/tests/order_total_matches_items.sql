with order_totals as (

    select
        order_id,
        net_order_amount
    from {{ ref('fct_orders') }}
    where order_status = 'completed'

),

item_totals as (

    select
        order_id,
        sum(net_line_amount) as item_net_amount
    from {{ ref('fct_order_items') }}
    group by order_id

)

select
    order_totals.order_id,
    order_totals.net_order_amount,
    item_totals.item_net_amount
from order_totals
left join item_totals
    on order_totals.order_id = item_totals.order_id
where abs(order_totals.net_order_amount - item_totals.item_net_amount) > 0.01
