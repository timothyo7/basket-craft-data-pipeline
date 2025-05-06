WITH stg_orders AS (
    SELECT *
    FROM {{ ref('stg_orders') }}
)

SELECT
    DATE(order_created_at) AS order_day,
    COUNT(order_id) AS total_orders
FROM stg_orders
GROUP BY DATE(order_created_at)