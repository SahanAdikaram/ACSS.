# .devcontainer/Dockerfile
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install additional OS packages if needed
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace

# Copy requirements.txt
COPY requirements.txt /workspace/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . /workspace/

