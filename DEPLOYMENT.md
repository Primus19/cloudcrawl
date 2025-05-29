# CloudCrawl Deployment Documentation

## Overview
This document provides detailed instructions for deploying the CloudCrawl application, which consists of:
- Backend API service (Python Flask)
- Frontend UI (React)
- Database (PostgreSQL)

## Prerequisites
- Docker and Docker Compose for local development
- Kubernetes cluster for production deployment
- kubectl configured to access your cluster
- Helm 3.x installed

## Docker Image Build Instructions

### Backend API Image
1. Navigate to the project root directory
2. Build the API Docker image:
```bash
docker build -t your-registry/cloudcrawl-api:latest -f Dockerfile .
```
3. Push the image to your container registry:
```bash
docker push your-registry/cloudcrawl-api:latest
```

### Frontend UI Image
1. Navigate to the UI directory:
```bash
cd src/ui/dashboard
```
2. Build the UI:
```bash
npm install
npm run build
```
3. Build the UI Docker image:
```bash
docker build -t your-registry/cloudcrawl-ui:latest -f Dockerfile .
```
4. Push the image to your container registry:
```bash
docker push your-registry/cloudcrawl-ui:latest
```

## Kubernetes Deployment

### Update Helm Values
1. Edit the `charts/cloudcrawl/values.yaml` file to update:
   - Image repository references to your registry
   - Ingress host to your domain
   - Any environment-specific configurations

Example:
```yaml
image:
  repository:
    api: your-registry/cloudcrawl-api
    ui: your-registry/cloudcrawl-ui
  tag: latest
  pullPolicy: Always
```

### Deploy with Helm
1. Install the Helm chart:
```bash
helm install cloudcrawl ./charts/cloudcrawl --namespace your-namespace --create-namespace
```

2. Verify the deployment:
```bash
kubectl get pods -n your-namespace
kubectl get services -n your-namespace
kubectl get ingress -n your-namespace
```

## Troubleshooting

### Common Issues

#### Pod in "Pending" State
- Check if your cluster has enough resources
- Verify PersistentVolumeClaims are bound
- Check node selectors and taints

#### "InvalidImageName" Error
- Ensure image names in values.yaml are correct
- Verify images are pushed to the registry
- Check imagePullSecrets if using private registry

#### API Connection Issues
- Verify services are running: `kubectl get svc`
- Check pod logs: `kubectl logs <pod-name>`
- Ensure environment variables are correctly set

## Local Development Setup

### Using Docker Compose
1. Navigate to the project root
2. Run:
```bash
docker-compose up -d
```
3. Access the application at http://localhost:3000

## Security Considerations
- The default JWT secret in values.yaml is for development only
- For production, generate a secure secret and update the values.yaml file
- Enable TLS for ingress in production environments
- Review and adjust resource limits based on your workload

## Monitoring and Maintenance
- The application exposes a /health endpoint for monitoring
- Configure liveness and readiness probes as needed
- Set up logging and monitoring solutions like Prometheus and Grafana
