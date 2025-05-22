# Cloud Cost Optimizer - Setup Instructions

This document provides instructions for setting up the Cloud Cost Optimizer project with all fixes applied.

## Prerequisites

- Kubernetes cluster (EKS or similar)
- kubectl configured to access your cluster
- Docker for building and pushing images

## Directory Setup for Persistent Volumes

Before applying the Kubernetes manifests, you need to create the required directories on your nodes:

```bash
# SSH into each node and run:
sudo mkdir -p /mnt/data/terraform-state
sudo mkdir -p /mnt/data/database
sudo chmod 777 /mnt/data/terraform-state
sudo chmod 777 /mnt/data/database
```

## Kubernetes Deployment

1. Apply the Kubernetes manifests:

```bash
kubectl apply -k k8s-manifests/overlays/production/
```

2. If you encounter PVC errors because they already exist with a different storage class:

```bash
# Option 1: Delete existing PVCs (if you don't have important data)
kubectl delete pvc database-pvc terraform-state-pvc -n cloud-cost-optimizer
kubectl apply -k k8s-manifests/overlays/production/

# Option 2: Update the storage class in your PV and PVC files to match existing ones
# Edit k8s-manifests/base/persistent-volume-claims.yaml and change storageClassName to match your existing PVCs
```

3. Verify that the pods are running:

```bash
kubectl get pods -n cloud-cost-optimizer
```

## Frontend Build and Deployment

1. Build the frontend Docker image:

```bash
docker build -t your-registry/cloud-cost-optimizer-frontend:latest -f Dockerfile.frontend .
docker push your-registry/cloud-cost-optimizer-frontend:latest
```

2. Update the frontend deployment image if needed:

```bash
kubectl set image deployment/cloud-cost-optimizer-frontend frontend=your-registry/cloud-cost-optimizer-frontend:latest -n cloud-cost-optimizer
```

## Accessing the Application

Once deployed, you can access the application through the configured ingress:

```bash
kubectl get ingress -n cloud-cost-optimizer
```

## Cloud Provider Integration

The application now includes a Cloud Accounts section for managing AWS, GCP, and Azure accounts. This allows you to:

1. Add and manage cloud provider credentials
2. View resources across multiple cloud providers
3. Optimize costs across your entire cloud infrastructure

## Troubleshooting

If you encounter any issues:

1. Check pod logs:
```bash
kubectl logs -f deployment/cloud-cost-optimizer-backend -n cloud-cost-optimizer
kubectl logs -f deployment/cloud-cost-optimizer-frontend -n cloud-cost-optimizer
```

2. Verify ConfigMap exists:
```bash
kubectl get configmap -n cloud-cost-optimizer
```

3. Check PVC status:
```bash
kubectl get pvc -n cloud-cost-optimizer
```
