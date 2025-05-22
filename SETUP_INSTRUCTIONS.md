# Node Setup Instructions for Local Storage

To ensure the backend pods can successfully mount the required volumes, you need to create the storage directories on each node where your pods might run:

```bash
# SSH into each node and run:
sudo mkdir -p /mnt/data/terraform-state
sudo mkdir -p /mnt/data/database
sudo chmod 777 /mnt/data/terraform-state
sudo chmod 777 /mnt/data/database
```

These directories will be used by the PersistentVolumes defined in the Kubernetes manifests.

# Deployment Instructions

1. Apply the Kubernetes manifests using Kustomize:
   ```bash
   kubectl apply -k k8s-manifests/overlays/production/
   ```

2. Verify that the backend pods are running:
   ```bash
   kubectl get pods -n cloud-cost-optimizer
   ```

3. If the backend pods are still in Pending state, check the events:
   ```bash
   kubectl describe pod -l tier=backend -n cloud-cost-optimizer
   ```

4. Build and deploy the frontend:
   ```bash
   cd src/ui/dashboard
   npm install --force
   npm run build
   ```

5. Deploy using your existing CI/CD pipeline or manually update the frontend container.

# Production Considerations

For production environments, you may want to:

1. Configure proper EBS storage with the EBS CSI driver instead of using hostPath storage
2. Implement additional security measures for cloud credentials
3. Add more validation and error handling for cloud account operations
