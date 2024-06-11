# .devcontainer/Dockerfile
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install additional OS packages
RUN apt-get update && apt-get install -y curl

# Install Docker and Docker Compose
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Start Docker
RUN service docker start

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

# Specify the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
