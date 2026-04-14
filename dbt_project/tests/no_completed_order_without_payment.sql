select *
from {{ ref('fct_orders') }}
where order_status = 'completed'
  and has_successful_payment = 0
