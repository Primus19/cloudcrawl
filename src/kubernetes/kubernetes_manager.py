"""
Kubernetes deployment manifests for Cloud Cost Optimizer.
This module provides functionality for managing Kubernetes deployments.
"""

import os
import yaml
import logging
import uuid
import tempfile
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime

class KubernetesManager:
    """Manager for Kubernetes deployments."""
    
    def __init__(self):
        """Initialize the Kubernetes manager."""
        self.logger = logging.getLogger(__name__)
        
        # Base directory for Kubernetes manifests
        self.manifests_dir = os.path.join(os.path.dirname(__file__), 'manifests')
        os.makedirs(self.manifests_dir, exist_ok=True)
        
        # Initialize with sample manifests
        self._initialize_sample_manifests()
    
    def get_manifests(self) -> List[Dict[str, Any]]:
        """
        Get all Kubernetes manifests.
        
        Returns:
            List of manifests
        """
        manifests = []
        
        # Get all YAML files in the manifests directory
        for filename in os.listdir(self.manifests_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(self.manifests_dir, filename)
                
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Parse YAML
                    manifest = yaml.safe_load(content)
                    
                    # Add metadata
                    manifests.append({
                        'name': os.path.splitext(filename)[0],
                        'filename': filename,
                        'path': file_path,
                        'kind': manifest.get('kind', 'Unknown'),
                        'api_version': manifest.get('apiVersion', 'v1'),
                        'metadata': manifest.get('metadata', {}),
                        'content': content
                    })
                except Exception as e:
                    self.logger.error(f"Error parsing manifest {filename}: {str(e)}")
        
        return manifests
    
    def get_manifest(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific Kubernetes manifest by name.
        
        Args:
            name: Manifest name
            
        Returns:
            Manifest or None if not found
        """
        # Get all manifests
        manifests = self.get_manifests()
        
        # Find manifest by name
        for manifest in manifests:
            if manifest['name'] == name:
                return manifest
        
        return None
    
    def create_manifest(self, name: str, content: str) -> bool:
        """
        Create a new Kubernetes manifest.
        
        Args:
            name: Manifest name
            content: YAML content
            
        Returns:
            True if manifest was created, False otherwise
        """
        try:
            # Validate YAML
            manifest = yaml.safe_load(content)
            if not manifest:
                raise ValueError("Invalid YAML content")
            
            # Create file
            filename = f"{name}.yaml"
            file_path = os.path.join(self.manifests_dir, filename)
            
            # Check if file already exists
            if os.path.exists(file_path):
                raise ValueError(f"Manifest {name} already exists")
            
            # Write file
            with open(file_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            self.logger.error(f"Error creating manifest {name}: {str(e)}")
            return False
    
    def update_manifest(self, name: str, content: str) -> bool:
        """
        Update a Kubernetes manifest.
        
        Args:
            name: Manifest name
            content: New YAML content
            
        Returns:
            True if manifest was updated, False otherwise
        """
        try:
            # Validate YAML
            manifest = yaml.safe_load(content)
            if not manifest:
                raise ValueError("Invalid YAML content")
            
            # Get file path
            filename = f"{name}.yaml"
            file_path = os.path.join(self.manifests_dir, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValueError(f"Manifest {name} not found")
            
            # Write file
            with open(file_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            self.logger.error(f"Error updating manifest {name}: {str(e)}")
            return False
    
    def delete_manifest(self, name: str) -> bool:
        """
        Delete a Kubernetes manifest.
        
        Args:
            name: Manifest name
            
        Returns:
            True if manifest was deleted, False otherwise
        """
        try:
            # Get file path
            filename = f"{name}.yaml"
            file_path = os.path.join(self.manifests_dir, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                raise ValueError(f"Manifest {name} not found")
            
            # Delete file
            os.remove(file_path)
            
            return True
        except Exception as e:
            self.logger.error(f"Error deleting manifest {name}: {str(e)}")
            return False
    
    def validate_manifest(self, content: str) -> Dict[str, Any]:
        """
        Validate a Kubernetes manifest.
        
        Args:
            content: YAML content
            
        Returns:
            Validation result
        """
        try:
            # Validate YAML
            manifest = yaml.safe_load(content)
            if not manifest:
                return {
                    'valid': False,
                    'errors': ['Invalid YAML content']
                }
            
            # Check required fields
            required_fields = ['apiVersion', 'kind', 'metadata']
            missing_fields = [field for field in required_fields if field not in manifest]
            
            if missing_fields:
                return {
                    'valid': False,
                    'errors': [f"Missing required field: {field}" for field in missing_fields]
                }
            
            # Check metadata
            if 'name' not in manifest['metadata']:
                return {
                    'valid': False,
                    'errors': ['Missing required field: metadata.name']
                }
            
            # In a real implementation, this would use kubectl to validate the manifest
            # For demonstration, we'll just check the basic structure
            
            return {
                'valid': True,
                'errors': []
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [str(e)]
            }
    
    def _initialize_sample_manifests(self):
        """Initialize with sample Kubernetes manifests."""
        # API Deployment
        api_deployment = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudcrawl-api
  labels:
    app: cloudcrawl
    component: api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cloudcrawl
      component: api
  template:
    metadata:
      labels:
        app: cloudcrawl
        component: api
    spec:
      containers:
      - name: api
        image: cloudcrawl/api:latest
        ports:
        - containerPort: 5000
        env:
        - name: PORT
          value: "5000"
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: cloudcrawl-secrets
              key: jwt-secret
        resources:
          limits:
            cpu: "1"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 15
          periodSeconds: 20
"""
        
        # UI Deployment
        ui_deployment = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudcrawl-ui
  labels:
    app: cloudcrawl
    component: ui
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cloudcrawl
      component: ui
  template:
    metadata:
      labels:
        app: cloudcrawl
        component: ui
    spec:
      containers:
      - name: ui
        image: cloudcrawl/ui:latest
        ports:
        - containerPort: 80
        env:
        - name: API_URL
          value: "http://cloudcrawl-api:5000"
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "200m"
            memory: "256Mi"
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
"""
        
        # API Service
        api_service = """
apiVersion: v1
kind: Service
metadata:
  name: cloudcrawl-api
  labels:
    app: cloudcrawl
    component: api
spec:
  selector:
    app: cloudcrawl
    component: api
  ports:
  - port: 5000
    targetPort: 5000
    protocol: TCP
  type: ClusterIP
"""
        
        # UI Service
        ui_service = """
apiVersion: v1
kind: Service
metadata:
  name: cloudcrawl-ui
  labels:
    app: cloudcrawl
    component: ui
spec:
  selector:
    app: cloudcrawl
    component: ui
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  type: ClusterIP
"""
        
        # Ingress
        ingress = """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cloudcrawl-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
  - host: cloudcrawl.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: cloudcrawl-api
            port:
              number: 5000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: cloudcrawl-ui
            port:
              number: 80
  tls:
  - hosts:
    - cloudcrawl.example.com
    secretName: cloudcrawl-tls
"""
        
        # Secrets
        secrets = """
apiVersion: v1
kind: Secret
metadata:
  name: cloudcrawl-secrets
type: Opaque
data:
  jwt-secret: c2VjcmV0LWtleS1mb3ItZGV2ZWxvcG1lbnQ=  # base64 encoded "secret-key-for-development"
"""
        
        # Create manifest files
        self.create_manifest('api-deployment', api_deployment)
        self.create_manifest('ui-deployment', ui_deployment)
        self.create_manifest('api-service', api_service)
        self.create_manifest('ui-service', ui_service)
        self.create_manifest('ingress', ingress)
        self.create_manifest('secrets', secrets)
