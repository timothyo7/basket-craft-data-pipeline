WITH stg_products AS (
   SELECT * FROM {{ ref('stg_products') }}
),
dim_products AS (
   SELECT
       product_id,
       product_name,
       product_description,
       created_at,
       CURRENT_TIMESTAMP AS dbt_updated_at
   FROM stg_products
)
SELECT * FROM dim_products