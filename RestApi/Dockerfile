# Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py
CMD ["python", "app.py"]
