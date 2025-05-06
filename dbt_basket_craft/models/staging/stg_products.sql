WITH raw_products AS (
    SELECT *
    FROM {{ source('basket_craft', 'products') }}
),

stg_products AS (
    SELECT
        product_id,
        created_at,
        description AS product_description,
        product_name,
        CURRENT_TIMESTAMP AS loaded_at
    FROM raw_products
)

SELECT * FROM stg_products