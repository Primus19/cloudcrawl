#!/bin/bash

# Script to run and test the CloudCrawl API with more detailed logging
# This script starts the API server and runs basic tests against it

echo "Starting CloudCrawl API server for testing with detailed logging..."

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if the app.py file exists
echo "Checking for app.py file..."
if [ ! -f "src/api/app.py" ]; then
    echo "ERROR: src/api/app.py file not found!"
    exit 1
fi

# Print the content of app.py for debugging
echo "Content of app.py:"
cat src/api/app.py

# Check for imported modules
echo "Checking for imported modules..."
grep -n "import" src/api/app.py

# Start the API server in the background with detailed logging
echo "Starting API server with detailed logging..."
PYTHONPATH=$(pwd) python -v src/api/app.py > api_server_detailed.log 2>&1 &
API_PID=$!

# Wait for the server to start
echo "Waiting for server to start..."
sleep 5

# Check if the process is still running
if ps -p $API_PID > /dev/null; then
    echo "API server is running with PID: $API_PID"
else
    echo "ERROR: API server failed to start or crashed immediately"
    echo "Checking logs..."
    cat api_server_detailed.log
    exit 1
fi

# Test the health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:5000/health)
echo "Health endpoint response: $HEALTH_RESPONSE"

# If we got this far, kill the API server
echo "Stopping API server..."
kill $API_PID || echo "Process already terminated"

# Deactivate virtual environment
deactivate

echo "API testing completed."
