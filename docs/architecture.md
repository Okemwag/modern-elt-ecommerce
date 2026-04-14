# Architecture

## Goal

Build a modern ELT analytics platform for e-commerce reporting. The platform ingests operational and file-based data, stores raw records in Databricks Delta tables, transforms data with dbt, and exposes trusted gold models for BI.

## System Flow

```text
                +------------------+
                | Source Systems   |
                | PostgreSQL, CSV  |
                +---------+--------+
                          |
                          v
                +------------------+
                | Airbyte          |
                | Extract + Load   |
                +---------+--------+
                          |
                          v
                +---------------------------+
                | Databricks Lakehouse      |
                | bronze / silver / gold    |
                +---------+-----------------+
                          |
                          v
                +------------------+
                | dbt              |
                | Tests + Models   |
                +---------+--------+
                          |
                          v
                +------------------+
                | BI Dashboard     |
                +------------------+
```

## Lakehouse Layers

### Bronze

Raw Airbyte-loaded data. Tables preserve source columns and ingestion metadata such as `_airbyte_raw_id`, `_airbyte_extracted_at`, and `_airbyte_loaded_at`.

Example tables:

- `ecommerce.bronze.customers_raw`
- `ecommerce.bronze.orders_raw`
- `ecommerce.bronze.order_items_raw`
- `ecommerce.bronze.payments_raw`
- `ecommerce.bronze.products_raw`
- `ecommerce.bronze.categories_raw`
- `ecommerce.bronze.regions_raw`

### Silver

Cleaned and standardized source-aligned models built by dbt staging models.

Example models:

- `ecommerce.silver.stg_customers`
- `ecommerce.silver.stg_orders`
- `ecommerce.silver.stg_order_items`
- `ecommerce.silver.stg_payments`
- `ecommerce.silver.stg_products`
- `ecommerce.silver.stg_categories`
- `ecommerce.silver.stg_regions`

### Gold

Dimensional models, facts, and marts for BI.

Example models:

- `ecommerce.gold.dim_customers`
- `ecommerce.gold.dim_products`
- `ecommerce.gold.fct_orders`
- `ecommerce.gold.fct_order_items`
- `ecommerce.gold.mart_monthly_revenue`

## Ownership Boundaries

- Airbyte owns extraction and loading only.
- Databricks owns storage, compute, Delta Lake, and workflow execution.
- dbt owns transformations, tests, documentation, and model contracts.
- BI tools consume only gold-layer models.
