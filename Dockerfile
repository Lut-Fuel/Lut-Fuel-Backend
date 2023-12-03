# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local "src" directory into the container's /app/src directory.
COPY src/ /app/

# Copy the requirements.txt file from the local directory into the container's /app directory.
COPY requirements.txt /app/

# Install production dependencies.
RUN pip install --no-cache-dir -r /app/requirements.txt

# Specify the command to run your Python server.
CMD uvicorn app:app --port $PORT --host 0.0.0.0
