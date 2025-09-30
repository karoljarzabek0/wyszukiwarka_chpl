FROM python:3.12-slim
# Install system dependencies needed for some Python packages
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     libxml2-dev \
#     libxslt1-dev \
#     git \
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install flask flask-cors python-dotenv sentence-transformers psycopg2-binary gunicorn
#RUN pip install --no-cache-dir -r requirements.txt


# Copy your application code
COPY . .

# Expose port for Flask / Gunicorn
EXPOSE 8000

# Start the app with Gunicorn
CMD ["gunicorn", "web_app.app:app", "-w", "1", "-b", "0.0.0.0:8000"]
