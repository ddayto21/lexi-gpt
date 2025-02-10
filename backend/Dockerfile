# syntax=docker/dockerfile:1

# 1) Use a lightweight Python 3.10 base image
FROM python:3.10-slim AS base

# 2) Set environment variables to optimize pip behavior
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

# 3) Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# 4) Set the working directory inside the container
WORKDIR /code

# 5) Copy only dependency files first for Docker caching
COPY requirements.txt /code/requirements.txt

# 6) Install dependencies 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 7) Copy the rest of the application code
COPY ./app /code/app

# 8) Remove unnecessary local/dev files
RUN rm -rf /code/app/__pycache__ \
    && rm -rf /code/app/.pytest_cache \
    && rm -rf /code/app/.vscode \
    && rm -rf /code/app/.git

# 9) Expose port 8000 for FastAPI
EXPOSE 8000

# 10) Set the entrypoint to use the virtual environment & run FastAPI
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]