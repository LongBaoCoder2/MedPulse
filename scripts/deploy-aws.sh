#!/bin/bash

# Các biến môi trường AWS (cần điền)
AWS_ACCOUNT_ID="your-account-id"
AWS_REGION="ap-southeast-1"
ECR_REPOSITORY="qllm"

# Login vào AWS ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tạo repository trên ECR nếu chưa tồn tại
aws ecr create-repository --repository-name $ECR_REPOSITORY --region $AWS_REGION || true

# Build và push Docker image
docker build -t $ECR_REPOSITORY .
docker tag $ECR_REPOSITORY:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest

# Tạo file docker-compose cho production
cat > docker-compose.prod.yml << EOL
version: '3.9'
name: qllm

services:
  api:
    image: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://[RDS_USERNAME]:[RDS_PASSWORD]@[RDS_ENDPOINT]:5432/qllm
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

echo "Script triển khai AWS đã hoàn tất!"
echo "Tiếp theo, bạn cần:"
echo "1. Cập nhật thông tin DATABASE_URL trong docker-compose.prod.yml với thông tin RDS"
echo "2. Triển khai lên EC2 instance bằng cách chạy: docker-compose -f docker-compose.prod.yml up -d" 