select
    date_trunc('month', order_date_day) as revenue_month,
    count(distinct order_id) as total_orders,
    count(distinct customer_id) as unique_customers,
    sum(net_order_amount) as total_revenue,
    cast(sum(net_order_amount) / nullif(count(distinct order_id), 0) as decimal(18, 2)) as avg_order_value
from {{ ref('fct_orders') }}
where order_status = 'completed'
group by date_trunc('month', order_date_day)
