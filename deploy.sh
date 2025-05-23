#!/bin/bash

# This script helps deploy the Cloud Cost Optimizer to EKS with custom image settings

# Set your actual image repository and tag values here
export BACKEND_IMAGE_REPO="637423222780.dkr.ecr.us-east-1.amazonaws.com/cloud-cost-optimizer-backend"
export BACKEND_IMAGE_TAG="latest"
export FRONTEND_IMAGE_REPO="637423222780.dkr.ecr.us-east-1.amazonaws.com/cloud-cost-optimizer-frontend"
export FRONTEND_IMAGE_TAG="latest"

# Build and push backend image
echo "Building backend Docker image..."
docker build -f Dockerfile.backend -t ${BACKEND_IMAGE_REPO}:${BACKEND_IMAGE_TAG} .
docker push ${BACKEND_IMAGE_REPO}:${BACKEND_IMAGE_TAG}

# Build and push frontend image
echo "Building frontend Docker image..."
docker build -f Dockerfile.frontend -t ${FRONTEND_IMAGE_REPO}:${FRONTEND_IMAGE_TAG} .
docker push ${FRONTEND_IMAGE_REPO}:${FRONTEND_IMAGE_TAG}

# Update image patch files with new tags
sed -i "s|image: .*cloud-cost-optimizer-backend.*|        image: ${BACKEND_IMAGE_REPO}:${BACKEND_IMAGE_TAG}|" k8s-manifests/overlays/production/backend-image-patch.yaml
sed -i "s|image: .*cloud-cost-optimizer-frontend.*|        image: ${FRONTEND_IMAGE_REPO}:${FRONTEND_IMAGE_TAG}|" k8s-manifests/overlays/production/frontend-image-patch.yaml


# Example:
# export BACKEND_IMAGE_REPO="123456789012.dkr.ecr.us-west-2.amazonaws.com/cloud-cost-optimizer-backend"
# export BACKEND_IMAGE_TAG="v1.0.0"
# export FRONTEND_IMAGE_REPO="123456789012.dkr.ecr.us-west-2.amazonaws.com/cloud-cost-optimizer-frontend"
# export FRONTEND_IMAGE_TAG="v1.0.0"

# Apply the Kubernetes manifests with the custom image settings
echo "Applying Kubernetes manifests with image settings:"
echo "Backend image: $BACKEND_IMAGE_REPO:$BACKEND_IMAGE_TAG"
echo "Frontend image: $FRONTEND_IMAGE_REPO:$FRONTEND_IMAGE_TAG"

# First, delete the old StatefulSet to avoid conflicts
kubectl delete statefulset postgres -n cloud-cost-optimizer

# Apply the updated manifests
kubectl apply -k k8s-manifests/overlays/production

echo "Deployment initiated. Check pod status with:"
echo "kubectl get pods -n cloud-cost-optimizer"
