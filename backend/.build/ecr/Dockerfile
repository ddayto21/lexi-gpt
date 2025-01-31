# Use AWS Lambda base image for Python
FROM public.ecr.aws/lambda/python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.0.1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory (AWS Lambda expects /var/task)
WORKDIR /var/task

# Copy dependency files
COPY .build/ecr/requirements.txt ./

# Install dependencies for AWS Lambda **inside /var/task**
RUN pip install --target /var/task -r requirements.txt

# Copy application code
COPY . .

# Ensure dependencies are accessible
ENV PYTHONPATH="/var/task"

# Set the Lambda entry point to `app.lambda_handler.handler`
CMD ["app.lambda_handler.handler"]