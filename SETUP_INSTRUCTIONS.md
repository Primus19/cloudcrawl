# Cloud Cost Optimizer - Setup Instructions

This document provides instructions for deploying the Cloud Cost Optimizer application with fully automated setup.

## Overview

The Cloud Cost Optimizer is a comprehensive solution for managing and optimizing cloud resources across AWS, GCP, and Azure. The application includes:

- Account management for cloud providers
- Resource discovery and visualization
- Cost analysis and optimization recommendations
- Terraform template management and deployment
- Fully automated database setup

## Prerequisites

- Kubernetes cluster with kubectl access
- AWS EBS CSI driver installed (for EBS storage)
- Container registry for storing images

## Deployment Steps

### 1. Create Namespace

```bash
kubectl create namespace cloud-cost-optimizer
```

### 2. Deploy Application

The application is deployed using Kustomize, which handles all components including:
- PostgreSQL database with automated schema initialization
- Backend API server
- Frontend web interface
- All required ConfigMaps, Secrets, and PersistentVolumeClaims

```bash
# From the repository root
kubectl apply -k k8s-manifests/overlays/production
```

This single command will:
1. Create the EBS storage class
2. Deploy PostgreSQL with persistent storage
3. Initialize the database schema automatically
4. Deploy the backend with health checks
5. Deploy the frontend
6. Create an Ingress for external access

### 3. Build and Push Images

Before deployment, build and push the Docker images:

```bash
# Build and push backend image
docker build -t your-registry/cloud-cost-optimizer-backend:latest -f Dockerfile.backend .
docker push your-registry/cloud-cost-optimizer-backend:latest

# Build and push frontend image
docker build -t your-registry/cloud-cost-optimizer-frontend:latest -f Dockerfile.frontend .
docker push your-registry/cloud-cost-optimizer-frontend:latest
```

Update the image references in `k8s-manifests/overlays/production/kustomization.yaml`:

```yaml
images:
  - name: ${BACKEND_IMAGE}
    newName: your-registry/cloud-cost-optimizer-backend
    newTag: latest
  - name: ${FRONTEND_IMAGE}
    newName: your-registry/cloud-cost-optimizer-frontend
    newTag: latest
```

## Configuration

### Security Credentials

For production deployment, update the secrets in `k8s-manifests/base/secrets.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud-cost-optimizer-secrets
  namespace: cloud-cost-optimizer
type: Opaque
stringData:
  postgres_user: "postgres"
  postgres_password: "changeme"  # Change this!
  credential_encryption_key: "changeme_with_secure_random_key"  # Change this!
```

## Accessing the Application

After deployment, the application will be available at the Ingress address:

```bash
kubectl get ingress -n cloud-cost-optimizer
```

## Features

The Cloud Cost Optimizer provides:

1. **AWS Integration**:
   - Account management with IAM role support
   - Resource discovery for EC2, S3, RDS, Lambda, and EKS
   - Cost analysis and optimization recommendations

2. **Terraform Template Management**:
   - Template creation and versioning
   - Variable support and customization
   - Cost estimation before deployment
   - Deployment workflow with plan, apply, and destroy operations

3. **Database**: Fully automated PostgreSQL setup with:
   - Secure credential storage
   - Resource metadata
   - Cost data
   - Terraform state management

## Troubleshooting

If you encounter issues:

1. Check pod status:
   ```bash
   kubectl get pods -n cloud-cost-optimizer
   ```

2. Check logs:
   ```bash
   kubectl logs -n cloud-cost-optimizer deployment/cloud-cost-optimizer-backend
   kubectl logs -n cloud-cost-optimizer deployment/cloud-cost-optimizer-frontend
   ```

3. Verify database initialization:
   ```bash
   kubectl logs -n cloud-cost-optimizer job/postgres-init-job
   ```

## Extending the Application

The Cloud Cost Optimizer is designed for easy extension to support GCP and Azure:

1. Implement provider interfaces in `src/providers/`
2. Add API endpoints in `src/api/`
3. Update frontend components to support new providers

All infrastructure is already in place to support multi-cloud operations.
