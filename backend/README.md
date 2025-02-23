# Development Environment

This guide walks you through setting up the development environment for the project. Follow the steps below to install dependencies, start services, and run the backend locally.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing Dependencies](#installing-dependencies)
   - [Redis](#install-redis)
3. [Run Development Server](#start-development-server)

---

## Build Docker Image

```bash
docker build -t book-search-dev:latest .
```

## Run Docker Container

```bash
docker run --name dev-container -p 8000:8000  book-search-dev
```

## Prerequisites

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

## Start Development Server

To start the backend server, navigate to the `backend` directory and run:

```bash
fastapi dev app/main.py
```

The backend should now be running. You can test it by visiting:

```bash
http://localhost:8000/docs
```

## OAuth FLow

- Create new project in google cloud platform
- Enable Google+ APi
- Create OAuth Client ID
- Web Application
- Set callback url ('/auth/callback')
