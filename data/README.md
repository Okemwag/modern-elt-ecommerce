# Sample Data

This project uses deterministic synthetic data designed to mirror a real e-commerce business.

The generator creates:

- 2,500 customers
- 9,000 orders
- Order items with realistic basket sizes, unit prices, and discounts
- One payment record per order
- 260 products
- 12 categories
- 16 regions
- Optional returns, shipping, and inventory datasets for advanced analysis

## Generate Data

From the project root:

```bash
python3 data/scripts/generate_sample_data.py
```

Outputs:

- `data/generated/*.csv`: full analysis extracts
- `data/csv/products.csv`: file-source reference data for Airbyte
- `data/csv/categories.csv`: file-source reference data for Airbyte
- `data/csv/regions.csv`: file-source reference data for Airbyte
- `data/sample_data/postgres_seed.sql`: PostgreSQL transactional seed script
- `source_postgres/init/01_seed.sql`: Docker init script for local PostgreSQL

## Realism Built Into the Dataset

- Repeat and one-time customer behavior
- Mixed order statuses: completed, pending, cancelled, and returned
- Mixed raw status casing to demonstrate standardization in dbt
- Multiple regions and countries
- Category and brand diversity
- Discounts at line-item level
- Payment statuses aligned with order outcomes
- Optional operational datasets for returns, shipping, and inventory
