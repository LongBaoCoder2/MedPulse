FROM python:3.11-slim

WORKDIR /app

# Cài đặt Poetry
RUN pip install poetry

# Sao chép các file cấu hình
COPY pyproject.toml poetry.lock ./
COPY .env .env

# Cài đặt dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Sao chép mã nguồn
COPY . .

# Expose port
EXPOSE 8000

# Chạy ứng dụng với Gunicorn
CMD ["poetry", "run", "gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"] 