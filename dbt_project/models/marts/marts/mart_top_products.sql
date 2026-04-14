with order_items as (

    select * from {{ ref('fct_order_items') }}
    where order_status = 'completed'

),

products as (

    select * from {{ ref('dim_products') }}

)

select
    products.product_id,
    products.product_name,
    products.category_name,
    products.brand,
    sum(order_items.quantity) as units_sold,
    sum(order_items.net_line_amount) as net_revenue,
    sum(order_items.gross_line_amount) as gross_revenue
from order_items
left join products
    on order_items.product_id = products.product_id
group by
    products.product_id,
    products.product_name,
    products.category_name,
    products.brand
