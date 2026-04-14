select payments.*
from {{ ref('fct_payments') }} as payments
left join {{ ref('fct_orders') }} as orders
    on payments.order_id = orders.order_id
where orders.order_id is null
