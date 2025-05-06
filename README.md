This project repository implements an end-to-end data pipeline for Basket Craft's e-commerce analytics. The pipeline extracts data from a MySQL source database (products, orders, and website sessions), loads it into a PostgreSQL raw schema, and transforms it through a modular dbt workflow with staging and warehouse layers. The architecture follows modern ELT principles, enabling separate storage and compute while maintaining data lineage. Using Python and SQLAlchemy for extraction, dbt for transformation, and GitHub Actions for automation, the pipeline runs every 15 minutes to ensure fresh data availability. The warehouse layer produces fact tables including website session metrics by UTM source, enabling stakeholders to analyze traffic patterns, repeat visit rates, and marketing channel effectiveness through interactive Looker Studio dashboards with cross-filtering capabilities.

graph LR
    %% STYLES
    classDef mysql fill:#00758F,color:white,stroke:#000000
    classDef python fill:#306998,color:white,stroke:#000000
    classDef postgres fill:#336791,color:white,stroke:#000000
    classDef dbt fill:#FF694B,color:white,stroke:#000000
    classDef looker fill:#4285F4,color:white,stroke:#000000
    classDef aws fill:#FF9900,color:white,stroke:#000000
    classDef github fill:#181717,color:white,stroke:#000000

    %% SOURCE LAYER
    subgraph mysqldb["MySQL Database (Source)"]
        products["products table"]
        orders["orders table"]
        sessions["website_sessions table"]
    end
    
    %% ETL LAYER
    subgraph etl["Python ETL Scripts (GitHub Actions)"]
        products_etl["basket_craft_products_extract_load_raw.py"]
        orders_etl["basket_craft_orders_extract_load_raw.py"]
        sessions_etl["basket_craft_website_sessions_extract_load_raw.py"]
    end
    
    %% RAW LAYER
    subgraph raw["PostgreSQL Database (raw schema)"]
        raw_products["raw.products"]
        raw_orders["raw.orders"]
        raw_sessions["raw.website_sessions"]
    end
    
    %% STAGING LAYER
    subgraph staging["dbt Transformations (staging schema)"]
        stg_products["stg_products (view)"]
        stg_orders["stg_orders (view)"]
        stg_sessions["stg_website_sessions (view)"]
    end
    
    %% WAREHOUSE LAYER
    subgraph warehouse["dbt Transformations (warehouse schema)"]
        dim_products["dim_products (table)"]
        fct_orders["fct_orders_product_daily (table)"]
        fct_sessions["fct_website_sessions_utm_source_daily (table)"]
    end
    
    %% VISUALIZATION LAYER
    subgraph viz["Looker Studio Dashboard"]
        viz1["Sessions Table"]
        viz2["UTM Source Heatmap"]
        viz3["Sessions Scorecard w/ Comparison"]
        viz4["Daily Sessions Time Series"]
        viz5["UTM Source Bar Chart"]
    end
    
    %% CONNECTIONS
    products --> products_etl
    orders --> orders_etl
    sessions --> sessions_etl
    
    products_etl --> raw_products
    orders_etl --> raw_orders
    sessions_etl --> raw_sessions
    
    raw_products --> stg_products
    raw_orders --> stg_orders
    raw_sessions --> stg_sessions
    
    stg_products --> dim_products
    stg_orders --> fct_orders
    stg_sessions --> fct_sessions
    
    fct_sessions --> viz1
    fct_sessions --> viz2
    fct_sessions --> viz3
    fct_sessions --> viz4
    fct_sessions --> viz5
    
    %% TECH STACK LABELS
    tech1["AWS RDS MySQL"]:::aws
    tech2["Python, Pandas, SQLAlchemy"]:::python
    tech3["GitHub Actions"]:::github
    tech4["AWS RDS PostgreSQL"]:::postgres
    tech5["dbt Core"]:::dbt
    tech6["Looker Studio"]:::looker
    
    %% APPLY STYLES
    mysqldb:::mysql
    etl:::python
    raw:::postgres
    staging:::dbt
    warehouse:::dbt
    viz:::looker


Dashboard: [https://lookerstudio.google.com/reporting/43a4bf11-e3db-4f40-94e1-3a86c7f97bb1](https://lookerstudio.google.com/reporting/43a4bf11-e3db-4f40-94e1-3a86c7f97bb1)
link: https://lookerstudio.google.com/reporting/43a4bf11-e3db-4f40-94e1-3a86c7f97bb1