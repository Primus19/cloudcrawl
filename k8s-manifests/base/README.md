apiVersion: v1
kind: ConfigMap
metadata:
  name: kubectl-apply-instructions
  namespace: cloud-cost-optimizer
data:
  instructions: |
    # Instructions for Applying Storage Fixes
    
    To fix the backend pods that are stuck in Pending state, apply these manifests in order:
    
    ```bash
    # 1. Apply the local storage class
    kubectl apply -f storage-class-hostpath.yaml
    
    # 2. Apply the persistent volumes
    kubectl apply -f terraform-state-pv.yaml
    kubectl apply -f database-pv.yaml
    
    # 3. Delete the existing PVCs that are stuck in Pending
    kubectl delete pvc terraform-state-pvc -n cloud-cost-optimizer
    kubectl delete pvc database-pvc -n cloud-cost-optimizer
    
    # 4. Apply the new PVCs with local-storage class
    kubectl apply -f terraform-state-pvc.yaml
    kubectl apply -f database-pvc.yaml
    
    # 5. Restart the backend deployment to pick up the new storage
    kubectl rollout restart deployment cloud-cost-optimizer-backend -n cloud-cost-optimizer
    
    # 6. Check pod status
    kubectl get pods -n cloud-cost-optimizer
    ```
    
    These commands will switch your storage from EBS (gp2) to local hostPath storage, which doesn't require the EBS CSI driver.
