# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11.0-slim

# Set environment variables to ensure the app runs correctly
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (only if you need some libraries for other parts of the app)
RUN apt-get update \
    && apt-get install -y libpq-dev gcc

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django application code into the container
COPY . /app/

# Copy the pod.env file into the container
COPY pod.env /app/pod.env

# Expose the default port (8000) for Gunicorn
EXPOSE 8000