# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt .

COPY . .

# Install the dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Set environment variables from the .env file

# Copy the rest of the application code into the container
# Expose the port that the app will run on
EXPOSE 8081

# Command to run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]