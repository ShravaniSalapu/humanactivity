# Use official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory contents into the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000



# Run the Flask app
CMD ["python", "app.py"]
