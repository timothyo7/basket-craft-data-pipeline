WITH raw_website_sessions AS (
    SELECT *
    FROM {{ source('basket_craft', 'website_sessions') }}
),

stg_website_sessions AS (
    SELECT
        website_session_id,
        created_at AS website_session_created_at,
        utm_source,
        is_repeat_session,
        CURRENT_TIMESTAMP AS loaded_at
    FROM raw_website_sessions
)

SELECT * FROM stg_website_sessions