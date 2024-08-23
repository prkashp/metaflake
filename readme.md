# MetaFlake

## Build the Docker image:

```bash
docker build . -t metaflake/py-docker
```

## Run the Docker container:

```bash
docker run -p 8501:8501 metaflake/py-docker
```

## Access the Streamlit app:

Open your browser and go to http://localhost:8501

## TODOs
- Add table search option, it will be helpful in case of large catalog of tables
- Basic analytics on table, size source and owner
- Configuration Management: Consider using environment variables for sensitive information like Snowflake credentials. You can use Docker secrets or a .env file and python-dotenv for this purpose.
- Error Handling: Implement error handling in your connection and data processing scripts to manage any potential issues gracefully.
- Security: Ensure sensitive data such as passwords and connection details are secured appropriately.
