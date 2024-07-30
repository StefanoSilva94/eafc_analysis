# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY backend/requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container
COPY backend/ .

# Expose the port your backend runs on
EXPOSE 8000

# Command to run your backend (e.g., with Gunicorn)
CMD ["uvicorn", "app.main:app", "/--host", "--port", "8000"]
