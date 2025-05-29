"""
Google Cloud Platform provider implementation for cloud cost optimizer.
This module provides integration with Google Cloud Platform services.
"""

import os
import logging
from typing import Dict, List, Any, Optional
import json

from google.oauth2 import service_account
from google.cloud import compute_v1
from google.cloud import storage
from google.cloud import monitoring_v3
from google.cloud import billing_v1

# Fix the import error by using the correct import path
# Instead of importing CloudCatalog directly, we'll use the client classes

logger = logging.getLogger(__name__)

class GCPProvider:
    """Google Cloud Platform provider for cloud cost optimization."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the GCP provider with optional credentials.
        
        Args:
            credentials_path: Path to the GCP service account credentials JSON file.
                If not provided, will attempt to use application default credentials.
        """
        self.credentials = None
        self.project_id = None
        
        if credentials_path and os.path.exists(credentials_path):
            try:
                self.credentials = service_account.Credentials.from_service_account_file(
                    credentials_path
                )
                with open(credentials_path, 'r') as f:
                    creds_data = json.load(f)
                    self.project_id = creds_data.get('project_id')
                logger.info(f"Initialized GCP provider with credentials from {credentials_path}")
            except Exception as e:
                logger.error(f"Failed to load GCP credentials: {str(e)}")
        else:
            logger.warning("No GCP credentials provided, using application default credentials")
        
    def list_compute_instances(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all compute instances in the specified project.
        
        Args:
            project_id: The GCP project ID. If not provided, uses the project from credentials.
            
        Returns:
            List of compute instances with their details.
        """
        project = project_id or self.project_id
        if not project:
            logger.error("No project ID provided")
            return []
            
        try:
            instance_client = compute_v1.InstancesClient(credentials=self.credentials)
            instances = []
            
            # List instances in all zones
            for zone in self._list_zones(project):
                request = compute_v1.ListInstancesRequest(
                    project=project,
                    zone=zone
                )
                for instance in instance_client.list(request=request):
                    instances.append({
                        'id': instance.id,
                        'name': instance.name,
                        'zone': zone,
                        'machine_type': instance.machine_type,
                        'status': instance.status,
                        'creation_timestamp': instance.creation_timestamp,
                        'labels': instance.labels,
                        'tags': instance.tags.items if instance.tags else []
                    })
            
            return instances
        except Exception as e:
            logger.error(f"Error listing GCP instances: {str(e)}")
            return []
    
    def _list_zones(self, project_id: str) -> List[str]:
        """
        List all zones available in the project.
        
        Args:
            project_id: The GCP project ID.
            
        Returns:
            List of zone names.
        """
        try:
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            request = compute_v1.ListZonesRequest(project=project_id)
            return [zone.name for zone in zones_client.list(request=request)]
        except Exception as e:
            logger.error(f"Error listing GCP zones: {str(e)}")
            return []
    
    def get_billing_data(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get billing data for the specified project.
        
        Args:
            project_id: The GCP project ID. If not provided, uses the project from credentials.
            
        Returns:
            Dictionary containing billing data.
        """
        project = project_id or self.project_id
        if not project:
            logger.error("No project ID provided")
            return {}
            
        try:
            # Use the billing client instead of direct type imports
            billing_client = billing_v1.CloudCatalogClient(credentials=self.credentials)
            
            # Get billing information
            billing_data = {
                'project_id': project,
                'services': []
            }
            
            # List services
            request = billing_v1.ListServicesRequest()
            for service in billing_client.list_services(request=request):
                billing_data['services'].append({
                    'name': service.name,
                    'service_id': service.service_id,
                    'display_name': service.display_name
                })
            
            return billing_data
        except Exception as e:
            logger.error(f"Error getting GCP billing data: {str(e)}")
            return {}
    
    def get_cost_recommendations(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get cost optimization recommendations for the specified project.
        
        Args:
            project_id: The GCP project ID. If not provided, uses the project from credentials.
            
        Returns:
            List of cost optimization recommendations.
        """
        project = project_id or self.project_id
        if not project:
            logger.error("No project ID provided")
            return []
            
        # This is a placeholder for actual recommendation logic
        # In a real implementation, this would use the Recommender API
        recommendations = [
            {
                'id': 'gcp-idle-vm-1',
                'resource_type': 'compute.googleapis.com/Instance',
                'description': 'Idle VM instance detected',
                'estimated_savings': {
                    'amount': 45.20,
                    'currency': 'USD'
                },
                'recommendation': 'Consider stopping or resizing this VM instance'
            },
            {
                'id': 'gcp-oversized-disk-1',
                'resource_type': 'compute.googleapis.com/Disk',
                'description': 'Oversized persistent disk detected',
                'estimated_savings': {
                    'amount': 12.80,
                    'currency': 'USD'
                },
                'recommendation': 'Resize the disk to match actual usage'
            }
        ]
        
        return recommendations
