# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY . .

EXPOSE 8080

# Run the Python script when the container launches
CMD ["uvicorn",:"main:app","--host","0.0.0.0","--port","8080"]