# messaging_app/Dockerfile
FROM python:3.10-slim

# Prevent Python from writing pyc files and buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building MySQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first (better for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project code into /app
COPY . .

# Move manage.py to root if it exists inside a subfolder (safety net for Jenkins)
RUN if [ -f messaging_app/manage.py ]; then mv messaging_app/manage.py ./; fi

# Create and use a non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the Django port
EXPOSE 8000

# Default command: run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
