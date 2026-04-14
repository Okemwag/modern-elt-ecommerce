use catalog ecommerce;

create schema if not exists bronze
comment 'Raw Airbyte-loaded data';

create schema if not exists silver
comment 'Cleaned and standardized dbt staging models';

create schema if not exists gold
comment 'Business-ready dimensions, facts, and marts';
