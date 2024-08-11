# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app/ app/

# Expose the port Streamlit will run on
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app/app.py"]
