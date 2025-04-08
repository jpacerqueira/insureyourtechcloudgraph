#!/bin/bash

# Set environment variables
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_DB=cloud_risk_portal
#export OLLAMA_HOST=http://ollama:11434
export OLLAMA_HOST=http://0.0.0.0:11434
export LLM=llama3.2

# Build the Docker image
echo "Building Docker image..."
docker build -t sql-metadata-rag -f querydata.Docker .

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting..."
    exit 1
fi

# Run the Docker container
echo "Starting Docker container..."
docker run -d \
    --name sql-metadata-rag \
    -p 8507:8507 \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e POSTGRES_HOST=$POSTGRES_HOST \
    -e POSTGRES_PORT=$POSTGRES_PORT \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e POSTGRES_DB=$POSTGRES_DB \
    -e OLLAMA_HOST=$OLLAMA_HOST \
    sql-metadata-rag

# Check if the container started successfully
if [ $? -ne 0 ]; then
    echo "Failed to start container. Exiting..."
    exit 1
fi

echo "Container started successfully!"
echo "Streamlit app is running at http://localhost:8507"

# Show container logs
echo "Showing container logs..."
docker logs -f sql-metadata-rag 