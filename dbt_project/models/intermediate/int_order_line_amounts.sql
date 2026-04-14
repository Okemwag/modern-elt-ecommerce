with order_items as (

    select * from {{ ref('stg_order_items') }}

)

select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    cast((quantity * unit_price) as decimal(18, 2)) as gross_line_amount,
    cast(((quantity * unit_price) - discount_amount) as decimal(18, 2)) as net_line_amount
from order_items
