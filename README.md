# LexiGPT: AI-Powered Recommendation Chatbot

![Build Status](https://img.shields.io/github/actions/workflow/status/ddayto21/lexi-gpt/deploy-backend.yml?style=flat-square&color=2E8B57&labelColor=1E1E1E&logo=github-actions&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/ddayto21/lexi-gpt?style=flat-square&color=FF8C00&labelColor=1E1E1E&logo=git&logoColor=white)

**LexiGPT** is a **retrieval-augmented generation (RAG) chatbot** designed to provide **intelligent, personalized book recommendations**. It combines **semantic search** with **large language models (LLMs)** such as OpenAI and DeepSeek to process natural language queries. Built with **FastAPI** and a **React web interface**, LexiGPT enables **fast, accurate book discovery** through a conversational web interface.

## Core Features

![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square&logo=react&logoColor=white&color=dodgerblue&labelColor=gray)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white&color=dodgerblue&labelColor=gray)

- **LLM-Powered Responses**: Utilizes OpenAI and DeepSeek to generate intelligent book recommendations.
- **Semantic Search**: Employs vector embeddings to identify books based on contextual relevance rather than keywords.
- **Real-Time Streaming**: Delivers instantaneous, conversational book recommendations.
- **Multi-LLM Support**: Allows configuration of various language model providers.
- **REST API**: Built with FastAPI to ensure efficient and high-performance search capabilities.

---

## **RAG Pipeline**

![Open Library](https://img.shields.io/badge/Open%20Library-API-008080?style=flat-square&logo=librarything&logoColor=white&color=dodgerblue&labelColor=gray)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=000&color=dodgerblue&labelColor=white)](#)
![DeepSeek](https://img.shields.io/badge/DeepSeek-v3-FF4500?style=flat-square&logo=openai&logoColor=white&color=dodgerblue&labelColor=gray)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white&color=dodgerblue&labelColor=gray)

1. **Query Processing**: Transforms user queries into vector embeddings using a Sentence Transformer model.
2. **Semantic Search**: Matches query embeddings with precomputed book embeddings using cosine similarity.
3. **Ranking & Retrieval**: Fetches the top-k most relevant books based on similarity scores.
4. **LLM Enhancement**: Refines and elucidates retrieved books using a language model for enhanced recommendations.

---

[![Medium](https://img.shields.io/badge/Medium-000000?style=flat-square&logo=medium&logoColor=white&color=dodgerblue&labelColor=gray)](#)
![Docs](https://img.shields.io/badge/Docs-📖-dodgerblue?style=flat-square&color=dodgerblue&labelColor=gray)

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Tech Stack](#tech-stack)
   - [Frontend](#frontend)
   - [Backend](#backend)
4. [RAG System](#rag-system)
   - [Data Collection](#data-collection)
   - [Preprocessing](#preprocessing)
   - [Embedding Generation](#embedding-generation)
   - [LLM Integration](#llm-integration)
5. [Backend Deployment](#backend-deployment)
   - [Set Up IAM Credentials](#step-1-set-up-iam-credentials)
   - [Build and Push Docker Image to ECR](#step-2-build-and-push-docker-image-to-ecr)
   - [Deploy the Service to AWS ECS](#step-3-deploy-the-service-to-aws-ecs)
   - [Updating the ECS Service](#step-4-updating-the-ecs-service)
6. [Frontend Deployment](#frontend-deployment)

---

## Overview

LexiGPT allows users to **search for books using natural language descriptions**. It integrates with the **OpenLibrary Web Service** to fetch book data and uses **LLMs to refine and enhance search results**. The goal is to deliver **fast, relevant recommendations** with response times under **1-3 seconds**.

---

## Problem Statement

Finding the right book can be challenging when you don't have an exact title or author in mind. **LexiGPT** solves this by **interpreting natural language queries, identifying key details, and retrieving relevant book recommendations** in real-time.

---

## Tech Stack

LexiGPT follows a **client-server architecture** for **scalability and performance**.

### Frontend

- **Tech Stack**: React, Fetch API (for HTTP requests)
- **Core Features**:
  - **Conversational Search** → Supports flexible, natural language queries.
  - **Dynamic Recommendations** → Displays book titles, authors, and summaries based on user input.
  - **Responsive UI** → Optimized for desktop and mobile.

### Backend

- **Tech Stack**:
  - **FastAPI** → High-performance Python backend.
  - **LLM APIs** → Uses OpenAI, DeepSeek, and HF APIs for query processing.
  - **Docker** → Containerized for portability.
- **Core Features**:
  - **Query Understanding** → Extracts structured details (title, author, genre) from user input.
  - **Information Retrieval** → Fetches book metadata from OpenLibrary.
  - **AI-Enhanced Responses** → Summarizes and ranks recommendations using LLMs.
  - **Caching for Performance** → Stores frequent queries to reduce API calls and improve speed.

---

## Environment Variable Configuration Guide

These instructions outlines how `environment variables` are configured and managed across different `environments` for both the `frontend` and `backend` applications. Properly managing environment variables ensures security, scalability, and seamless deployments.

### 1. Development Environment

For local development, `environment variables` are stored in `.env` files. Each service (frontend/backend) loads the required variables from these files to simulate a real production environment.

#### Using .env.example as a Template

Before running the project for the first time, copy the `.env.example` template file to create a local `.env` file:

```bash
cp .env.example .env.development
```

This ensures all required environment variables are properly set.

#### Frontend Development (.env.development)

The React application uses `.env.development` to configure local API endpoints and settings.

```plaintext
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_ENV=development
```

We can use `process.env` to access these variables in the application:

```tsx
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
```

#### Backend Development (.env.development)

TThe FastAPI backend loads environment variables using `python-dotenv`.

For example, the `REDIS_PASSWORD` is loaded from the `.env.development` as such:

```python
from dotenv import load_dotenv
import os

load_dotenv(".env.development")

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
if not REDIS_PASSWORD:
    raise ValueError("Missing required environment variable: REDIS_PASSWORD")
```

- We add error handling to ensure the application falls gracefully if critical environment variables are missing.

### 1. CI/CD Environment

In CI/CD pipelines, environment variables are not stored in `.env` files. Instead, they are securely stored in `GitHub Secrets`.

#### Storing Environment Variables in GitHub Secrets

We can manage environment variables with secrets:

Secrets are managed in `GitHub Actions` → `Repository Settings` → `Secrets`.

Ensure the following secrets are set before running any CI/CD workflows:

```plaintext
REDIS_PASSWORD=supersecretpassword
JWT_SECRET_KEY=supersecurejwtkey
FRONTEND_ORIGIN=https://staging.yourdomain.com
```

#### Retrieving Environment Variables in GitHub Actions

`GitHub Actions` automatically injects `secrets` into workflows:

```yaml
env:
  REDIS_PASSWORD: ${{ secrets.REDIS_PASSWORD }}
  JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
```

### 3. Production Environment

In production, environment variables are securely stored in `AWS Secrets Manager` and injected into ECS `Task Definitions`.

#### Storing Secrets in AWS Secrets Manager

AWS allows us to store secrets as key-value pairs.

```bash
aws secretsmanager create-secret --name REDIS_PASSWORD --secret-string "productionsecret"
aws secretsmanager create-secret --name JWT_SECRET_KEY --secret-string "productionjwtsecret"
```

#### Injecting Secrets into AWS ECS Task Definitions

In `AWS ECS`, secrets are injected at runtime through `task definitions`.

```yaml
environment:
  - name: REDIS_PASSWORD
    valueFrom: arn:aws:secretsmanager:us-east-1:123456789012:secret:REDIS_PASSWORD
  - name: JWT_SECRET_KEY
    valueFrom: arn:aws:secretsmanager:us-east-1:123456789012:secret:JWT_SECRET_KEY
```

#### ECS Task Definition Example

Environment variables passed from AWS Secrets Manager to running containers using task definitions.

```json
{
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "backend-image:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "environment": [
        {
          "name": "FRONTEND_ORIGIN",
          "value": "https://yourdomain.com"
        }
      ],
      "secrets": [
        {
          "name": "REDIS_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:REDIS_PASSWORD"
        },
        {
          "name": "JWT_SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:JWT_SECRET_KEY"
        }
      ]
    }
  ]
}
```

1. `AWS ECS` reads `secrets` from `AWS Secrets Manager`.
2. The container loads `environment variables` from those `secrets`.
3. The backend can access these variables using `os.getenv()`.

### 4. Handling Missing Environment Variables

If a required environment variable is missing, the application is designed to fail gracefully with an error message.

#### Example: Error Handling in FastAPI

```python
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("Missing required environment variable: JWT_SECRET_KEY")
```

## Setup Development Environment

This guide walks you through the steps to set up both the frontend and backend development environments. Before you begin, ensure you have the following prerequisites installed:

- Node.js
- Yarn
- Docker Desktop

---

## Integration Tests

### Playwright

This guide will walk you through the process of setting up Playwright for integration testing in your CRA TypeScript project, targeting both your frontend and API server. We'll use **Yarn** for dependency management.

#### 1. Install Playwright and Its Dependencies

Add playwright as a development dependency:

```bash
yarn add --dev @playwright/test
```

#### Install browser binaries

This command downloads the necessary browser binaries (Chromium, Firefox, WebKit) required for testing.

```bash
npx playwright install
```

#### 2.Configure Playwright

Create a file named `playwright.config.ts` in the root of your project and add the following configuration:

```typescript
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests", // Directory where your tests will live
  timeout: 30000, // Global timeout for each test in milliseconds
  expect: {
    timeout: 5000, // Timeout for expect assertions
  },
  use: {
    // Set a base URL for your tests (adjust as needed)
    baseURL: "http://localhost:3000",
    // Capture screenshots on test failure
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "Chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "Firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "WebKit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
});
```

### Frontend Setup

The frontend application is built with React. Follow these steps to launch the development server:

#### 1. Navigate to the /frontend directory

Open your terminal and change your current directory to the `/frontend` directory:

```bash
cd frontend
```

#### 2. Run the development server

Run the following command to start the development server:

```bash
yarn run start
```

- This command launches the React development server.

- You should see logs indicating that the server is running, and the application will typically open in your default browser.

---

### Backend Setup

The backend is powered by `FastAPI` and uses `Redis` for caching/session management. `Docker Compose` is used to build and run the services.

#### 1. Navigate to the Backend Directory

Open your terminal and change your current directory to the `/backend` directory:

```bash
cd backend
```

#### 2. Spin Up the Backend Services

Run the following command to build and launch all the backend services:

```bash
docker compose up --build
```

This command performs the following:

What this command does:

- Builds Docker Images: It builds the Docker images for each service defined in the docker-compose.yml file using the respective Dockerfiles.
- Starts Containers: It launches the containers for:
  - API Service: Runs the FastAPI application, which depends on Redis for caching and session storage. The API is bound to 127.0.0.1 on port 8000 for local access.
  - Redis Service: Uses the lightweight redis:alpine image with a custom configuration file and a persistent volume (redis_data) for storing data. It also includes a health check to ensure Redis is running correctly.

---

## Getting Started

### 1. Setup Development Environment

We can set up our development environment by running:

```bash
docker compose up --build
```

This command will spin up the following services:

- Web Interface (React Application)
- REST API (Python)
- Caching Server (Redis)

### 2.Run Automated Tests in Docker

Then, run automated tests in docker with the command:

```bash
docker compose -f docker-compose.test.yml up --build
```

- This will run all our tests inside a controlled environment.

#### Monitor Container Logs

```bash
docker compose logs -f
```

---

## RAG System

The RAG system enhances LLM responses by incorporating external knowledge through a multi-step process:

### Data Collection

- **Objective:** Gather book metadata via OpenLibrary’s API.
- **Method:**
  1. **Extract Subjects:**
     ```python
     def extract_subjects(url="https://openlibrary.org/subjects") -> List[str]:
         # Code to parse HTML and extract subjects...
     ```
  2. **Collect Books per Subject:**
     ```python
     def fetch_books_by_subject(subject: str, limit=100) -> List[Dict[str, Any]]:
         # Code to query the API and structure metadata...
     ```
- **Output:** A JSON file containing subjects and book lists.

### Preprocessing

- **Objective:** Normalize and structure text for better semantic search.
- **Method:**
  - **Text Normalization:** Convert text to lowercase, remove special characters, tokenize, and lemmatize.
    ```python
    def normalize_text(text: str) -> str:
        # Code to clean and lemmatize text...
    ```
  - **Metadata Formatting:** Standardize titles, authors, and subjects.
- **Output:** Cleaned and structured data ready for embedding.

### Embedding Generation

- **Objective:** Transform textual metadata into vector embeddings for similarity searches.
- **Method:**
  1. **Format for Embedding:**

```python
def format_book_for_embedding(book: dict) -> str:
    return f"Title: {book.get('title', '')}. Author: {book.get('author', '')}. Subjects: {book.get('subjects', '')}. Year: {book.get('year', '')}."
```

2. **Create Embeddings:**

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode(["Example text for embedding"])
```

- **Output:** A JSON file containing vector embeddings for each book.

### LLM Integration

- **Objective:** Use LLMs to refine and enhance retrieved book data.
- **Method:**
  1. **Query Processing:** Transform user queries into embeddings.
  2. **Retrieve and Rank:** Use cosine similarity to identify top-k matching books.
  3. **Generate Enhanced Responses:** Leverage OpenAI or DeepSeek to produce detailed recommendations.
- **Output:** Final, enriched recommendations delivered to the user.

For more detailed insight, read the full [Medium article](#).

---

# Backend Deployment

This section walks through deploying the backend service on AWS using **IAM**, **ECR**, and **ECS**. The deployment process ensures a secure, scalable, and containerized environment for the application.

---

## Prerequisites

Before we begin, ensure you have:

- An **AWS account** with administrative access.
- The **AWS CLI** installed and configured.
- **Docker** installed on your local machine.
- Your backend service **containerized** using Docker.

---

## Step 1: Set Up IAM Credentials

### 1.1 Create an IAM User

1. Log in to your AWS account and navigate to the [AWS IAM Console](https://console.aws.amazon.com/iam/home).
2. In the left sidebar, click **Users** → **Create User**.
3. Provide a username (e.g., `backend-deploy-user`).
4. Select **Access Key - Programmatic Access**.

### 1.2 Assign IAM Policies

Attach the following policies to grant the necessary permissions:

- **AmazonEC2ContainerRegistryFullAccess** – Allows full access to Amazon ECR (push, pull, delete images).
- **AmazonECS_FullAccess** – Provides full permissions to create and manage ECS resources.
- **IAMFullAccess** – Enables role and permission management.
- **CloudWatchLogsFullAccess** – Allows access to CloudWatch for ECS logging.
- **AmazonS3ReadOnlyAccess** – Grants read-only access to S3, useful if storing static assets or configuration.
- **SecretsManagerReadWrite** - Grant permission to read secrets in AWS Secrets Manager.

### 1.3 Generate Access Keys

1. In the IAM user settings, navigate to **Security Credentials**.
2. Scroll to the **Access Keys** section and click **Create Access Key**.
3. Copy both the **Access Key ID** and **Secret Access Key**. Store these securely.

### 1.4 Configure AWS CLI with Credentials

1. Install AWS CLI by running the command in terminal:

```bash
brew install awscli
```

2. Run the following command and enter the IAM credentials when prompted:

```bash
aws configure
```

## Step 2: Build and Push Docker Image to ECR

### **2.1 Create an ECR Repository**

1. Open the [Amazon ECR Console](https://console.aws.amazon.com/ecr/home).
2. Click **Create Repository**.
3. Enter a repository name (e.g., `backend-service`).
4. Select **Private Repository**.
5. Click **Create** and note the repository URI.

### **2.2 Authenticate Docker with ECR**

To push Docker images to ECR, first authenticate your local Docker client:

```bash
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
```

Ensure you replace the following variables:

- `${AWS_REGION}` with the AWS region (e.g., `us-east-2`)
- `${AWS_ACCOUNT_ID}` with your AWS account ID.

### **2.3** Build the Docker Image

Once the Amazon ECR repository is set up, we need to build, tag, and push the Docker image. This ensures that the backend service is properly containerized and stored in AWS Elastic Container Registry (ECR) for deployment.

We will use `docker buildx` to build the image. This ensures compatibility with AWS Fargate, which runs on **linux/amd64** architecture.

```bash
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  -t ${ECR_REPOSITORY_NAME}:latest \
  --load .
```

- `--platform linux/amd64` → Ensures compatibility with AWS Fargate.
- `--provenance=false` → Disables provenance metadata, reducing build time.
- `-t ${ECR_REPOSITORY_NAME}:latest` → Tags the image locally as latest.
- `--load` → Loads the built image into the local Docker daemon.

### **2.4** Tag Image for ECR

Tagging is required so the image can be correctly referenced when pushing to ECR.

```bash
docker tag ${ECR_REPOSITORY_NAME}:latest \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest
```

- `${ECR_REPOSITORY_NAME}:latest` → The locally built image.
- `${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest` → The ECR repository where the image will be pushed.

### **2.4** Push Image to ECR

```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/${ECR_REPOSITORY_NAME}:latest
```

---

## **Step 3: Deploy the Service to AWS ECS**

Now that our Docker image is stored in **Amazon ECR**, we can deploy it to **Amazon ECS (Elastic Container Service)** using **Fargate**, AWS’s serverless container orchestration service.

---

### **3.1 Create an ECS Cluster**

1. Open the [ECS Console](https://console.aws.amazon.com/ecs/home).
2. In the left sidebar, click **Clusters** → **Create Cluster**.
3. Select **Fargate (serverless)**.
4. Configure the cluster settings as needed (default settings are fine for most cases).
5. Click **Create**.

---

### **3.2 Create a Task Definition**

A **task definition** tells ECS how to run a container, including CPU/memory limits, networking, and container settings.

1. Navigate to **Task Definitions** → **Create New Task Definition**.
2. Choose **Fargate** as the launch type and click **Next**.
3. Configure the container settings:
   - **Container Name**: `backend-service`
   - **Image URI**: Use the **ECR repository URI** from Step 2.
   - **Memory/CPU**: Choose an appropriate size (e.g., `512 MB / 0.25 vCPU`).
   - **Port Mappings**: Set **8000** (or the port your backend listens on).
4. Click **Create**.

---

### **3.3 Deploy the Service on ECS**

A **service** ensures that the task (container) runs continuously and handles scaling.

1. Navigate to **ECS Clusters** and select your cluster.
2. Click **Create Service**.
3. Configure the service:
   - **Launch Type**: `Fargate`
   - **Task Definition**: Select the one created in Step 3.2.
   - **Service Name**: `backend-service`
   - **Number of Tasks**: Set an appropriate number (`1` for testing, scale up for production).
4. Click **Deploy**.

---

### **3.4 Verify the Deployment**

1. Navigate to your **ECS Cluster** → **Services**.
2. Click on your running service and note the **Public IP** of the running task.
3. Test the deployment by sending a request:

```bash
  curl http://${PUBLIC_IP}:8080
```

If the service responds correctly, your backend is now successfully running on AWS ECS Fargate.

---

## Step 4: Updating the ECS Service

When changes are made to the backend service, the updated Docker container needs to be deployed to **Amazon ECS** to ensure the latest version of the application is running in the cluster. Below are the steps to build, tag, push, and deploy the updated container.

---

### **4.1 Build the Docker Image**

First, build the Docker image for the backend service. This step compiles the application into a container that can be deployed to ECS.

```bash
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  -t ${ECR_REPOSITORY_NAME}:latest \
  --load .
```

---

### **4.2 Tag the Docker Image**

After building the image, tag it with the full ECR repository URL. This step prepares the image to be pushed to the Amazon Elastic Container Registry (ECR).

```bash
docker tag ${ECR_REPOSITORY_NAME}:latest \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest
```

---

### **4.3 Push the Image to ECR**

```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/${ECR_REPOSITORY_NAME}:latest
```

---

### **4.4 Update ECS Service**

Finally, update the ECS service to use the newly pushed container image. This step triggers a new deployment, replacing the old containers with the updated version.

```bash
aws ecs update-service --cluster ${ECS_CLUSTER_NAME} --service ${ECS_SERVICE_NAME} --force-new-deployment --region ${AWS_REGION}
```

---

## Environment Configuration

### Set Environment Variables in AWS Secrets Manager

Run the following command to attach the `SecretsManagerReadWrite` AWS Managed Policy to your IAM user:

```bash
aws iam attach-user-policy \
  --user-name ${AWS_IAM_USER} \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

### Set Environment Variables in AWS Amplify

To set a single environment variable, run:

```bash
aws amplify update-app \
    --app-id ${AWS_AMPLIFY_APP_ID} \
    --environment-variables ${ENV_NAME}=`${VALUE}`
```

We can also load multiple variables by creating an `env.json` file:

```json
{
  "REDIS_PASSWORD": "your-secure-password",
  "FRONTEND_ORIGIN": "https://yourdomain.com",
  "API_KEY": "12345abcdef"
}
```

---

## Frontend Deployment

This section outlines the steps required to deploy the frontend of the **Book Search Application** using **AWS Amplify**. AWS Amplify automates the deployment process, integrating directly with GitHub for continuous deployment. By following these steps, you can ensure a smooth and efficient deployment process.

---

## Prerequisites

Before starting the deployment process, ensure the following steps are completed:

1. **AWS Account**: You need an AWS account with the necessary permissions to create and manage Amplify applications.
2. **GitHub Repository**: The frontend code should be hosted in a GitHub repository.
3. **Node.js and Yarn**: Ensure Node.js and Yarn are installed on your local machine.

---

## Step 1: Build the Application

### 1.1 Run linting tool

Run the linting tool to ensure the code adheres to the project's coding standards:

```bash
yarn run lint
```

### 1.2 Create Production Build

Generate an optimized production build of the application:

```bash
yarn run build
```

This command compiles the React application into a set of static files that can be served by a web server.

## Step 2: Configure AWS Amplify

### 2.1: Navigate to the AWS Amplify Console

1. Go to the AWS Amplify Console.
2. Sign in with your AWS credentials.

### 2.2: Create a New Application

1. Click the "Create New Application" button to start the process.
2. Select GitHub as the source code provider.

### 2.3: Connect the Repository

- Choose the name of the repository from your GitHub account.
- Select the `main` branch for deployment.

### 2.4: Configure the Monorepo

Since the frontend application is part of a monorepo, specify the root directory:

- Set the root directory to `frontend` to ensure Amplify knows where to find the source code.

## Step 3: Deploy the Application

- Click the "Next" button to proceed.
- AWS Amplify will automatically build and deploy the application to the cloud.

Once the deployment is complete, the application will be accessible at the provided Amplify URL.

---
