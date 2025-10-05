#!/bin/bash
# CAEPA Deployment Script

echo "🚀 Deploying CAEPA..."

# Build and run with Docker Compose
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "✅ CAEPA deployed!"
echo "🌐 Frontend: http://localhost:8501"
echo "🔧 Backend: http://localhost:8001"

# Show logs
docker-compose logs -f