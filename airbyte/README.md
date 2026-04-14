# Airbyte Setup

Airbyte handles extraction and loading into Databricks. Transformations should stay in dbt.

## Sources

### PostgreSQL

Use PostgreSQL for transactional data:

- `customers`
- `orders`
- `order_items`
- `payments`

Suggested sync mode:

- `customers`: incremental append or incremental dedupe
- `orders`: incremental append or incremental dedupe
- `order_items`: incremental append or incremental dedupe
- `payments`: incremental append or incremental dedupe

Cursor fields:

- `customers.created_at`
- `orders.order_date`
- `payments.paid_at`

For `order_items`, use an updated timestamp if you add one. If not, use full refresh for the MVP.

### CSV File Source

Use file ingestion for reference data:

- `products`
- `categories`
- `regions`

Suggested sync mode:

- Full refresh overwrite for MVP
- Incremental only if the source files include reliable update timestamps

## Destination

Use Databricks as the destination. Land raw data in:

```text
catalog: ecommerce
schema: bronze
```

Expected raw table names:

- `customers_raw`
- `orders_raw`
- `order_items_raw`
- `payments_raw`
- `products_raw`
- `categories_raw`
- `regions_raw`

If Airbyte creates different table names, update [../dbt_project/models/staging/sources.yml](../dbt_project/models/staging/sources.yml).

## Portfolio Screenshots

Add screenshots to `airbyte/screenshots/` after configuration:

- PostgreSQL source
- File source
- Databricks destination
- Successful sync history
- Connection table selection
