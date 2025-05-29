"""
Azure provider implementation for cloud cost optimizer.
This module provides integration with Azure services.
"""

import os
import logging
from typing import Dict, List, Any, Optional

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient

from src.config import ConfigManager

logger = logging.getLogger(__name__)

class AzureProvider:
    """Azure provider for cloud cost optimization."""
    
    def __init__(self, client_id=None, client_secret=None, tenant_id=None, subscription_id=None):
        """
        Initialize the Azure provider with optional credentials.
        
        Args:
            client_id: Azure client ID. If not provided, will use the value from configuration.
            client_secret: Azure client secret. If not provided, will use the value from configuration.
            tenant_id: Azure tenant ID. If not provided, will use the value from configuration.
            subscription_id: Azure subscription ID. If not provided, will use the value from configuration.
        """
        # Get configuration
        config = ConfigManager()
        
        # Use provided values or get from config
        self.client_id = client_id or config.get('azure', 'client_id')
        self.client_secret = client_secret or config.get('azure', 'client_secret')
        self.tenant_id = tenant_id or config.get('azure', 'tenant_id')
        self.subscription_id = subscription_id or config.get('azure', 'subscription_id')
        
        self.credential = None
        self.compute_client = None
        self.resource_client = None
        self.storage_client = None
        self.monitor_client = None
        self.consumption_client = None
        
        # Initialize clients if credentials are available
        if self.client_id and self.client_secret and self.tenant_id and self.subscription_id:
            try:
                self.credential = ClientSecretCredential(
                    tenant_id=self.tenant_id,
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
                
                self.compute_client = ComputeManagementClient(
                    credential=self.credential,
                    subscription_id=self.subscription_id
                )
                
                self.resource_client = ResourceManagementClient(
                    credential=self.credential,
                    subscription_id=self.subscription_id
                )
                
                self.storage_client = StorageManagementClient(
                    credential=self.credential,
                    subscription_id=self.subscription_id
                )
                
                self.monitor_client = MonitorManagementClient(
                    credential=self.credential,
                    subscription_id=self.subscription_id
                )
                
                self.consumption_client = ConsumptionManagementClient(
                    credential=self.credential,
                    subscription_id=self.subscription_id
                )
                
                logger.info("Azure provider initialized with credentials")
            except Exception as e:
                logger.error(f"Failed to initialize Azure clients: {str(e)}")
        else:
            logger.warning("Azure provider initialized without credentials")
    
    def list_virtual_machines(self) -> List[Dict[str, Any]]:
        """
        List all virtual machines in the subscription.
        
        Returns:
            List of virtual machines with their details.
        """
        if not self.compute_client:
            logger.error("Azure compute client not initialized")
            return []
            
        try:
            vms = []
            for vm in self.compute_client.virtual_machines.list_all():
                vms.append({
                    'id': vm.id,
                    'name': vm.name,
                    'location': vm.location,
                    'vm_size': vm.hardware_profile.vm_size,
                    'os_type': vm.storage_profile.os_disk.os_type,
                    'provisioning_state': vm.provisioning_state,
                    'tags': vm.tags
                })
            return vms
        except Exception as e:
            logger.error(f"Error listing Azure VMs: {str(e)}")
            return []
    
    def list_storage_accounts(self) -> List[Dict[str, Any]]:
        """
        List all storage accounts in the subscription.
        
        Returns:
            List of storage accounts with their details.
        """
        if not self.storage_client:
            logger.error("Azure storage client not initialized")
            return []
            
        try:
            accounts = []
            for account in self.storage_client.storage_accounts.list():
                accounts.append({
                    'id': account.id,
                    'name': account.name,
                    'location': account.location,
                    'sku': account.sku.name,
                    'kind': account.kind,
                    'provisioning_state': account.provisioning_state,
                    'tags': account.tags
                })
            return accounts
        except Exception as e:
            logger.error(f"Error listing Azure storage accounts: {str(e)}")
            return []
    
    def get_cost_data(self) -> Dict[str, Any]:
        """
        Get cost data for the subscription.
        
        Returns:
            Dictionary containing cost data.
        """
        if not self.consumption_client:
            logger.error("Azure consumption client not initialized")
            return {}
            
        try:
            # In a real implementation, this would use the consumption client
            # For now, return mock data for development/testing
            cost_data = {
                'subscription_id': self.subscription_id,
                'total_cost': 987.65,
                'currency': 'USD',
                'time_period': {
                    'start': '2023-01-01',
                    'end': '2023-01-31'
                },
                'services': [
                    {
                        'name': 'Virtual Machines',
                        'cost': 456.78
                    },
                    {
                        'name': 'Storage',
                        'cost': 98.76
                    },
                    {
                        'name': 'Networking',
                        'cost': 76.54
                    }
                ]
            }
            
            return cost_data
        except Exception as e:
            logger.error(f"Error getting Azure cost data: {str(e)}")
            return {}
    
    def get_cost_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get cost optimization recommendations for the subscription.
        
        Returns:
            List of cost optimization recommendations.
        """
        # This is a placeholder for actual recommendation logic
        # In a real implementation, this would use the Azure Advisor API
        recommendations = [
            {
                'id': 'azure-idle-vm-1',
                'resource_type': 'Microsoft.Compute/virtualMachines',
                'description': 'Idle VM instance detected',
                'estimated_savings': {
                    'amount': 35.40,
                    'currency': 'USD'
                },
                'recommendation': 'Consider stopping or resizing this VM instance'
            },
            {
                'id': 'azure-storage-tier-1',
                'resource_type': 'Microsoft.Storage/storageAccounts',
                'description': 'Storage account with infrequent access',
                'estimated_savings': {
                    'amount': 18.60,
                    'currency': 'USD'
                },
                'recommendation': 'Consider changing storage tier to Cool or Archive'
            }
        ]
        
        return recommendations
