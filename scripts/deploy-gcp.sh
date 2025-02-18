#!/bin/bash

# Các biến môi trường GCP (cần điền)
PROJECT_ID="your-project-id"
REGION="asia-southeast1"
REPOSITORY="qllm"

# Đăng nhập vào Google Cloud
gcloud auth configure-docker asia-southeast1-docker.pkg.dev

# Tạo Artifact Registry repository
gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION \
    --project=$PROJECT_ID

# Build và push Docker image
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/api:latest .
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/api:latest

# Tạo file docker-compose cho production
cat > docker-compose.prod.yml << EOL
version: '3.9'
name: qllm

services:
  api:
    image: ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/api:latest
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://[CLOUD_SQL_USERNAME]:[CLOUD_SQL_PASSWORD]@[CLOUD_SQL_IP]:5432/qllm
      - QDRANT_HOST=localhost
      - QDRANT_PORT=6333
    
  qdrant:
    image: qdrant/qdrant:latest
    restart: always
    ports:
      - 6333:6333
      - 6334:6334
    environment:
      - RUN_MODE=production
    volumes:
      - ./qdrant_storage:/qdrant/storage
      - ./qdrant-dev.config.yaml:/qdrant/config/production.yaml
EOL

# Tạo Cloud Run service
gcloud run deploy qllm \
    --image=$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/api:latest \
    --platform=managed \
    --region=$REGION \
    --allow-unauthenticated

echo "Script triển khai GCP đã hoàn tất!"
echo "Tiếp theo, bạn cần:"
echo "1. Tạo Cloud SQL instance cho PostgreSQL"
echo "2. Cập nhật biến môi trường DATABASE_URL trong Cloud Run service"
echo "3. Cấu hình VPC connector nếu cần kết nối private với Cloud SQL" 