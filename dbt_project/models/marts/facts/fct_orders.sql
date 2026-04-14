select
    order_id,
    customer_id,
    order_date,
    order_date_day,
    order_status,
    payment_status,
    region_id,
    gross_amount,
    gross_item_amount,
    net_order_amount,
    total_items,
    paid_amount,
    has_successful_payment
from {{ ref('int_orders_enriched') }}
