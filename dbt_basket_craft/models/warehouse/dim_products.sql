WITH stg_products AS (
    SELECT *
    FROM {{ ref('stg_products') }}
)

SELECT
    product_id,
    product_name,
    product_description,
    created_at
FROM stg_products