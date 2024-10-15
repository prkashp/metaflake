# MetaFlake

![Screenshot 2024-09-17 at 19-07-09 metaflake](https://github.com/user-attachments/assets/d8bb3029-ae41-4c7d-ae9c-201af6849706)


## Run Streamlit App locally:

Open terminal run local.sh
```bash
bash local.sh
```

## Access the Streamlit app:

Open your browser and go to http://localhost:8501

## TODOs
- Add table search option, it will be helpful in case of large catalog of tables
- Basic analytics on table, size source and owner
- Configuration Management: Consider using environment variables for sensitive information like Snowflake credentials. You can use Docker secrets or a .env file and python-dotenv for this purpose.
- Error Handling: Implement error handling in your connection and data processing scripts to manage any potential issues gracefully.
- Security: Ensure sensitive data such as passwords and connection details are secured appropriately.
