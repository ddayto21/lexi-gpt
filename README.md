# 📖 LexiGPT: AI-Powered Recommendation Chatbot

![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)
![React](https://img.shields.io/badge/react-18.2.0-blue?logo=react)
![DeepSeek](https://img.shields.io/badge/deepseek-v3-blue?logo=openai)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green?logo=openai)

![Docs](https://img.shields.io/badge/docs-%F0%9F%93%96-blue)
![Community](https://img.shields.io/badge/community-%F0%9F%92%AC-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**LexiGPT** is a **retrieval-augmented generation (RAG) chatbot** designed to provide **intelligent, personalized book recommendations**. It combines **semantic search** with **large language models (LLMs)** such as OpenAI and DeepSeek to process natural language queries. Built with **FastAPI** and a **React web interface**, LexiGPT enables **fast, accurate book discovery** through a conversational web interface.

## **🚀 Features**

- **LLM-Powered Responses** → Uses OpenAI/DeepSeek to process book-related queries.
- **Semantic Search with Vector Embeddings** → Finds books based on meaning, not just keywords.
- **Real-Time Streaming** → Fast, chatbot-style recommendations.
- **Multi-LLM Support** → Users can configure different language model providers.
- **Highly Scalable API** → Built with **FastAPI** for high-performance search.

---

## **🧠 How the RAG Pipeline Works**

1. **Query Processing**: A user's natural language query is **vectorized** using a **Sentence Transformer model**.
2. **Semantic Search**: Precomputed **book embeddings** are compared using **cosine similarity**.
3. **Ranking & Retrieval**: The **top-k most relevant books** are retrieved based on similarity scores.
4. **LLM Enhancement**: The retrieved books are **re-ranked and explained** using a **language model**.

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Tech Stack](#tech-stack)
   - [Frontend](#frontend)
   - [Backend](#backend)
4. [Backend Deployment](#backend-deployment)
   - [Set Up IAM Credentials](#step-1-set-up-iam-credentials)
   - [Build and Push Docker Image to ECR](#step-2-build-and-push-docker-image-to-ecr)
   - [Deploy the Service to AWS ECS](#step-3-deploy-the-service-to-aws-ecs)
   - [Updating the ECS Service](#step-4-updating-the-ecs-service)
5. [Frontend Deployment](#frontend-deployment)
   - [Build the Application](#step-1-build-the-application)
   - [Configure AWS Amplify](#step-2-configure-aws-amplify)
   - [Deploy the Application](#step-3-deploy-the-application)

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

# Frontend Deployment

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
