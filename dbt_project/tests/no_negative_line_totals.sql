select *
from {{ ref('fct_order_items') }}
where net_line_amount < 0
   or gross_line_amount < 0
