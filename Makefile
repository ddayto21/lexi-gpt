# -----------------------------------------------
# Makefile: Full Automation for Dev, Docker, and AWS Deployment
# -----------------------------------------------

# ✅ Load environment variables from .env
include backend/.env
export $(shell sed 's/=.*//' backend/.env)

# Colors for better readability
RESET=\033[0m
BLUE=\033[1;34m
GREEN=\033[1;32m
YELLOW=\033[1;33m
RED=\033[1;31m


# ✅ Required environment variables
REQUIRED_ENV_VARS = REDIS_PASSWORD FRONTEND_ORIGIN JWT_SECRET_KEY

.PHONY: setup check-env docker-start deploy update-lambda deploy-lambda

# -----------------------------------------------
# 🚀 Step 1: Load and Validate Environment Variables
# -----------------------------------------------

setup:
	@echo "🚀 Loading environment variables from backend/.env..."
	@if [ ! -f backend/.env ]; then \
		echo "❌ Error: backend/.env file not found. Please create it or copy from .env.example."; \
		exit 1; \
	fi
	@export $(grep -v '^#' backend/.env | xargs)  # ✅ Ensures variables persist

check-env: setup
	@echo "🔍 Checking required environment variables..."
	@for var in $(REQUIRED_ENV_VARS); do \
		if [ -z "$$(printenv $$var)" ]; then \
			echo "❌ Error: Missing $$var in backend/.env. Ensure all required variables are set."; \
			exit 1; \
		fi \
	done
	@echo "✅ All required environment variables are set."

# -----------------------------------------------
# 🐳 Step 2: Start Docker Containers
# -----------------------------------------------
docker-start: check-env
	@echo "🐳 Checking if Docker is running..."
	@if ! docker info > /dev/null 2>&1; then \
		echo "❌ Error: Docker is not running. Please start Docker and try again."; \
		exit 1; \
	fi
	@echo "🚀 Starting Docker Compose..."
	docker compose up --build

# -----------------------------------------------
# 🚀 Step 3: Build and Deploy Backend to AWS
# -----------------------------------------------

# ✅ Define AWS image URI
IMAGE_URI=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPO_NAME):latest

deploy:
	@echo "🚀 Building Docker image for deployment..."
	docker buildx build --platform linux/amd64 --provenance=false --output=type=docker -t $(IMAGE_NAME) -f $(DOCKERFILE_PATH) .
	@echo "✅ Docker build completed!"
	
	@echo "🏷️ Tagging the image as: $(IMAGE_URI)"
	docker tag $(IMAGE_NAME):latest $(IMAGE_URI)
	@echo "✅ Image tagged successfully!"
	
	@echo "📤 Pushing image to AWS ECR..."
	docker push $(IMAGE_URI)
	@echo "✅ Image pushed to ECR successfully!"

update-lambda:
	@echo "🔄 Updating AWS Lambda function: $(ECR_REPO_NAME)"
	aws lambda update-function-code --function-name $(ECR_REPO_NAME) --image-uri $(IMAGE_URI)
	@echo "✅ AWS Lambda function updated successfully!"

deploy-lambda: deploy update-lambda
	@echo "🚀 Invoking AWS Lambda function to verify deployment..."
	aws lambda invoke --function-name $(ECR_REPO_NAME) response.json
	@echo "✅ Lambda function invoked successfully!"
	@cat response.json | jq .
	@echo "✅ Deployment to AWS Lambda completed successfully!"

# -----------------------------------------------
# 🔥 Step 4: AWS Lambda Testing & API Invocation
# -----------------------------------------------

test-get-health:
	@echo "🚀 Invoking AWS Lambda function with a GET /health request..."
	aws lambda invoke --function-name $(ECR_REPO_NAME) --payload '{ "version": "2.0", "routeKey": "GET /health", "rawPath": "/health" }' --cli-binary-format raw-in-base64-out response.json
	@echo "✅ Response:"
	@cat response.json | jq .

test-post-search-books:
	@echo "🚀 Invoking AWS Lambda function for POST /search_books..."
	aws lambda invoke --function-name $(ECR_REPO_NAME) --payload '{ "version": "2.0", "routeKey": "POST /search_books", "rawPath": "/search_books", "body": "{\"query\": \"lord of the rings\"}" }' --cli-binary-format raw-in-base64-out response.json
	@echo "✅ Response:"
	@cat response.json | jq .

# -----------------------------------------------
# 🔍 Step 5: Run & Inspect Backend Containers
# -----------------------------------------------

run-container:
	@echo "🚀 Running backend container locally..."
	docker run --rm -p 8000:8000 --platform=linux/amd64 --name backend-lambda $(IMAGE_NAME)
	@echo "✅ Container running at http://localhost:8000"

inspect-container:
	@echo "🔍 Opening shell inside the running container..."


# -----------------------------------------------
#  Optimize Build - Clean Unused Dependencies 
# -----------------------------------------------
clean-deps:
	@BACKEND_DIR="$$(cd "$(dirname "$$0")" && pwd)/backend"; \
	if [ ! -d "$$BACKEND_DIR" ]; then \
		echo "$(RED)❌ Error: Directory $$BACKEND_DIR does not exist.$(RESET)"; \
		exit 1; \
	fi; \
	echo "$(BLUE)📂 Changing directory to $$BACKEND_DIR...$(RESET)"; \
	cd $$BACKEND_DIR; \
	echo "$(YELLOW)🚀 **Activating virtual environment...**$(RESET)"; \
	if [ ! -d "$$BACKEND_DIR/venv" ]; then \
		echo "$(RED)❌ Error: Virtual environment not found in $$BACKEND_DIR/venv.$(RESET)"; \
		echo "$(YELLOW)🔹 Run the following command to create it:$(RESET)"; \
		echo '```sh'; \
		echo "python -m venv venv"; \
		echo '```'; \
		exit 1; \
	fi; \
	echo '```sh'; \
	echo "source venv/bin/activate"; \
	echo '```'; \
	source venv/bin/activate; \
	echo ""; \
	echo "$(GREEN)🔍 **Identifying used dependencies with pipreqs...**$(RESET)"; \
	echo '```sh'; \
	echo "pipreqs . --force"; \
	echo '```'; \
	pipreqs . --force; \
	echo ""; \
	echo "$(GREEN)📜 **Comparing new requirements.txt with original...**$(RESET)"; \
	echo '```sh'; \
	echo "git diff requirements.txt > removed_deps.txt || true"; \
	echo '```'; \
	git diff requirements.txt > removed_deps.txt || true; \
	echo ""; \
	echo "$(YELLOW)🔢 **Number of dependencies removed:**$(RESET)"; \
	echo '```sh'; \
	echo "cat removed_deps.txt | grep '^- ' | wc -l"; \
	echo '```'; \
	cat removed_deps.txt | grep '^- ' | wc -l; \
	echo ""; \
	echo "$(GREEN)✅ **Unused dependencies have been identified. Review 'removed_deps.txt'.**$(RESET)"