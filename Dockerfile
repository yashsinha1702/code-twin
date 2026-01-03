# Use a lightweight Python Linux image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install pytest inside the container
RUN pip install pytest

# We don't copy files yet; we will do that dynamically in the executor