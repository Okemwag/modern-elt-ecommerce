use catalog ecommerce;
use schema bronze;

select 'customers_raw' as table_name, count(*) as row_count from customers_raw
union all
select 'orders_raw' as table_name, count(*) as row_count from orders_raw
union all
select 'order_items_raw' as table_name, count(*) as row_count from order_items_raw
union all
select 'payments_raw' as table_name, count(*) as row_count from payments_raw
union all
select 'products_raw' as table_name, count(*) as row_count from products_raw
union all
select 'categories_raw' as table_name, count(*) as row_count from categories_raw
union all
select 'regions_raw' as table_name, count(*) as row_count from regions_raw;

select
    'orders_raw' as table_name,
    min(_airbyte_loaded_at) as first_loaded_at,
    max(_airbyte_loaded_at) as last_loaded_at
from orders_raw;
