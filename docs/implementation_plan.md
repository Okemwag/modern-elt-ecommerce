# Implementation Plan

## Phase 1: Business Case

Deliverables:

- Scope statement
- Business questions
- KPI list

## Phase 2: Source Data

Deliverables:

- PostgreSQL transactional tables for customers, orders, order items, and payments
- CSV reference files for products, categories, and regions

## Phase 3: Airbyte

Deliverables:

- PostgreSQL source
- File source for CSV data
- Databricks destination
- Connections for transactional and reference data
- Screenshots of configured connectors and successful syncs

## Phase 4: Databricks

Deliverables:

- Catalog and schemas
- Bronze raw tables
- Validation notebooks
- Optional workflow job

## Phase 5: dbt

Deliverables:

- Staging models in silver
- Intermediate models for reusable business logic
- Gold dimensions, facts, and marts
- Generic and singular tests
- dbt docs

## Phase 6: Dashboard

Deliverables:

- Executive page
- Product performance page
- Customer insights page
- Regional performance page

## Phase 7: Portfolio Polish

Deliverables:

- Architecture diagram
- Data dictionary
- Dashboard screenshots
- README with setup instructions and project explanation
