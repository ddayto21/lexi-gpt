# syntax=docker/dockerfile:1

############################
# 1) Base Stage
############################
FROM python:3.10-slim AS base

# Common environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install any system packages both builder and runtime layers need
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

############################
# 2) Builder Stage
############################
FROM base AS builder

# Additional environment variables just for building
ENV POETRY_VERSION=2.0.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    # Put your venv directly in /app/.venv
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

# We can optionally use a build arg to install dev deps if needed.
ARG DEV=false

# Install build dependencies for compiling packages (C libraries, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    gcc \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy only dependency files first for layer caching
COPY pyproject.toml poetry.lock ./

# Install dependencies:
# If DEV=true, install dev extras; else omit them.
RUN if [ "$DEV" = "true" ] ; then \
      poetry install --with dev --no-root ; \
    else \
      poetry install --without dev --no-root ; \
    fi && rm -rf $POETRY_CACHE_DIR

# Copy the rest of your application code
COPY . .

# Remove local dev/test artifacts if you want a clean builder
RUN rm -rf \
    .env .env.tests node_modules \
    .pytest_cache .mypy_cache .ruff_cache __pycache__ \
    tests

############################
# 3) Runtime Stage
############################
FROM base AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy Poetry + everything from /root/.local where it was installed
COPY --from=builder /root/.local /root/.local

# Optionally re-link if needed:
RUN ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Then copy the entire /app folder from builder
COPY --from=builder /app /app

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]