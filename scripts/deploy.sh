#!/bin/bash

# Dừng và xóa các container cũ nếu có
docker-compose down

# Build lại images
docker-compose build

# Khởi động các services
docker-compose up -d

# Chạy migrations
docker-compose exec api poetry run alembic upgrade head

echo "Ứng dụng đã được triển khai thành công!"
echo "API có thể truy cập tại: http://localhost:8000"
echo "Qdrant UI có thể truy cập tại: http://localhost:6333" 