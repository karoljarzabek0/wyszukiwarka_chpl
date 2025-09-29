# Stage 1: Build Python dependencies (wheels)
FROM python:3.12-slim AS builder

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip & wheel
RUN pip install --upgrade pip wheel setuptools

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# Stage 2: Runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy pre-built wheels and install
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels

# Copy your application code
COPY . .

# Expose port for Flask / Gunicorn
EXPOSE 8000

# Start the app with Gunicorn
CMD ["gunicorn", "web_app.app:app", "-w", "4", "-b", "0.0.0.0:8000"]
