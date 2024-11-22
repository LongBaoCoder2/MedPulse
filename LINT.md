# Format code
black qllm tests

# Check import order
isort --check-only qllm tests

# Lint with Flake8
flake8 qllm tests

# Type-check with Mypy
mypy qllm
