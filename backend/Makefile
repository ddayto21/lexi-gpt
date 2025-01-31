# Load environment variables from .env
include .env
export $(shell sed 's/=.*//' .env)

# Define target image URI
IMAGE_URI=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPO_NAME):latest

# Colors for better readability
RESET=\033[0m
BLUE=\033[1;34m
GREEN=\033[1;32m
YELLOW=\033[1;33m
RED=\033[1;31m

# Print a separator
define print-separator
	@echo "$(BLUE)------------------------------------------$(RESET)"
endef

# Build, tag, and push the Docker image
deploy:
	@$(call print-separator)
	@echo "$(YELLOW)🚀 Starting Docker build process...$(RESET)"
	docker buildx build --platform linux/amd64 --provenance=false --output=type=docker -t $(IMAGE_NAME) -f $(DOCKERFILE_PATH) .
	@echo "$(GREEN)✅ Docker build completed!$(RESET)"

	@$(call print-separator)
	@echo "$(YELLOW)🏷️  Tagging the image as: $(IMAGE_URI)$(RESET)"
	docker tag $(IMAGE_NAME):latest $(IMAGE_URI)
	@echo "$(GREEN)✅ Image tagged successfully!$(RESET)"

	@$(call print-separator)
	@echo "$(YELLOW)📤 Pushing image to AWS ECR...$(RESET)"
	docker push $(IMAGE_URI)
	@echo "$(GREEN)✅ Image pushed to ECR successfully!$(RESET)"

# ✅ Update AWS Lambda function with the latest image
update-lambda:
	@$(call print-separator)
	@echo "$(YELLOW)🔄 Updating AWS Lambda function: $(ECR_REPO_NAME)$(RESET)"
	aws lambda update-function-code \
		--function-name $(ECR_REPO_NAME) \
		--image-uri $(IMAGE_URI)
	@echo "$(GREEN)✅ AWS Lambda function updated successfully!$(RESET)"

		
deploy-lambda: deploy update-lambda
	@$(call print-separator)
	@echo "$(YELLOW)🚀 Invoking AWS Lambda function to verify deployment...$(RESET)"
	aws lambda invoke --function-name $(ECR_REPO_NAME) response.json
	@echo "$(GREEN)✅ Lambda function invoked successfully!$(RESET)"

	@$(call print-separator)
	@echo "$(YELLOW)📄 Printing Lambda response...$(RESET)"
	cat response.json | jq .
	@echo "$(GREEN)✅ Response printed successfully!$(RESET)"

	@echo "$(GREEN)🎉 Deployment to AWS Lambda completed successfully!$(RESET)"

# ✅ Invoke the Lambda function with a valid payload
invoke-lambda:
	@$(call print-separator)
	@echo "$(YELLOW)🚀 Invoking AWS Lambda function with a valid payload...$(RESET)"
	aws lambda invoke \
		--function-name $(ECR_REPO_NAME) \
		--payload '{ \
			"version": "2.0", \
			"routeKey": "GET /health", \
			"rawPath": "/health", \
			"headers": { \
				"accept": "*/*" \
			}, \
			"requestContext": { \
				"http": { \
					"method": "GET", \
					"path": "/health", \
					"sourceIp": "192.168.1.1" \
				} \
			}, \
			"body": null, \
			"isBase64Encoded": false \
		}' \
		--cli-binary-format raw-in-base64-out \
		response.json
	@echo "$(GREEN)✅ Lambda function invoked successfully!$(RESET)"

	@$(call print-separator)
	@echo "$(YELLOW)📄 Printing Lambda response...$(RESET)"
	cat response.json | jq .
	@echo "$(GREEN)✅ Response printed successfully!$(RESET)"

# Run container locally
run-container:
	@$(call print-separator)
	@echo "$(YELLOW)🚀 Running container locally...$(RESET)"
	docker run --rm -p 8000:8000 --platform=linux/amd64 --name backend-lambda $(IMAGE_NAME)
	@echo "$(GREEN)✅ Container is running on http://localhost:8000$(RESET)"

# Open interactive shell inside the running container
inspect-container:
	@$(call print-separator)
	@echo "$(YELLOW)🔍 Opening shell inside the running container...$(RESET)"
	docker exec -it backend-lambda /bin/bash
	@echo "$(GREEN)✅ Shell session started! Type 'exit' to leave.$(RESET)"