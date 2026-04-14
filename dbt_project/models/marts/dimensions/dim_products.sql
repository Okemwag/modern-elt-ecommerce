with products as (

    select * from {{ ref('stg_products') }}

),

categories as (

    select * from {{ ref('stg_categories') }}

)

select
    products.product_id,
    products.product_name,
    products.category_id,
    categories.category_name,
    products.brand,
    products.unit_cost,
    products.list_price,
    cast((products.list_price - products.unit_cost) as decimal(18, 2)) as unit_margin
from products
left join categories
    on products.category_id = categories.category_id
