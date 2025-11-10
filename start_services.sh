#!/bin/bash

# Exit on error
set -e

echo "Starting all services..."

# Function to handle cleanup on exit
cleanup() {
    echo "Shutting down services..."
    kill 0
    wait
    echo "All services stopped"
}

# Trap EXIT signal to cleanup
trap cleanup EXIT INT TERM

# Wait for Temporal server to be ready
echo "Waiting for Temporal server at ${WORKFLOW_URL}..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s "${WORKFLOW_URL}" > /dev/null 2>&1; then
        echo "Temporal server is ready!"
        break
    fi
    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts - Temporal not ready yet..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "Warning: Temporal server not reachable, continuing anyway..."
fi

# Start Temporal Worker in background
echo "Starting Temporal Worker..."
cd /app/temporal_workflow
python worker.py > /app/logs/worker.log 2>&1 &
WORKER_PID=$!
echo "Worker started with PID: $WORKER_PID"

# Give worker time to initialize
sleep 2

# Start MCP Server in background
echo "Starting MCP Server..."
cd /app
python mcp_client_Server/mcp_server.py > /app/logs/mcp_server.log 2>&1 &
MCP_PID=$!
echo "MCP Server started with PID: $MCP_PID"

# Give MCP server time to initialize
sleep 2

# Start FastAPI server (in foreground to keep container running)
echo "Starting FastAPI Server on port 8000..."
cd /app
exec python -m uvicorn main:app --host 0.0.0.0 --port 8000
