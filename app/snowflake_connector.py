import snowflake.connector
import pandas as pd

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT',
        warehouse='YOUR_WAREHOUSE',
        database='YOUR_DATABASE',
        schema='YOUR_SCHEMA'
    )
    return conn

def fetch_data(query: str) -> pd.DataFrame:
    conn = get_snowflake_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
