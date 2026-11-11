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
EXPOSE 5000

# Start the Flask application
CMD ["flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=5000"]
