# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the server will run on
EXPOSE 5000

# Run the server
CMD ["python", "server.py"]

# Test stage
FROM base AS test

CMD ["python", "-m", "unittest", "discover"]

