# Use official Python slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.0.1

# Install system dependencies and Poetry, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get remove -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (leveraging Docker layer caching)
COPY pyproject.toml poetry.lock README.md ./

# Install dependencies (only main)
RUN /root/.local/bin/poetry install --with dev --no-interaction --no-ansi

# Copy application code
COPY . .

RUN rm -rf .env .env.tests node_modules .pytest_cache .mypy_cache .ruff_cache __pycache__


# Expose application port
EXPOSE 8000

# Run FastAPI server
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]