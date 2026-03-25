# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt (with increased timeout for large ML libraries)
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/
COPY models/ ./models/

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
