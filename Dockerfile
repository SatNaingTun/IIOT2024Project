# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY IIOTWeb/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY IIOTWeb /app/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8024"]
