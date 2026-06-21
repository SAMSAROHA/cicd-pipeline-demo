#!/bin/bash

# Exit on any error
set -e

echo "Building and starting local Docker environment..."
docker-compose up --build -d

echo ""
echo "======================================================="
echo "Application is starting in the background!"
echo "API is accessible at: http://localhost:5000"
echo "Healthcheck: http://localhost:5000/health"
echo "======================================================="
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop the application, run: docker-compose down"
