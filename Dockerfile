# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code to the container
COPY . .

# Expose the port
EXPOSE 9696

# Add labels to the Docker image
LABEL Name=thirdparty_service
LABEL Version=1.0

# Run the Flask application
CMD ["python", "Adfi.py"]