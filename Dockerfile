# Start with a lightweight Python image
FROM python:3.12-slim

# Configure Python
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files into the container
COPY . .

# Document the port Flask uses
EXPOSE 8080

# Start the application
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 8 "app:create_app()"
