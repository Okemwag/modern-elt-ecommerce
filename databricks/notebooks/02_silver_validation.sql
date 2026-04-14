use catalog ecommerce;
use schema silver;

select 'stg_customers' as model_name, count(*) as row_count from stg_customers
union all
select 'stg_orders' as model_name, count(*) as row_count from stg_orders
union all
select 'stg_order_items' as model_name, count(*) as row_count from stg_order_items
union all
select 'stg_payments' as model_name, count(*) as row_count from stg_payments
union all
select 'stg_products' as model_name, count(*) as row_count from stg_products
union all
select 'stg_categories' as model_name, count(*) as row_count from stg_categories
union all
select 'stg_regions' as model_name, count(*) as row_count from stg_regions;

select
    order_status,
    payment_status,
    count(*) as orders
from stg_orders
group by order_status, payment_status
order by orders desc;
