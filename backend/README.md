# Development Environment

This guide walks you through setting up the development environment for the project. Follow the steps below to install dependencies, start services, and run the backend locally.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing Dependencies](#installing-dependencies)
   - [Redis](#install-redis)
3. [Run Backend Application](#running-the-backend)

---

## Prerequisites

Ensure you have the following installed before proceeding:

- **[Poetry](https://python-poetry.org/)** – Dependency and package manager for Python.
- **[Redis](https://redis.io/)** – Caching server for session storage and fast lookups.
- **[Homebrew](https://brew.sh/)** (MacOS only) – Package manager for installing Redis.

---

## Installing Dependencies

### **Install Redis**

On macOS, install Redis using Homebrew:

```bash
brew install redis
```

### Start Redis Instance

Once installed, start the Redis server:

```bash
redis-server
```

To start the backend server, navigate to the `backend` directory and run:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend should now be running. You can test it by visiting:

```bash
http://localhost:8000/docs
```

This will open the Swagger UI, where you can interact with the API.

## Running Tests

```bash
poetry run pytest
```
