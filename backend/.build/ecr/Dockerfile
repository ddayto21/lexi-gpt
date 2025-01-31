# Use AWS Lambda base image for Python
FROM public.ecr.aws/lambda/python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set working directory (AWS Lambda expects /var/task)
WORKDIR /var/task

# Copy dependency file
COPY .build/ecr/requirements.txt .

# Install dependencies into /var/task
RUN pip install --target /var/task -r requirements.txt

# Copy application code
COPY app/ app/

# Ensure dependencies are accessible
ENV PYTHONPATH="/var/task"

# Set the Lambda entry point correctly
CMD ["app.main.handler"]