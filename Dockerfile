# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the tokenizer and model files into the container
COPY tokenizer.pkl .
COPY model.h5 .

# Copy the Python script into the container
COPY main.py .

# Run the Python script when the container launches
ENTRYPOINT ["python", "main.py"]