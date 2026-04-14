# Modern ELT Pipeline for E-commerce Analytics

[![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)](https://databricks.com/)
[![Airbyte](https://img.shields.io/badge/Airbyte-615EFF?style=flat&logo=airbyte&logoColor=white)](https://airbyte.com/)

> **A production-grade, portfolio-ready ELT pipeline demonstrating modern data engineering best practices**

This project showcases an end-to-end Extract, Load, Transform (ELT) data pipeline built with industry-standard tools: **Airbyte** for data ingestion, **Databricks** as the lakehouse platform, and **dbt** for transformation and data quality. Designed for an e-commerce analytics use case, it delivers actionable insights on revenue trends, customer behavior, product performance, and payment quality.

---

## 📋 Table of Contents

- [Business Context](#-business-context)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Models](#-data-models)
- [Getting Started](#-getting-started)
- [Pipeline Execution](#-pipeline-execution)
- [Data Quality & Testing](#-data-quality--testing)
- [Analytics Outputs](#-analytics-outputs)
- [Advanced Extensions](#-advanced-extensions)
- [Documentation](#-documentation)

---

## 🎯 Business Context

An e-commerce company needs a unified analytics platform to answer critical business questions:

- **Revenue Analytics**: What are our monthly revenue trends and growth rates?
- **Customer Insights**: Who are our most valuable customers? What's the repeat purchase rate?
- **Product Performance**: Which products and categories drive the most revenue?
- **Payment Quality**: Are there payment failures or anomalies affecting revenue?
- **Regional Analysis**: How does performance vary across geographic regions?

This pipeline centralizes data from transactional databases and flat files, transforms it into analytics-ready models, and powers dashboards for data-driven decision-making.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐              ┌──────────────────────┐            │
│  │   PostgreSQL DB      │              │     CSV Files        │            │
│  │  ┌────────────────┐  │              │  ┌────────────────┐  │            │
│  │  │ • customers    │  │              │  │ • categories   │  │            │
│  │  │ • orders       │  │              │  │ • regions      │  │            │
│  │  │ • order_items  │  │              │  │ • products     │  │            │
│  │  │ • payments     │  │              │  └────────────────┘  │            │
│  │  └────────────────┘  │              └──────────────────────┘            │
│  └──────────────────────┘                                                   │
│            │                                      │                          │
└────────────┼──────────────────────────────────────┼──────────────────────────┘
             │                                      │
             └──────────────┬───────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INGESTION LAYER (Airbyte)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │  • PostgreSQL Source Connector                                  │      │
│   │  • File (CSV) Source Connector                                  │      │
│   │  • Databricks Destination Connector                             │      │
│   │  • Change Data Capture (CDC) Ready                              │      │
│   │  • Incremental Sync Support                                     │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATABRICKS LAKEHOUSE (Medallion Architecture)            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🥉 BRONZE LAYER (Raw Data)                                        │    │
│  │  ─────────────────────────────────────────────────────────────     │    │
│  │  • Raw Airbyte tables with metadata (_airbyte_*)                  │    │
│  │  • Preserves source structure and history                         │    │
│  │  • No transformations applied                                     │    │
│  │  • Schema: ecommerce_bronze                                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                              │
│                              │ dbt staging models                           │
│                              ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🥈 SILVER LAYER (Cleaned & Standardized)                          │    │
│  │  ─────────────────────────────────────────────────────────────     │    │
│  │  • Type casting and data cleaning                                 │    │
│  │  • Deduplication and standardization                              │    │
│  │  • Column renaming and business logic                             │    │
│  │  • Schema: ecommerce_silver                                       │    │
│  │                                                                    │    │
│  │  Models: stg_customers, stg_orders, stg_order_items,              │    │
│  │          stg_payments, stg_products, stg_categories, stg_regions  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                              │                                              │
│                              │ dbt intermediate & mart models               │
│                              ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🥇 GOLD LAYER (Analytics-Ready)                                   │    │
│  │  ─────────────────────────────────────────────────────────────     │    │
│  │  • Business-ready fact and dimension tables                       │    │
│  │  • Aggregated metrics and KPIs                                    │    │
│  │  • Optimized for query performance                                │    │
│  │  • Schema: ecommerce_gold                                         │    │
│  │                                                                    │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │    │
│  │  │   DIMENSIONS     │  │      FACTS       │  │      MARTS      │ │    │
│  │  ├──────────────────┤  ├──────────────────┤  ├─────────────────┤ │    │
│  │  │ • dim_customers  │  │ • fct_orders     │  │ • monthly_rev   │ │    │
│  │  │ • dim_products   │  │ • fct_order_items│  │ • top_products  │ │    │
│  │  │ • dim_regions    │  │ • fct_payments   │  │ • repeat_cust   │ │    │
│  │  │                  │  │                  │  │ • category_perf │ │    │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘ │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ANALYTICS & VISUALIZATION                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│  │   Power BI   │    │   Tableau    │    │   Metabase   │                 │
│  └──────────────┘    └──────────────┘    └──────────────┘                 │
│                                                                              │
│  • Revenue Dashboards      • Customer Segmentation                          │
│  • Product Analytics       • Payment Quality Monitoring                     │
│  • Regional Performance    • Executive KPI Scorecards                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌────────────────────────────────┐
                    │   ORCHESTRATION & MONITORING   │
                    ├────────────────────────────────┤
                    │ • Databricks Workflows         │
                    │ • dbt Cloud / Airflow          │
                    │ • Data Quality Monitoring      │
                    │ • Lineage & Documentation      │
                    └────────────────────────────────┘
```

### Architecture Principles

- **Medallion Architecture**: Bronze (raw) → Silver (cleaned) → Gold (curated) layers for progressive data refinement
- **ELT over ETL**: Transform data in the lakehouse using SQL, leveraging Databricks compute power
- **Modular Design**: Reusable dbt models with clear separation of concerns (staging, intermediate, marts)
- **Data Quality First**: Comprehensive testing at every layer ensures data reliability
- **Scalability**: Designed to handle growing data volumes with incremental processing

---

## ✨ Key Features

### Data Ingestion
- **Multi-source connectivity** via Airbyte (PostgreSQL, CSV, and extensible to 300+ connectors)
- **Automated schema detection** and evolution handling
- **Incremental sync** capabilities for efficient data loading
- **Change Data Capture (CDC)** ready for real-time updates

### Data Transformation
- **Modular dbt project** with staging, intermediate, and mart layers
- **Dimensional modeling** with star schema (facts and dimensions)
- **Business logic encapsulation** in reusable SQL models
- **Macro-driven schema management** for environment flexibility

### Data Quality
- **Automated testing** for uniqueness, referential integrity, and accepted values
- **Custom business rule tests** (e.g., order totals match line items)
- **Data validation notebooks** for bronze, silver, and gold layers
- **Comprehensive documentation** with dbt docs and data lineage

### Analytics Outputs
- **Customer Lifetime Value (CLV)** and segmentation
- **Revenue trends** with month-over-month growth
- **Product performance** rankings and category analysis
- **Repeat purchase behavior** and cohort analysis
- **Payment quality** monitoring and anomaly detection

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Ingestion** | Airbyte | Multi-source data extraction and loading |
| **Storage & Compute** | Databricks | Unified lakehouse platform with Delta Lake |
| **Transformation** | dbt Core | SQL-based transformations and testing |
| **Orchestration** | Databricks Workflows | Job scheduling and pipeline automation |
| **Visualization** | Power BI / Tableau / Metabase | Business intelligence dashboards |
| **Version Control** | Git | Code versioning and collaboration |
| **Data Format** | Delta Lake | ACID transactions and time travel |

---

## 📁 Project Structure

```text
modern-elt-ecommerce/
│
├── README.md                          # This file
│
├── docs/                              # Comprehensive documentation
│   ├── architecture.md                # Detailed architecture decisions
│   ├── business_questions.md          # Analytics requirements
│   ├── dashboard_mockups.md           # BI dashboard specifications
│   ├── data_dictionary.md             # Complete data catalog
│   └── implementation_plan.md         # Step-by-step setup guide
│
├── airbyte/                           # Airbyte configuration
│   ├── README.md                      # Airbyte setup instructions
│   ├── sources/                       # Source connector configs
│   │   ├── postgres_source.template.json
│   │   └── csv_source.template.json
│   ├── destinations/                  # Destination connector configs
│   │   └── databricks_destination.template.json
│   ├── connections/                   # Connection configurations
│   │   ├── postgres_to_databricks.template.json
│   │   └── csv_to_databricks.template.json
│   └── screenshots/                   # Setup documentation images
│
├── databricks/                        # Databricks assets
│   ├── setup/                         # Initial setup scripts
│   │   ├── create_catalogs.sql        # Catalog creation
│   │   └── create_schemas.sql         # Schema definitions
│   ├── notebooks/                     # Validation notebooks
│   │   ├── 01_bronze_validation.sql
│   │   ├── 02_silver_validation.sql
│   │   └── 03_gold_checks.sql
│   └── workflows/                     # Job definitions
│       └── dbt_job.template.yml
│
├── dbt_project/                       # dbt transformation project
│   ├── dbt_project.yml                # Project configuration
│   ├── profiles.example.yml           # Connection profile template
│   ├── packages.yml                   # dbt package dependencies
│   │
│   ├── models/                        # SQL transformation models
│   │   ├── staging/                   # Silver layer (cleaned data)
│   │   │   ├── sources.yml            # Source definitions
│   │   │   ├── stg_customers.sql
│   │   │   ├── stg_orders.sql
│   │   │   ├── stg_order_items.sql
│   │   │   ├── stg_payments.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_categories.sql
│   │   │   └── stg_regions.sql
│   │   │
│   │   ├── intermediate/              # Business logic layer
│   │   │   ├── int_orders_enriched.sql
│   │   │   ├── int_order_line_amounts.sql
│   │   │   └── int_customer_order_history.sql
│   │   │
│   │   ├── marts/                     # Gold layer (analytics-ready)
│   │   │   ├── dimensions/            # Dimension tables
│   │   │   │   ├── dim_customers.sql
│   │   │   │   ├── dim_products.sql
│   │   │   │   └── dim_regions.sql
│   │   │   │
│   │   │   ├── facts/                 # Fact tables
│   │   │   │   ├── fct_orders.sql
│   │   │   │   ├── fct_order_items.sql
│   │   │   │   └── fct_payments.sql
│   │   │   │
│   │   │   └── marts/                 # Business marts
│   │   │       ├── mart_monthly_revenue.sql
│   │   │       ├── mart_top_products.sql
│   │   │       ├── mart_repeat_customers.sql
│   │   │       └── mart_category_performance.sql
│   │   │
│   │   └── schema.yml                 # Model documentation and tests
│   │
│   ├── macros/                        # Reusable SQL macros
│   │   └── generate_schema_name.sql
│   │
│   ├── tests/                         # Custom data tests
│   │   ├── order_total_matches_items.sql
│   │   ├── no_negative_line_totals.sql
│   │   ├── no_completed_order_without_payment.sql
│   │   └── payments_reference_orders.sql
│   │
│   └── seeds/                         # Static reference data
│
├── data/                              # Sample and generated data
│   ├── sample_data/                   # Seed data for testing
│   ├── csv/                           # CSV source files
│   ├── generated/                     # Synthetic data scripts
│   └── scripts/                       # Data generation utilities
│
├── source_postgres/                   # PostgreSQL setup
│   └── init/                          # Database initialization scripts
│
└── dashboard/                         # BI dashboard exports
    └── (Power BI / Tableau files)
```

---

## 📊 Data Models

### Source Tables (Bronze Layer)

| Table | Source | Records | Description |
|-------|--------|---------|-------------|
| `customers` | PostgreSQL | ~10K | Customer master data |
| `orders` | PostgreSQL | ~50K | Order headers |
| `order_items` | PostgreSQL | ~150K | Order line items |
| `payments` | PostgreSQL | ~50K | Payment transactions |
| `products` | CSV | ~500 | Product catalog |
| `categories` | CSV | ~20 | Product categories |
| `regions` | CSV | ~10 | Geographic regions |

### Staging Models (Silver Layer)

Cleaned and standardized versions of source tables with:
- Type casting and null handling
- Column renaming for consistency
- Deduplication logic
- Business rule application

**Models**: `stg_customers`, `stg_orders`, `stg_order_items`, `stg_payments`, `stg_products`, `stg_categories`, `stg_regions`

### Intermediate Models

Business logic layer for complex transformations:
- `int_orders_enriched`: Orders with customer and region details
- `int_order_line_amounts`: Calculated line item totals
- `int_customer_order_history`: Customer purchase aggregations

### Gold Layer Models

#### Dimensions (Slowly Changing Dimensions Ready)
- **`dim_customers`**: Customer attributes with lifetime metrics
- **`dim_products`**: Product catalog with category hierarchy
- **`dim_regions`**: Geographic dimension

#### Facts (Grain: One row per transaction)
- **`fct_orders`**: Order-level facts with metrics
- **`fct_order_items`**: Line item-level facts
- **`fct_payments`**: Payment transaction facts

#### Business Marts (Aggregated Analytics)
- **`mart_monthly_revenue`**: Revenue trends by month
- **`mart_top_products`**: Product performance rankings
- **`mart_repeat_customers`**: Customer retention analysis
- **`mart_category_performance`**: Category-level metrics

---

## 🚀 Getting Started

### Prerequisites

- **Databricks Workspace** (Community Edition or paid tier)
- **Airbyte** (Cloud or self-hosted)
- **PostgreSQL** (for source data)
- **Python 3.8+** with `dbt-databricks` adapter
- **Git** for version control

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Okemwag/modern-elt-ecommerce.git
cd modern-elt-ecommerce
```

#### 2. Set Up PostgreSQL Source

```bash
# Load sample data into PostgreSQL
psql -U postgres -d ecommerce -f data/sample_data/postgres_seed.sql
```

#### 3. Configure Airbyte

Follow the detailed guide in [`airbyte/README.md`](airbyte/README.md):

1. Create PostgreSQL source connector
2. Create CSV file source connector
3. Create Databricks destination connector
4. Set up connections with sync schedules

#### 4. Initialize Databricks

```sql
-- Run in Databricks SQL Editor
-- Create catalogs and schemas
source databricks/setup/create_catalogs.sql;
source databricks/setup/create_schemas.sql;
```

#### 5. Configure dbt

```bash
cd dbt_project

# Copy and configure profile
cp profiles.example.yml ~/.dbt/profiles.yml
# Edit with your Databricks credentials

# Install dependencies
dbt deps

# Test connection
dbt debug
```

---

## ⚙️ Pipeline Execution

### Full Pipeline Run

```bash
cd dbt_project

# Run all models
dbt run

# Execute all tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### Selective Execution

```bash
# Run only staging models
dbt run --select staging

# Run specific model and downstream dependencies
dbt run --select mart_monthly_revenue+

# Test specific model
dbt test --select dim_customers

# Run models modified in current branch
dbt run --select state:modified+
```

### Production Deployment

```bash
# Full build with tests
dbt build --target prod

# Incremental run for large tables
dbt run --select fct_orders --full-refresh
```

---

## ✅ Data Quality & Testing

### Test Coverage

| Test Type | Count | Examples |
|-----------|-------|----------|
| **Uniqueness** | 15 | Primary keys across all tables |
| **Not Null** | 25 | Critical business fields |
| **Referential Integrity** | 12 | Foreign key relationships |
| **Accepted Values** | 8 | Status codes, categories |
| **Custom Business Rules** | 4 | Order totals, payment validation |

### Custom Tests

```sql
-- Example: Order total matches sum of line items
-- tests/order_total_matches_items.sql
select
    order_id,
    order_total,
    sum_line_totals
from {{ ref('fct_orders') }}
where abs(order_total - sum_line_totals) > 0.01
```

### Validation Notebooks

Run validation checks in Databricks:
- `01_bronze_validation.sql`: Raw data quality checks
- `02_silver_validation.sql`: Staging model validation
- `03_gold_checks.sql`: Business logic verification

---

## 📈 Analytics Outputs

### Key Metrics Delivered

1. **Revenue Analytics**
   - Monthly revenue trends
   - Year-over-year growth
   - Revenue by region and category

2. **Customer Insights**
   - Customer lifetime value (CLV)
   - Repeat purchase rate
   - Customer segmentation (high/medium/low value)

3. **Product Performance**
   - Top 10 products by revenue
   - Category performance comparison
   - Product profitability analysis

4. **Operational Metrics**
   - Payment success rates
   - Order fulfillment metrics
   - Regional performance benchmarks

### Sample Queries

```sql
-- Monthly revenue trend
SELECT * FROM ecommerce_gold.mart_monthly_revenue
ORDER BY order_month DESC;

-- Top customers by lifetime value
SELECT * FROM ecommerce_gold.dim_customers
ORDER BY total_lifetime_value DESC
LIMIT 10;

-- Product performance
SELECT * FROM ecommerce_gold.mart_top_products
WHERE rank <= 20;
```

---

## 🔧 Advanced Extensions

### Recommended Enhancements

1. **Incremental Models**
   ```sql
   -- Convert large fact tables to incremental
   {{ config(materialized='incremental', unique_key='order_id') }}
   ```

2. **Slowly Changing Dimensions (SCD Type 2)**
   ```sql
   -- Track historical changes in customer attributes
   {{ config(materialized='snapshot') }}
   ```

3. **Orchestration**
   - Databricks Workflows for scheduled runs
   - Apache Airflow for complex dependencies
   - dbt Cloud for managed execution

4. **CI/CD Pipeline**
   ```yaml
   # GitHub Actions example
   - name: Run dbt tests
     run: dbt test --select state:modified+
   ```

5. **Data Observability**
   - Integrate with Monte Carlo or Datafold
   - Set up dbt Cloud monitoring
   - Custom alerting on test failures

6. **Performance Optimization**
   - Partition large tables by date
   - Z-order clustering on frequently filtered columns
   - Materialized views for expensive aggregations

---

## 📚 Documentation

### Available Resources

- **[Architecture Guide](docs/architecture.md)**: Detailed design decisions and patterns
- **[Business Questions](docs/business_questions.md)**: Analytics requirements and use cases
- **[Data Dictionary](docs/data_dictionary.md)**: Complete field-level documentation
- **[Implementation Plan](docs/implementation_plan.md)**: Step-by-step setup instructions
- **[Dashboard Mockups](docs/dashboard_mockups.md)**: BI visualization specifications

### dbt Documentation

Generate and view interactive documentation:

```bash
dbt docs generate
dbt docs serve
```

Access at `http://localhost:8080` to explore:
- Data lineage graphs
- Model descriptions
- Column-level documentation
- Test coverage reports

---

