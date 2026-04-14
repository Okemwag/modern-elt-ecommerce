# Modern ELT Pipeline for E-commerce Analytics

This project is a portfolio-ready blueprint for an end-to-end ELT pipeline using Airbyte, Databricks, and dbt.

The business case is an e-commerce company that wants one analytics platform for revenue, product performance, customer behavior, payment quality, and regional performance.

## Architecture

```text
PostgreSQL + CSV files
        |
        v
Airbyte extraction and loading
        |
        v
Databricks Lakehouse
  - bronze: raw Airbyte tables
  - silver: cleaned dbt staging models
  - gold: dimensions, facts, and marts
        |
        v
BI dashboard: Power BI, Tableau, or Metabase
```

## What This Demonstrates

- Multi-source ingestion design with Airbyte
- Databricks lakehouse layout with bronze, silver, and gold layers
- dbt transformation structure with staging, intermediate, dimensions, facts, and marts
- Data quality tests for keys, relationships, accepted values, and business rules
- Analytics-ready outputs for dashboards

## Project Structure

```text
modern-elt-ecommerce/
├── README.md
├── docs/
├── airbyte/
├── databricks/
├── dbt_project/
├── data/
└── dashboard/
```

## Primary Tables

- `customers`
- `orders`
- `order_items`
- `payments`
- `products`
- `categories`
- `regions`

## Gold Models

- `dim_customers`
- `dim_products`
- `dim_regions`
- `fct_orders`
- `fct_order_items`
- `fct_payments`
- `mart_monthly_revenue`
- `mart_top_products`
- `mart_repeat_customers`

## Setup Summary

1. Load the sample PostgreSQL tables from [data/sample_data/postgres_seed.sql](data/sample_data/postgres_seed.sql).
2. Configure Airbyte PostgreSQL and file sources using the notes in [airbyte/README.md](airbyte/README.md).
3. Create the Databricks catalog and schemas with [databricks/setup/create_catalogs.sql](databricks/setup/create_catalogs.sql).
4. Configure a dbt Databricks profile from [dbt_project/profiles.example.yml](dbt_project/profiles.example.yml).
5. From `dbt_project/`, run:

```bash
dbt deps
dbt debug
dbt run
dbt test
dbt docs generate
```

## MVP Scope

The MVP uses PostgreSQL for transactional tables and CSV files for reference data. Airbyte lands raw data into the bronze layer. dbt creates silver staging models and gold analytics models.

## Advanced Extensions

- Add dbt snapshots for customer or product SCD Type 2 history.
- Add incremental models for high-volume fact tables.
- Add Databricks Workflows or Airflow orchestration.
- Add CI checks for `dbt build`.
- Add BI dashboard screenshots under `airbyte/screenshots/` and `dashboard/`.
