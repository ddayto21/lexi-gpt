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
test-get-health:
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

# Invoke the Lambda function for a POST request to `/search_books`
test-post-search-books:
	@$(call print-separator)
	@echo "$(YELLOW)🚀 Invoking AWS Lambda function for POST /search_books...$(RESET)"
	aws lambda invoke \
		--function-name $(ECR_REPO_NAME) \
		--payload '{ \
			"version": "2.0", \
			"routeKey": "POST /search_books", \
			"rawPath": "/search_books", \
			"headers": { \
				"Content-Type": "application/json" \
			}, \
			"body": "{\"query\": \"lord of the rings\"}", \
			"isBase64Encoded": false, \
			"requestContext": { \
				"http": { \
					"method": "POST", \
					"path": "/search_books", \
					"sourceIp": "127.0.0.1" \
				} \
			} \
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

# Display useful AWS Lambda commands
aws-lambda-help:
	@$(call print-separator)
	@echo "$(YELLOW)📌 Useful AWS Lambda CLI Commands$(RESET)"
	@echo "$(GREEN)🔹 List all Lambda functions:$(RESET)"
	@echo "aws lambda list-functions --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Get details of a specific Lambda function:$(RESET)"
	@echo "aws lambda get-function --function-name $(ECR_REPO_NAME) --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Update Lambda function code with the latest Docker image:$(RESET)"
	@echo "aws lambda update-function-code --function-name $(ECR_REPO_NAME) --image-uri $(IMAGE_URI)"
	@echo ""
	@echo "$(GREEN)🔹 Invoke a Lambda function (sync):$(RESET)"
	@echo "aws lambda invoke --function-name $(ECR_REPO_NAME) response.json"
	@echo ""
	@echo "$(GREEN)🔹 Invoke a Lambda function with payload:$(RESET)"
	@echo "aws lambda invoke --function-name $(ECR_REPO_NAME) --payload '{\"key\": \"value\"}' --cli-binary-format raw-in-base64-out response.json"
	@echo ""
	@echo "$(GREEN)🔹 View Lambda logs using AWS CloudWatch:$(RESET)"
	@echo "aws logs tail /aws/lambda/$(ECR_REPO_NAME) --follow"
	@echo ""
	@echo "$(GREEN)🔹 Get the Lambda function URL (if using Function URLs):$(RESET)"
	@echo "aws lambda get-function-url-config --function-name $(ECR_REPO_NAME)"
	@echo ""
	@echo "$(GREEN)🔹 Add a Lambda function URL (if not behind API Gateway):$(RESET)"
	@echo "aws lambda create-function-url-config --function-name $(ECR_REPO_NAME) --auth-type NONE --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Delete a Lambda function:$(RESET)"
	@echo "aws lambda delete-function --function-name $(ECR_REPO_NAME)"
	@$(call print-separator)


# Display useful AWS API Gateway commands
aws-apigateway-help:
	@$(call print-separator)
	@echo "$(YELLOW)📌 Useful AWS API Gateway Commands$(RESET)"
	@echo "$(GREEN)🔹 List all API Gateways:$(RESET)"
	@echo "aws apigateway get-rest-apis --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Get details of a specific API Gateway:$(RESET)"
	@echo "aws apigateway get-rest-api --rest-api-id ${API_GATEWAY_ID} --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Display all resources for a specific API Gateway:$(RESET)"
	@echo "aws apigateway get-resources --rest-api-id ${API_GATEWAY_ID} --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Display all deployments for a specific API Gateway:$(RESET)"
	@echo "aws apigateway get-deployments --rest-api-id ${API_GATEWAY_ID} --region $(AWS_REGION)"
	@echo ""

	
	@echo "$(BLUE)🔹 Create a new API Gateway REST API:$(BLUE)"
	@echo "aws apigateway create-rest-api --name 'MyAPI' --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Create a new resource (e.g., /health):$(RESET)"
	@echo "aws apigateway create-resource --rest-api-id ${API_GATEWAY_ID} --parent-id <PARENT_ID> --path-part health --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Create a new method (e.g., GET for /health):$(RESET)"
	@echo "aws apigateway put-method --rest-api-id <API_ID> --resource-id <RESOURCE_ID> --http-method GET --authorization-type NONE --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Link API Gateway method to Lambda:$(RESET)"
	@echo "aws apigateway put-integration --rest-api-id <API_ID> --resource-id <RESOURCE_ID> --http-method GET --type AWS_PROXY --integration-http-method POST --uri arn:aws:apigateway:$(AWS_REGION):lambda:path/2015-03-31/functions/$(AWS_LAMBDA_ARN)/invocations"
	@echo ""
	@echo "$(GREEN)🔹 Deploy the API Gateway:$(RESET)"
	@echo "aws apigateway create-deployment --rest-api-id <API_ID> --stage-name dev --region $(AWS_REGION)"
	@echo ""
	@echo "$(GREEN)🔹 Get API Gateway invoke URL:$(RESET)"
	@echo "aws apigateway get-stage --rest-api-id <API_ID> --stage-name dev --region $(AWS_REGION)"
	@echo ""
	@echo "$(RED)🔹 Delete an API Gateway:$(RED)"
	@echo "aws apigateway delete-rest-api --rest-api-id <API_ID> --region $(AWS_REGION)"
	@$(call print-separator)


# ✅ Function to fetch and display API Gateway Invoke URL
aws-apigateway-get-url:
	@$(call print-separator)
	@echo "$(YELLOW)🌐 Fetching API Gateway Invoke URL...$(RESET)"
	@echo "Select a stage:"
	@echo "  (1) dev"
	@echo "  (2) test"
	@echo "  (3) production"
	@read -p "Enter option (1-3): " STAGE_OPTION; \
	case $$STAGE_OPTION in \
		1) STAGE_NAME="dev";; \
		2) STAGE_NAME="test";; \
		3) STAGE_NAME="production";; \
		*) echo "$(RED)❌ Invalid selection! Exiting...$(RESET)"; exit 1;; \
	esac; \
	URL=$$(aws apigateway get-stage \
		--rest-api-id $(API_GATEWAY_ID) \
		--stage-name $$STAGE_NAME \
		--region $(AWS_REGION) \
		--query "invokeUrl" \
		--output text); \
	echo "$(GREEN)✅ API Gateway Invoke URL: $$URL$(RESET)"

# ✅ Function to create a new API Gateway resource with user input
aws-apigateway-create-resource:
	@$(call print-separator)
	@echo "$(YELLOW)🔧 Creating a new API Gateway resource...$(RESET)"
	@read -p "Enter the resource name (e.g., health, books, users): " RESOURCE_NAME; \
	aws apigateway create-resource \
		--rest-api-id $(API_GATEWAY_ID) \
		--parent-id $(API_GATEWAY_ROOT_RESOURCE_ID) \
		--path-part "$$RESOURCE_NAME" \
		--region $(AWS_REGION)
	@echo "$(GREEN)✅ API Gateway resource created successfully!$(RESET)"

aws-apigateway-get-resources:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Fetching API Gateway resources...$(RESET)"
	aws apigateway get-resources \
		--rest-api-id $(API_GATEWAY_ID) \
		--region $(AWS_REGION) | tee apigateway_resources.json
	@echo "$(GREEN)✅ Resources listed successfully! Check 'apigateway_resources.json' for full output.$(RESET)"

# Function to delete an existing API Gateway resource
aws-apigateway-delete-resource:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Fetching API Gateway resources...$(RESET)"
	aws apigateway get-resources \
		--rest-api-id $(API_GATEWAY_ID) \
		--region $(AWS_REGION) | tee apigateway_resources.json

	@echo "$(GREEN)✅ Resources listed successfully! Check 'apigateway_resources.json' for full output.$(RESET)"
	@cat apigateway_resources.json | jq .

	@$(call print-separator)
	@echo "$(RED)Enter the Resource ID to delete: $(RESET)"; \
	read RESOURCE_ID; \
	echo "$(YELLOW)🔴 Deleting resource: $$RESOURCE_ID$(RESET)"; \
	aws apigateway delete-resource \
		--rest-api-id $(API_GATEWAY_ID) \
		--resource-id $$RESOURCE_ID \
		--region $(AWS_REGION)

	@echo "$(GREEN)🔴  API Gateway resource successfully deleted.$(RESET)"

# ✅ Function to create a POST method for an API Gateway resource
aws-apigateway-create-post-method:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Fetching API Gateway resources...$(RESET)"
	aws apigateway get-resources \
		--rest-api-id $(API_GATEWAY_ID) \
		--region $(AWS_REGION) | tee apigateway_resources.json

	@echo "$(GREEN)✅ Resources listed successfully! Check 'apigateway_resources.json' for full output.$(RESET)"
	@cat apigateway_resources.json | jq .

	@$(call print-separator)
	@echo "$(BLUE)Enter the Resource ID where the POST method should be created:$(RESET)"; \
	read RESOURCE_ID; \
	echo "$(YELLOW)🔧 Creating POST method on resource: $$RESOURCE_ID$(RESET)"; \
	aws apigateway put-method \
		--region $(AWS_REGION) \
		--rest-api-id $(API_GATEWAY_ID) \
		--resource-id $$RESOURCE_ID \
		--http-method POST \
		--authorization-type NONE

	@echo "$(GREEN)✅ POST method successfully created!$(RESET)"


# ✅ Function to integrate a POST method with AWS Lambda in API Gateway
aws-apigateway-integrate-post-method-with-lambda:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Fetching API Gateway resources...$(RESET)"
	aws apigateway get-resources \
		--rest-api-id $(API_GATEWAY_ID) \
		--region $(AWS_REGION) | tee apigateway_resources.json

	@echo "$(GREEN)✅ Resources listed successfully! Check 'apigateway_resources.json' for full output.$(RESET)"
	@cat apigateway_resources.json | jq .

	@$(call print-separator)
	@echo "$(BLUE)Enter the Resource ID for the POST method integration:$(RESET)"; \
	read RESOURCE_ID; \
	echo "$(YELLOW)🔧 Integrating POST method with AWS Lambda for resource: $$RESOURCE_ID$(RESET)"; \
	aws apigateway put-integration \
		--region $(AWS_REGION) \
		--rest-api-id $(API_GATEWAY_ID) \
		--resource-id $$RESOURCE_ID \
		--http-method POST \
		--integration-http-method POST \
		--type AWS_PROXY \
		--uri "arn:aws:apigateway:$(AWS_REGION):lambda:path/2015-03-31/functions/$(LAMBDA_FUNCTION_ARN)/invocations"

	@echo "$(GREEN)✅ Successfully integrated POST method with AWS Lambda!$(RESET)"

# ✅ Function to create an API Gateway deployment
aws-apigateway-create-deployment:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Enter the REST API ID: $(RESET)"; \
	read API_GATEWAY_ID; \
	if [ -z "$$API_GATEWAY_ID" ]; then \
		echo "$(RED)❌ Error: REST API ID cannot be empty!$(RESET)"; \
		exit 1; \
	fi; \
	echo "$(YELLOW)📜 Enter the stage name (dev, test, production): $(RESET)"; \
	read STAGE_NAME; \
	if [ -z "$$STAGE_NAME" ]; then \
		echo "$(RED)❌ Error: Stage name cannot be empty!$(RESET)"; \
		exit 1; \
	fi; \
	echo "$(YELLOW)🚀 Deploying API Gateway (REST API ID: $$API_GATEWAY_ID) to stage: $$STAGE_NAME...$(RESET)"; \
	aws apigateway create-deployment \
		--rest-api-id $$API_GATEWAY_ID \
		--stage-name $$STAGE_NAME \
		--region $(AWS_REGION); \
	echo "$(GREEN)✅ Deployment to stage '$$STAGE_NAME' completed successfully!$(RESET)"
# ✅ Function to create an IAM role for AWS Lambda
aws-iam-create-lambda-role:
	@$(call print-separator)
	@echo "$(YELLOW)🚀 Creating IAM role: $(LAMBDA_ROLE_NAME)...$(RESET)"
	@if [ -z "$(LAMBDA_ROLE_NAME)" ]; then \
		echo "$(RED)❌ Error: LAMBDA_ROLE_NAME is not set in .env file!$(RESET)"; \
		exit 1; \
	fi
	@if [ ! -f lambda-role-policy.json ]; then \
		echo "$(RED)❌ Error: 'lambda-role-policy.json' not found!$(RESET)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)⏳ Creating IAM role...$(RESET)"
	@ROLE_ARN=$$(aws iam create-role \
		--role-name $(LAMBDA_ROLE_NAME) \
		--assume-role-policy-document file://lambda-role-policy.json \
		--query 'Role.Arn' \
		--output text); \
	if [ -z "$$ROLE_ARN" ]; then \
		echo "$(RED)❌ IAM role creation failed!$(RESET)"; \
		exit 1; \
	fi; \
	echo "$$ROLE_ARN" | tee lambda-role-arn.txt; \
	echo "$(GREEN)✅ IAM role created successfully! ARN: $$ROLE_ARN (stored in 'lambda-role-arn.txt')$(RESET)"

# ✅ Function to attach the AWSLambdaBasicExecutionRole policy to the IAM role
aws-iam-attach-lambda-policy:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Reading the IAM role ARN from 'lambda-role-arn.txt'...$(RESET)"

	@if [ ! -f lambda-role-arn.txt ]; then \
		echo "$(RED)❌ Error: 'lambda-role-arn.txt' not found!$(RESET)"; \
		exit 1; \
	fi

	@ROLE_ARN=$$(cat lambda-role-arn.txt); \
	ROLE_NAME=$$(echo $$ROLE_ARN | awk -F'role/' '{print $$2}'); \
	echo "$(BLUE)🔍 Extracted Role ARN: $$ROLE_ARN$(RESET)"; \
	echo "$(BLUE)🔍 Extracted Role Name: $$ROLE_NAME$(RESET)"; \
	echo ""

	@if [ -z "$$ROLE_NAME" ]; then \
		echo "$(RED)❌ Error: Could not extract role name from ARN!$(RESET)"; \
		exit 1; \
	fi

	@echo "$(YELLOW)🔗 Attaching AWSLambdaBasicExecutionRole policy to role: $$ROLE_NAME...$(RESET)"
	aws iam attach-role-policy \
		--role-name $$ROLE_NAME \
		--policy-arn arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole

	@echo "$(GREEN)✅ Policy attached successfully to the Lambda role!$(RESET)"



# ✅ Function to display useful AWS IAM CLI commands
aws-iam-help:
	@$(call print-separator)
	@echo "$(YELLOW)📜 Useful AWS IAM CLI Commands$(RESET)"
	@echo "$(BLUE)🔍 List all IAM roles:$(RESET)"
	@echo "    aws iam list-roles --query 'Roles[*].{RoleName:RoleName, ARN:Arn}' --output table"
	@echo ""
	@echo "$(BLUE)🔍 Get details of a specific IAM role:$(RESET)"
	@echo "    aws iam get-role --role-name <ROLE_NAME>"
	@echo ""
	@echo "$(BLUE)🔍 List all attached policies for a specific IAM role:$(RESET)"
	@echo "    aws iam list-attached-role-policies --role-name <ROLE_NAME>"
	@echo ""
	@echo "$(BLUE)🔍 List inline policies attached to a specific IAM role:$(RESET)"
	@echo "    aws iam list-role-policies --role-name <ROLE_NAME>"
	@echo ""
	@echo "$(BLUE)🔍 Get the permissions for an IAM policy:$(RESET)"
	@echo "    aws iam get-policy --policy-arn <POLICY_ARN>"
	@echo ""
	@echo "$(BLUE)🔍 Get IAM role trust relationship (who can assume the role):$(RESET)"
	@echo "    aws iam get-role --role-name <ROLE_NAME> --query 'Role.AssumeRolePolicyDocument'"
	@echo ""
	@echo "$(BLUE)🔍 Attach a managed policy to an IAM role:$(RESET)"
	@echo "    aws iam attach-role-policy --role-name <ROLE_NAME> --policy-arn arn:aws:iam::aws:policy/<POLICY_NAME>"
	@echo ""
	@echo "$(BLUE)🔍 Detach a managed policy from an IAM role:$(RESET)"
	@echo "    aws iam detach-role-policy --role-name <ROLE_NAME> --policy-arn arn:aws:iam::aws:policy/<POLICY_NAME>"
	@echo ""
	@echo "$(BLUE)❌ Delete an IAM role (must detach policies first):$(RESET)"
	@echo "    aws iam delete-role --role-name <ROLE_NAME>"
	@echo ""
	@echo "$(GREEN)✅ Use these commands to manage IAM roles and permissions efficiently!$(RESET)"
	@$(call print-separator)