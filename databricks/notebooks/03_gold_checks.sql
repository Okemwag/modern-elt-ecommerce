use catalog ecommerce;
use schema gold;

select
    revenue_month,
    total_orders,
    unique_customers,
    total_revenue,
    avg_order_value
from mart_monthly_revenue
order by revenue_month;

select
    product_name,
    category_name,
    units_sold,
    net_revenue
from mart_top_products
order by net_revenue desc
limit 10;

select
    customer_segment,
    count(*) as customers,
    sum(lifetime_value) as lifetime_value
from mart_repeat_customers
group by customer_segment;
