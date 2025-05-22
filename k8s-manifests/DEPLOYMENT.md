# Cloud Cost Optimizer - Deployment Guide for PrimusAllCluster

This guide provides step-by-step instructions for deploying the Cloud Cost Optimizer to your existing EKS cluster (PrimusAllCluster).

## Prerequisites

- AWS CLI configured with appropriate permissions
- kubectl installed and configured to access your EKS cluster
- Docker installed for building container images
- Terraform installed (v1.0.0+)

## Repository Structure

```
k8s-manifests/
├── base/                      # Base Kubernetes manifests
│   ├── namespace.yaml
│   ├── service-account.yaml
│   ├── rbac.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── persistent-volume-claims.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── horizontal-pod-autoscaler.yaml
│   ├── ingress.yaml
│   └── kustomization.yaml
├── overlays/                  # Environment-specific overlays
│   └── production/
│       ├── configmap.yaml
│       └── kustomization.yaml
└── terraform/                 # Terraform files for AWS resources
    ├── main.tf
    └── variables.tf
```

## Deployment Steps

### 1. Set Up AWS Resources with Terraform

First, deploy the necessary AWS resources (ECR repositories and IAM roles) using Terraform:

```bash
cd k8s-manifests/terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan -var="cluster_name=PrimusAllCluster"

# Apply the configuration
terraform apply -var="cluster_name=PrimusAllCluster"
```

This will create:
- ECR repositories for your container images
- IAM roles and policies for the application
- Service account annotations for IAM role integration

### 2. Build and Push Docker Images

Use the commands from the Terraform output to build and push your Docker images:

```bash
# Navigate to the project root
cd /path/to/cloud-cost-optimizer

# Build and push backend image
docker build -t <backend-ecr-url>:latest -f Dockerfile.backend .
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <backend-ecr-url>
docker push <backend-ecr-url>:latest

# Build and push frontend image
cd src/ui/dashboard
docker build -t <frontend-ecr-url>:latest -f Dockerfile.frontend .
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <frontend-ecr-url>
docker push <frontend-ecr-url>:latest
```

### 3. Update Kubernetes Manifests

Update the image references in the Kustomize overlay:

```bash
cd k8s-manifests/overlays/production

# Update the image URLs in the kustomization.yaml file
sed -i 's|your-registry/cloud-cost-optimizer-backend:latest|<backend-ecr-url>:latest|g' kustomization.yaml
sed -i 's|your-registry/cloud-cost-optimizer-frontend:latest|<frontend-ecr-url>:latest|g' kustomization.yaml
```

### 4. Update Cloud Provider Credentials

Before deploying, update the cloud provider credentials in the secrets file:

```bash
# Edit the secrets.yaml file to include your actual cloud provider credentials
vi ../../base/secrets.yaml
```

Replace the placeholder values with your actual AWS, Azure, and GCP credentials.

### 5. Deploy to Kubernetes

Apply the Kubernetes manifests using Kustomize:

```bash
# Ensure kubectl is configured for your cluster
aws eks update-kubeconfig --region <your-region> --name PrimusAllCluster

# Apply the manifests
kubectl apply -k .
```

### 6. Verify the Deployment

Check that all resources are deployed correctly:

```bash
# Check pods
kubectl get pods -n cloud-cost-optimizer

# Check services
kubectl get svc -n cloud-cost-optimizer

# Check the LoadBalancer endpoint
kubectl get svc cloud-cost-optimizer-frontend -n cloud-cost-optimizer
```

The frontend service is configured as a LoadBalancer, which will provision an AWS Load Balancer automatically. You can access the application using the external IP/hostname provided by the LoadBalancer.

### 7. Access the Application

Once the LoadBalancer is provisioned (which may take a few minutes), you can access the application at:

```
http://<load-balancer-hostname>
```

You can find the hostname with:

```bash
kubectl get svc cloud-cost-optimizer-frontend -n cloud-cost-optimizer -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

## Troubleshooting

### Pod Startup Issues

If pods are not starting correctly:

```bash
kubectl describe pod <pod-name> -n cloud-cost-optimizer
kubectl logs <pod-name> -n cloud-cost-optimizer
```

### Service Connectivity Issues

If services cannot communicate:

```bash
# Test backend connectivity
kubectl exec -it <frontend-pod-name> -n cloud-cost-optimizer -- curl cloud-cost-optimizer-backend:5000/api/v1/health
```

### LoadBalancer Issues

If the LoadBalancer is not provisioning:

```bash
kubectl describe svc cloud-cost-optimizer-frontend -n cloud-cost-optimizer
```

## Scaling the Application

The application is configured with Horizontal Pod Autoscalers that will automatically scale the deployments based on CPU utilization. You can modify the scaling parameters:

```bash
kubectl edit hpa cloud-cost-optimizer-backend-hpa -n cloud-cost-optimizer
kubectl edit hpa cloud-cost-optimizer-frontend-hpa -n cloud-cost-optimizer
```

## Cleanup

To remove the application from your cluster:

```bash
kubectl delete -k k8s-manifests/overlays/production
```

To remove the AWS resources created by Terraform:

```bash
cd k8s-manifests/terraform
terraform destroy -var="cluster_name=PrimusAllCluster"
```
