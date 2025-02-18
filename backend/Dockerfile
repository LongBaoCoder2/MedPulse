# Use a slim Python image for smaller size
FROM python:3.11.3-slim-bullseye

# Set environment variables for non-buffered output and working directory
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Install system dependencies in one step
RUN apt-get update --no-cache && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
        build-essential \
        wkhtmltopdf && \
    rm -rf /var/lib/apt/lists/*  # Clean up APT cache

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["poetry", "run", "start"]