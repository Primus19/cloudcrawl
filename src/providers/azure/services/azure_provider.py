"""
Azure provider implementation for cloud cost optimizer.
"""
import datetime
from typing import Dict, List, Any, Optional
from uuid import UUID

# Azure SDK imports
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.mgmt.advisor import AdvisorManagementClient
from azure.core.exceptions import HttpResponseError

from src.providers.base import CloudProviderInterface


class AzureProvider(CloudProviderInterface):
    """Azure provider implementation."""
    
    def __init__(self):
        self.credential = None
        self.subscription_id = None
        self.compute_client = None
        self.resource_client = None
        self.storage_client = None
        self.monitor_client = None
        self.consumption_client = None
        self.advisor_client = None
        self.authenticated = False
    
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with Azure."""
        try:
            tenant_id = credentials.get('tenant_id')
            client_id = credentials.get('client_id')
            client_secret = credentials.get('client_secret')
            self.subscription_id = credentials.get('subscription_id')
            
            if not all([tenant_id, client_id, client_secret, self.subscription_id]):
                raise ValueError("Missing required credentials for Azure authentication")
            
            # Create credential object
            self.credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            
            # Initialize clients
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
            
            self.advisor_client = AdvisorManagementClient(
                credential=self.credential,
                subscription_id=self.subscription_id
            )
            
            # Test authentication by listing resource groups
            self.resource_client.resource_groups.list()
            
            self.authenticated = True
            return True
        except Exception as e:
            print(f"Azure authentication error: {str(e)}")
            self.authenticated = False
            return False
    
    def get_resources(self, resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get resources from Azure."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        resources = []
        
        if resource_type is None or resource_type == 'virtual_machine':
            # Get virtual machines
            for vm in self.compute_client.virtual_machines.list_all():
                # Get VM details
                resource_group_name = self._extract_resource_group(vm.id)
                vm_details = self.compute_client.virtual_machines.get(
                    resource_group_name=resource_group_name,
                    vm_name=vm.name
                )
                
                # Get VM status
                vm_status = self.compute_client.virtual_machines.instance_view(
                    resource_group_name=resource_group_name,
                    vm_name=vm.name
                )
                
                # Extract status
                status = "unknown"
                for status_code in vm_status.statuses:
                    if status_code.code.startswith("PowerState"):
                        status = status_code.code.split("/")[1]
                        break
                
                # Get tags
                tags = vm_details.tags or {}
                
                resources.append({
                    'id': vm.id,
                    'type': 'virtual_machine',
                    'name': vm.name,
                    'region': vm.location,
                    'status': status,
                    'created_at': None,  # Azure doesn't provide creation time directly
                    'properties': {
                        'vm_size': vm_details.hardware_profile.vm_size,
                        'os_type': vm_details.storage_profile.os_disk.os_type,
                        'admin_username': vm_details.os_profile.admin_username if hasattr(vm_details.os_profile, 'admin_username') else None,
                        'resource_group': resource_group_name
                    },
                    'tags': tags
                })
        
        if resource_type is None or resource_type == 'storage_account':
            # Get storage accounts
            for storage_account in self.storage_client.storage_accounts.list():
                resource_group_name = self._extract_resource_group(storage_account.id)
                
                # Get tags
                tags = storage_account.tags or {}
                
                resources.append({
                    'id': storage_account.id,
                    'type': 'storage_account',
                    'name': storage_account.name,
                    'region': storage_account.location,
                    'status': storage_account.provisioning_state,
                    'created_at': None,  # Azure doesn't provide creation time directly
                    'properties': {
                        'sku': storage_account.sku.name,
                        'kind': storage_account.kind,
                        'access_tier': storage_account.access_tier,
                        'https_only': storage_account.enable_https_traffic_only,
                        'resource_group': resource_group_name
                    },
                    'tags': tags
                })
        
        return resources
    
    def get_resource(self, resource_id: str, resource_type: str) -> Dict[str, Any]:
        """Get a specific resource from Azure."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        if resource_type == 'virtual_machine':
            resource_group_name = self._extract_resource_group(resource_id)
            vm_name = resource_id.split('/')[-1]
            
            # Get VM details
            vm_details = self.compute_client.virtual_machines.get(
                resource_group_name=resource_group_name,
                vm_name=vm_name
            )
            
            # Get VM status
            vm_status = self.compute_client.virtual_machines.instance_view(
                resource_group_name=resource_group_name,
                vm_name=vm_name
            )
            
            # Extract status
            status = "unknown"
            for status_code in vm_status.statuses:
                if status_code.code.startswith("PowerState"):
                    status = status_code.code.split("/")[1]
                    break
            
            # Get tags
            tags = vm_details.tags or {}
            
            return {
                'id': vm_details.id,
                'type': 'virtual_machine',
                'name': vm_details.name,
                'region': vm_details.location,
                'status': status,
                'created_at': None,  # Azure doesn't provide creation time directly
                'properties': {
                    'vm_size': vm_details.hardware_profile.vm_size,
                    'os_type': vm_details.storage_profile.os_disk.os_type,
                    'admin_username': vm_details.os_profile.admin_username if hasattr(vm_details.os_profile, 'admin_username') else None,
                    'resource_group': resource_group_name
                },
                'tags': tags
            }
        
        elif resource_type == 'storage_account':
            resource_group_name = self._extract_resource_group(resource_id)
            storage_account_name = resource_id.split('/')[-1]
            
            # Get storage account details
            storage_account = self.storage_client.storage_accounts.get_properties(
                resource_group_name=resource_group_name,
                account_name=storage_account_name
            )
            
            # Get tags
            tags = storage_account.tags or {}
            
            return {
                'id': storage_account.id,
                'type': 'storage_account',
                'name': storage_account.name,
                'region': storage_account.location,
                'status': storage_account.provisioning_state,
                'created_at': None,  # Azure doesn't provide creation time directly
                'properties': {
                    'sku': storage_account.sku.name,
                    'kind': storage_account.kind,
                    'access_tier': storage_account.access_tier,
                    'https_only': storage_account.enable_https_traffic_only,
                    'resource_group': resource_group_name
                },
                'tags': tags
            }
        
        else:
            raise Exception(f"Unsupported resource type: {resource_type}")
    
    def get_cost_data(self, start_date: str, end_date: str, granularity: str) -> List[Dict[str, Any]]:
        """Get cost data from Azure."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        # Validate granularity
        valid_granularities = ['Daily', 'Monthly']
        if granularity.capitalize() not in valid_granularities:
            granularity = 'Daily'
        
        # Format dates for Azure API
        start_date_obj = datetime.datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date_obj = datetime.datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Get usage details
        usage_details = self.consumption_client.usage_details.list(
            scope=f"/subscriptions/{self.subscription_id}",
            expand="properties/additionalProperties",
            filter=f"properties/usageStart ge '{start_date_obj.strftime('%Y-%m-%d')}' and properties/usageEnd le '{end_date_obj.strftime('%Y-%m-%d')}'",
        )
        
        results = []
        for usage in usage_details:
            # Extract cost data
            service_name = usage.properties.consumed_service or "Unknown"
            amount = float(usage.properties.pretax_cost)
            currency = usage.properties.billing_currency or "USD"
            
            results.append({
                'timestamp': usage.properties.date.strftime('%Y-%m-%d'),
                'service': service_name,
                'amount': amount,
                'currency': currency,
                'granularity': granularity.lower(),
                'resource_id': usage.properties.instance_id,
                'resource_name': usage.properties.instance_name,
                'resource_group': self._extract_resource_group(usage.properties.instance_id) if usage.properties.instance_id else None
            })
        
        return results
    
    def get_metrics(self, resource_id: str, resource_type: str, metric_names: List[str], 
                   start_time: str, end_time: str, period: int) -> Dict[str, Any]:
        """Get metrics for a specific resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        metrics_data = {}
        
        # Convert string dates to datetime objects
        start_datetime = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_datetime = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        # Convert period from seconds to ISO 8601 duration format
        duration = f"PT{period}S"
        
        for metric_name in metric_names:
            try:
                # Get metric data
                metrics = self.monitor_client.metrics.list(
                    resource_uri=resource_id,
                    timespan=f"{start_datetime.isoformat()}/{end_datetime.isoformat()}",
                    interval=duration,
                    metricnames=metric_name,
                    aggregation="Average,Maximum"
                )
                
                datapoints = []
                for metric in metrics.value:
                    for time_series in metric.timeseries:
                        for data in time_series.data:
                            if data.average is not None or data.maximum is not None:
                                datapoints.append({
                                    'timestamp': data.time_stamp.isoformat() if data.time_stamp else None,
                                    'average': data.average,
                                    'maximum': data.maximum,
                                    'unit': metric.unit
                                })
                
                metrics_data[metric_name] = {
                    'datapoints': datapoints,
                    'label': metric_name
                }
            except Exception as e:
                print(f"Error getting metric {metric_name} for resource {resource_id}: {str(e)}")
                metrics_data[metric_name] = {
                    'datapoints': [],
                    'label': metric_name,
                    'error': str(e)
                }
        
        return metrics_data
    
    def execute_action(self, action_type: str, resource_id: str, resource_type: str, 
                      parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on a resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        result = {
            'action_type': action_type,
            'resource_id': resource_id,
            'resource_type': resource_type,
            'success': False,
            'message': '',
            'details': {}
        }
        
        try:
            # Virtual Machine Actions
            if resource_type == 'virtual_machine':
                resource_group_name = self._extract_resource_group(resource_id)
                vm_name = resource_id.split('/')[-1]
                
                if action_type == 'start_vm':
                    # Start VM
                    self.compute_client.virtual_machines.begin_start(
                        resource_group_name=resource_group_name,
                        vm_name=vm_name
                    ).wait()
                    
                    result['success'] = True
                    result['message'] = f"Started virtual machine {vm_name}"
                
                elif action_type == 'stop_vm':
                    # Stop VM
                    deallocate = parameters.get('deallocate', True)
                    
                    if deallocate:
                        self.compute_client.virtual_machines.begin_deallocate(
                            resource_group_name=resource_group_name,
                            vm_name=vm_name
                        ).wait()
                        result['message'] = f"Stopped and deallocated virtual machine {vm_name}"
                    else:
                        self.compute_client.virtual_machines.begin_power_off(
                            resource_group_name=resource_group_name,
                            vm_name=vm_name
                        ).wait()
                        result['message'] = f"Stopped virtual machine {vm_name} without deallocation"
                    
                    result['success'] = True
                    result['details'] = {'deallocated': deallocate}
                
                elif action_type == 'resize_vm':
                    # Resize VM
                    vm_size = parameters.get('vm_size')
                    if not vm_size:
                        raise ValueError("vm_size parameter is required")
                    
                    # Get current VM
                    vm = self.compute_client.virtual_machines.get(
                        resource_group_name=resource_group_name,
                        vm_name=vm_name
                    )
                    
                    # Update VM size
                    vm.hardware_profile.vm_size = vm_size
                    
                    # Update VM
                    self.compute_client.virtual_machines.begin_update(
                        resource_group_name=resource_group_name,
                        vm_name=vm_name,
                        parameters=vm
                    ).wait()
                    
                    result['success'] = True
                    result['message'] = f"Resized virtual machine {vm_name} to {vm_size}"
                    result['details'] = {'new_vm_size': vm_size}
                
                elif action_type == 'delete_vm':
                    # Delete VM
                    self.compute_client.virtual_machines.begin_delete(
                        resource_group_name=resource_group_name,
                        vm_name=vm_name
                    ).wait()
                    
                    result['success'] = True
                    result['message'] = f"Deleted virtual machine {vm_name}"
            
            # Storage Account Actions
            elif resource_type == 'storage_account':
                resource_group_name = self._extract_resource_group(resource_id)
                storage_account_name = resource_id.split('/')[-1]
                
                if action_type == 'update_tier':
                    # Update storage account tier
                    access_tier = parameters.get('access_tier')
                    if not access_tier:
                        raise ValueError("access_tier parameter is required")
                    
                    # Get current storage account
                    storage_account = self.storage_client.storage_accounts.get_properties(
                        resource_group_name=resource_group_name,
                        account_name=storage_account_name
                    )
                    
                    # Update access tier
                    storage_account.access_tier = access_tier
                    
                    # Update storage account
                    self.storage_client.storage_accounts.update(
                        resource_group_name=resource_group_name,
                        account_name=storage_account_name,
                        parameters=storage_account
                    )
                    
                    result['success'] = True
                    result['message'] = f"Updated storage account {storage_account_name} tier to {access_tier}"
                    result['details'] = {'new_access_tier': access_tier}
                
                elif action_type == 'delete_storage_account':
                    # Delete storage account
                    self.storage_client.storage_accounts.delete(
                        resource_group_name=resource_group_name,
                        account_name=storage_account_name
                    )
                    
                    result['success'] = True
                    result['message'] = f"Deleted storage account {storage_account_name}"
            
            else:
                result['message'] = f"Unsupported resource type: {resource_type}"
        
        except Exception as e:
            result['message'] = str(e)
        
        return result
    
    def tag_resource(self, resource_id: str, resource_type: str, tags: Dict[str, str]) -> bool:
        """Tag a resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        try:
            # Get current resource
            resource = self.resource_client.resources.get_by_id(
                resource_id=resource_id,
                api_version="2021-04-01"
            )
            
            # Update tags
            current_tags = resource.tags or {}
            current_tags.update(tags)
            
            # Apply tags
            self.resource_client.resources.begin_update_by_id(
                resource_id=resource_id,
                api_version="2021-04-01",
                parameters={'tags': current_tags}
            ).wait()
            
            return True
        
        except Exception as e:
            print(f"Error tagging resource: {str(e)}")
            return False
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get cost optimization recommendations from Azure Advisor."""
        if not self.authenticated:
            raise Exception("Not authenticated with Azure")
        
        recommendations = []
        
        try:
            # Get recommendations from Azure Advisor
            advisor_recommendations = self.advisor_client.recommendations.list()
            
            for rec in advisor_recommendations:
                # Filter for cost recommendations
                if rec.category == 'Cost':
                    # Extract resource details
                    resource_id = rec.impacted_resource
                    resource_type = resource_id.split('/')[-2] if resource_id else 'unknown'
                    resource_name = resource_id.split('/')[-1] if resource_id else 'unknown'
                    
                    # Extract savings information
                    savings = 0.0
                    savings_currency = 'USD'
                    
                    if rec.extended_properties and 'savingsAmount' in rec.extended_properties:
                        try:
                            savings = float(rec.extended_properties['savingsAmount'])
                        except (ValueError, TypeError):
                            pass
                    
                    if rec.extended_properties and 'savingsCurrency' in rec.extended_properties:
                        savings_currency = rec.extended_properties['savingsCurrency']
                    
                    recommendations.append({
                        'id': rec.id,
                        'type': 'azure_advisor',
                        'resource_type': resource_type,
                        'resource_id': resource_id,
                        'description': rec.short_description.solution if rec.short_description else '',
                        'estimated_savings': savings,
                        'savings_currency': savings_currency,
                        'savings_period': 'monthly',
                        'details': {
                            'impact': rec.impact,
                            'problem': rec.short_description.problem if rec.short_description else '',
                            'recommendation_type_id': rec.recommendation_type_id,
                            'last_updated': rec.last_updated.isoformat() if rec.last_updated else None
                        }
                    })
        
        except Exception as e:
            print(f"Error getting Azure recommendations: {str(e)}")
        
        return recommendations
    
    # Helper methods
    
    def _extract_resource_group(self, resource_id: str) -> str:
        """Extract resource group name from resource ID."""
        if not resource_id:
            return ""
        
        parts = resource_id.split('/')
        for i, part in enumerate(parts):
            if part.lower() == 'resourcegroups' and i + 1 < len(parts):
                return parts[i + 1]
        
        return ""
