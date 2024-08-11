import os
import snowflake.connector
import pandas as pd

PATH = 'app/sql/account_usage_tables.sql'


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

def get_query(file) -> str:
    try:
        with open(file) as f:
            sql_query = f.read()
    except:
        raise Exception('query file not found',file,os.getcwd(), os.listdir())
    return sql_query

def fetch_data() -> pd.DataFrame:
    query = get_query(PATH)
    conn = get_snowflake_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
