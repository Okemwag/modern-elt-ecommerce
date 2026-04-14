# Data Dictionary

## Source Tables

### customers

| Column | Description |
| --- | --- |
| customer_id | Primary key for the customer |
| first_name | Customer first name |
| last_name | Customer last name |
| email | Customer email address |
| phone | Customer phone number |
| city | Customer city |
| country | Customer country |
| created_at | Customer creation timestamp |

### orders

| Column | Description |
| --- | --- |
| order_id | Primary key for the order |
| customer_id | Customer who placed the order |
| order_date | Order timestamp |
| order_status | Order lifecycle status |
| payment_status | Payment lifecycle status |
| shipping_region_id | Region used for fulfillment or shipping |
| total_amount | Source order total |

### order_items

| Column | Description |
| --- | --- |
| order_item_id | Primary key for the line item |
| order_id | Parent order |
| product_id | Product sold |
| quantity | Units purchased |
| unit_price | Unit sale price |
| discount_amount | Discount applied to the line |

### payments

| Column | Description |
| --- | --- |
| payment_id | Primary key for the payment |
| order_id | Parent order |
| payment_method | Payment method such as card, paypal, bank_transfer, or mobile_money |
| payment_status | Payment status |
| payment_amount | Payment amount |
| paid_at | Payment timestamp |

### products

| Column | Description |
| --- | --- |
| product_id | Primary key for the product |
| product_name | Product name |
| category_id | Product category |
| brand | Product brand |
| unit_cost | Product unit cost |
| list_price | Product list price |

### categories

| Column | Description |
| --- | --- |
| category_id | Primary key for the category |
| category_name | Category name |

### regions

| Column | Description |
| --- | --- |
| region_id | Primary key for the region |
| region_name | Region name |
| country | Region country |

## Key Metrics

| Metric | Definition |
| --- | --- |
| Gross amount | Source order total |
| Net order amount | Sum of line item totals after discounts |
| Average order value | Net revenue divided by completed order count |
| Repeat customer | Customer with at least two completed orders |
| Lifetime value | Sum of completed net order amount for a customer |
| Payment success rate | Successful payments divided by all payments |
