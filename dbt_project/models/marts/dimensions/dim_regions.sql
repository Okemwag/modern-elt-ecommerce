select
    region_id,
    region_name,
    country
from {{ ref('stg_regions') }}
