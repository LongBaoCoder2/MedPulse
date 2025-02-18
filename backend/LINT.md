# Format code
black qllm example tests

# Check import order
isort --check-only qllm example tests

# Fix import order
isort qllm example tests

# Lint with Flake8
flake8 qllm example tests

# Type-check with Mypy
mypy qllm example
