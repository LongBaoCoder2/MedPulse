# Hướng dẫn Triển khai QLLM

## 1. Triển khai trên AWS

### Yêu cầu
- Tài khoản AWS với quyền truy cập EC2, RDS, và ECR
- AWS CLI đã được cài đặt và cấu hình
- Docker và Docker Compose

### Các bước triển khai

1. Chuẩn bị môi trường AWS:
   - Tạo VPC và Security Groups
   - Tạo RDS instance cho PostgreSQL
   - Tạo EC2 instance (Ubuntu 22.04 LTS)

2. Cập nhật thông tin trong `deploy-aws.sh`:
   ```bash
   AWS_ACCOUNT_ID="your-account-id"
   AWS_REGION="ap-southeast-1"
   ```

3. Chạy script triển khai:
   ```bash
   chmod +x deploy-aws.sh
   ./deploy-aws.sh
   ```

4. SSH vào EC2 instance và cài đặt Docker:
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   ```

5. Copy các file cần thiết lên EC2:
   ```bash
   scp -i your-key.pem docker-compose.prod.yml ubuntu@your-ec2-ip:~/
   scp -i your-key.pem .env ubuntu@your-ec2-ip:~/
   ```

6. Chạy ứng dụng trên EC2:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 2. Triển khai trên Google Cloud Platform

### Yêu cầu
- Tài khoản GCP với dự án đã được tạo
- Google Cloud SDK đã được cài đặt
- Docker và Docker Compose

### Các bước triển khai

1. Chuẩn bị môi trường GCP:
   - Kích hoạt các API cần thiết (Cloud Run, Cloud SQL, Artifact Registry)
   - Tạo Cloud SQL instance cho PostgreSQL
   - Cấu hình VPC và firewall rules

2. Cập nhật thông tin trong `deploy-gcp.sh`:
   ```bash
   PROJECT_ID="your-project-id"
   REGION="asia-southeast1"
   ```

3. Chạy script triển khai:
   ```bash
   chmod +x deploy-gcp.sh
   ./deploy-gcp.sh
   ```

4. Cấu hình Cloud Run:
   - Thêm các biến môi trường
   - Cấu hình VPC connector nếu cần
   - Cấu hình domain tùy chỉnh (nếu có)

## Các lưu ý quan trọng

### Bảo mật
1. Sử dụng secrets management:
   - AWS Secrets Manager
   - Google Secret Manager
2. Cấu hình SSL/TLS
3. Thiết lập firewall và security groups
4. Sử dụng IAM roles với least privilege

### Monitoring
1. Cấu hình logging:
   - CloudWatch (AWS)
   - Cloud Logging (GCP)
2. Thiết lập alerts
3. Monitoring metrics:
   - CPU/Memory usage
   - Request latency
   - Error rates

### Backup
1. Cấu hình backup tự động cho database
2. Backup Qdrant storage
3. Lưu trữ Docker images với version tags

### Scaling
1. Cấu hình auto-scaling:
   - EC2 Auto Scaling Groups (AWS)
   - Cloud Run auto-scaling (GCP)
2. Database scaling
3. Load balancing

## Khắc phục sự cố

### Logs
- API logs: `docker logs qllm_api_1`
- Database logs: Xem trong RDS/Cloud SQL console
- Qdrant logs: `docker logs qllm_qdrant_1`

### Common Issues
1. Database connection errors:
   - Kiểm tra security groups/firewall rules
   - Verify connection string
2. Docker issues:
   - Check disk space
   - Verify Docker daemon status
3. Memory/CPU issues:
   - Monitor resource usage
   - Adjust instance size if needed 