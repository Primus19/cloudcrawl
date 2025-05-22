# EBS Storage Migration Instructions for Cloud Cost Optimizer

This guide provides instructions for migrating from hostPath volumes to AWS EBS volumes for your Cloud Cost Optimizer backend pods in EKS.

## Why Switch to EBS?

- **Reliability**: EBS volumes are more reliable than hostPath volumes in EKS
- **Persistence**: Data persists even if nodes are terminated
- **Managed Service**: AWS handles the underlying storage infrastructure
- **Dynamic Provisioning**: Volumes are created on-demand

## Migration Steps

### 1. Delete Existing PVCs (if they exist)

```bash
kubectl delete pvc terraform-state-pvc database-pvc -n cloud-cost-optimizer
```

### 2. Apply the EBS Storage Configuration

```bash
kubectl apply -k .
```

This will create:
- An EBS StorageClass (`ebs-sc`)
- PVCs for terraform state and database that use the EBS StorageClass

### 3. Restart the Backend Deployment

```bash
kubectl rollout restart deployment cloud-cost-optimizer-backend -n cloud-cost-optimizer
```

### 4. Verify the Pods are Running

```bash
kubectl get pods -n cloud-cost-optimizer
```

## Troubleshooting

If you encounter issues:

1. Check if the EBS CSI driver is installed on your EKS cluster:
   ```bash
   kubectl get deployment ebs-csi-controller -n kube-system
   ```

2. If not installed, add it using the AWS EKS console or with eksctl:
   ```bash
   eksctl create addon --name aws-ebs-csi-driver --cluster your-cluster-name --region your-region
   ```

3. Verify PVC status:
   ```bash
   kubectl get pvc -n cloud-cost-optimizer
   ```

4. Check pod events:
   ```bash
   kubectl describe pod -n cloud-cost-optimizer [pod-name]
   ```

## Data Migration (if needed)

If you need to migrate existing data from hostPath volumes to EBS:

1. Create a temporary pod that mounts both volumes
2. Copy data from hostPath to EBS volume
3. Delete the temporary pod

Example migration pod:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-migration
  namespace: cloud-cost-optimizer
spec:
  containers:
  - name: data-migration
    image: busybox
    command: ["/bin/sh", "-c", "cp -r /source/* /destination/ && sleep 3600"]
    volumeMounts:
    - name: source-volume
      mountPath: /source
    - name: destination-volume
      mountPath: /destination
  volumes:
  - name: source-volume
    hostPath:
      path: /mnt/data/terraform-state
  - name: destination-volume
    persistentVolumeClaim:
      claimName: terraform-state-pvc
```

## Reverting (if necessary)

If you need to revert to hostPath volumes:

1. Delete the EBS PVCs
2. Reapply your original hostPath PVCs
3. Restart the backend deployment
