FROM python:3.10-slim

# Install system dependencies (Tesseract OCR, language packs, and libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ind \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure uploads directory exists
RUN mkdir -p uploads

# Dynamic port binding (Render, Railway, Fly.io, etc. inject $PORT)
ENV PORT=5000
EXPOSE 5000

# Run production server using Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 app:app"]
