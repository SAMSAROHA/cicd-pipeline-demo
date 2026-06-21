# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /install

# Copy requirements and install dependencies into /install using --prefix
COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim

LABEL maintainer="somil"
LABEL version="1.0.0"
LABEL description="Flask Task API CI/CD Demo"

# Install curl for HEALTHCHECK
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user "appuser"
RUN useradd -m appuser

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code (excluding tests directory)
COPY app/app.py /app/app.py

# Switch to non-root user
USER appuser

EXPOSE 5000

# Healthcheck running every 30s
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# Start the Flask app
CMD ["python", "app.py"]
