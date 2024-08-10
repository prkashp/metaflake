import streamlit as st
import pandas as pd
from snowflake_connector import fetch_data
from data_processor import preprocess_data

# SQL query path
PATH = './sql/account_usage_table.sql'

def get_query(file):
    file_dir = open(file, 'r')
    sql_query = file_dir.read()
    file_dir.close()
    return sql_query

def main():
    st.title("Snowflake Data Summary")

    # Fetch data from Snowflake
    data = fetch_data(get_query(PATH))

    # Preprocess data
    processed_data = preprocess_data(data)

    # Display data using Streamlit
    st.write("Raw Data", data)
    st.write("Processed Data", processed_data)

if __name__ == "__main__":
    main()
