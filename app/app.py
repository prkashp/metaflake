import streamlit as st
import pandas as pd
from snowflake_connector import fetch_data
from data_processor import preprocess_data

# Define your SQL query
SQL_QUERY = "SELECT * FROM your_table LIMIT 100"

def main():
    st.title("Snowflake Data Summary")

    # Fetch data from Snowflake
    data = fetch_data(SQL_QUERY)

    # Preprocess data
    processed_data = preprocess_data(data)

    # Display data using Streamlit
    st.write("Raw Data", data)
    st.write("Processed Data", processed_data)

if __name__ == "__main__":
    main()
