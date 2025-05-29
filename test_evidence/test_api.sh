#!/bin/bash

# Script to run and test the CloudCrawl API
# This script starts the API server and runs basic tests against it

echo "Starting CloudCrawl API server for testing..."

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

# Start the API server in the background
echo "Starting API server..."
python src/api/app.py > api_server.log 2>&1 &
API_PID=$!

# Wait for the server to start
echo "Waiting for server to start..."
sleep 5

# Test the health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:5000/health)
echo "Health endpoint response: $HEALTH_RESPONSE"

# Test the authentication endpoint
echo "Testing authentication endpoint..."
AUTH_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}')
echo "Authentication endpoint response: $AUTH_RESPONSE"

# Extract token from response
TOKEN=$(echo $AUTH_RESPONSE | grep -o '"token":"[^"]*' | sed 's/"token":"//')

# Test the cloud accounts endpoint with authentication
echo "Testing cloud accounts endpoint..."
ACCOUNTS_RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/cloud-accounts -H "Authorization: Bearer $TOKEN")
echo "Cloud accounts endpoint response: $ACCOUNTS_RESPONSE"

# Test the recommendations endpoint
echo "Testing recommendations endpoint..."
RECOMMENDATIONS_RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/recommendations -H "Authorization: Bearer $TOKEN")
echo "Recommendations endpoint response: $RECOMMENDATIONS_RESPONSE"

# Test the Terraform templates endpoint
echo "Testing Terraform templates endpoint..."
TERRAFORM_RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/terraform/templates -H "Authorization: Bearer $TOKEN")
echo "Terraform templates endpoint response: $TERRAFORM_RESPONSE"

# Test the AI recommendations endpoint
echo "Testing AI recommendations endpoint..."
AI_RESPONSE=$(curl -s -X GET http://localhost:5000/api/v1/ai/recommendations -H "Authorization: Bearer $TOKEN")
echo "AI recommendations endpoint response: $AI_RESPONSE"

# Kill the API server
echo "Stopping API server..."
kill $API_PID

# Deactivate virtual environment
deactivate

echo "API testing completed."
