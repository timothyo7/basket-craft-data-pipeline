"""
1. Import necessary libraries
2. Load source MySQL and destination Postgres connection details.
3. Build connection strings and create database engines.
4. Read products table from MySQL and load into a DataFrame.
5. Write DataFrame to products table in Postgres. (raw schema)
"""
# %%
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# %%
# Load environment variables from .env file
load_dotenv()

# %%
# MySQL database connection details
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_host = os.environ['MYSQL_HOST']
mysql_db = os.environ['MYSQL_DB']

# Postgres database connection details
pg_user = os.environ['PG_USER']
pg_password = os.environ['PG_PASSWORD']
pg_host = os.environ['PG_HOST']
pg_db = os.environ['PG_DB']

pg_db

# %%
# Build connection strings
mysql_conn_str = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
pg_conn_str = f'postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}/{pg_db}'


# %%
# Create database engines
mysql_engine = create_engine(mysql_conn_str)
pg_engine = create_engine(pg_conn_str)

# %%
# Read products table from MySQL
df = pd.read_sql('SELECT * FROM products', mysql_engine)
# %%
# Create raw schema if it doesn't exist
with pg_engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    connection.commit()

# Check if table exists and truncate it, or create it if it doesn't
with pg_engine.connect() as connection:
    result = connection.execute(text(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'raw' AND table_name = 'products')"
    ))
    table_exists = result.scalar()
    
    if table_exists:
        # Truncate the table instead of dropping it
        connection.execute(text("TRUNCATE TABLE raw.products"))
        connection.commit()
        # Write data without dropping table
        df.to_sql('products', pg_engine, schema='raw', if_exists='append', index=False)
    else:
        # Create new table
        df.to_sql('products', pg_engine, schema='raw', if_exists='replace', index=False)

# %%
print(f'{len(df)} records loaded into Postgres products table.')