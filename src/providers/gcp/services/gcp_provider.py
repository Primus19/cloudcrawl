"""
Google Cloud Platform provider implementation for cloud cost optimizer.
"""
import datetime
from typing import Dict, List, Any, Optional
from uuid import UUID

# GCP SDK imports
from google.oauth2 import service_account
from google.cloud import compute_v1
from google.cloud import storage
from google.cloud import monitoring_v3
from google.cloud import billing_v1
from google.cloud import recommender_v1

from src.providers.base import CloudProviderInterface


class GCPProvider(CloudProviderInterface):
    """GCP provider implementation."""
    
    def __init__(self):
        self.credentials = None
        self.project_id = None
        self.compute_client = None
        self.storage_client = None
        self.monitoring_client = None
        self.billing_client = None
        self.recommender_client = None
        self.authenticated = False
    
    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with GCP."""
        try:
            # Check authentication method
            if 'service_account_json' in credentials:
                # Use service account JSON
                self.credentials = service_account.Credentials.from_service_account_info(
                    credentials['service_account_json']
                )
            elif 'service_account_file' in credentials:
                # Use service account file
                self.credentials = service_account.Credentials.from_service_account_file(
                    credentials['service_account_file']
                )
            else:
                raise ValueError("Missing required credentials for GCP authentication")
            
            self.project_id = credentials.get('project_id')
            if not self.project_id:
                raise ValueError("project_id is required for GCP authentication")
            
            # Initialize clients
            self.compute_client = compute_v1.InstancesClient(credentials=self.credentials)
            self.storage_client = storage.Client(credentials=self.credentials, project=self.project_id)
            self.monitoring_client = monitoring_v3.MetricServiceClient(credentials=self.credentials)
            self.billing_client = billing_v1.CloudBillingClient(credentials=self.credentials)
            self.recommender_client = recommender_v1.RecommenderClient(credentials=self.credentials)
            
            # Test authentication by listing zones
            compute_v1.ZonesClient(credentials=self.credentials).list(project=self.project_id)
            
            self.authenticated = True
            return True
        except Exception as e:
            print(f"GCP authentication error: {str(e)}")
            self.authenticated = False
            return False
    
    def get_resources(self, resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get resources from GCP."""
        if not self.authenticated:
            raise Exception("Not authenticated with GCP")
        
        resources = []
        
        if resource_type is None or resource_type == 'compute_instance':
            # Get compute instances from all zones
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            zones = zones_client.list(project=self.project_id)
            
            for zone in zones:
                zone_name = zone.name
                
                # List instances in this zone
                request = compute_v1.ListInstancesRequest(
                    project=self.project_id,
                    zone=zone_name
                )
                
                instances = self.compute_client.list(request=request)
                
                for instance in instances:
                    # Extract status
                    status = instance.status.lower()
                    
                    # Extract creation timestamp
                    created_at = None
                    if instance.creation_timestamp:
                        created_at = instance.creation_timestamp
                    
                    # Extract tags
                    tags = {}
                    if instance.labels:
                        tags = dict(instance.labels)
                    
                    # Extract network interfaces
                    network_interfaces = []
                    for nic in instance.network_interfaces:
                        interface = {
                            'network': nic.network.split('/')[-1],
                            'subnet': nic.subnetwork.split('/')[-1] if nic.subnetwork else None,
                            'internal_ip': nic.network_i_p,
                            'external_ips': []
                        }
                        
                        # Extract external IPs
                        for access_config in nic.access_configs:
                            if access_config.nat_i_p:
                                interface['external_ips'].append(access_config.nat_i_p)
                        
                        network_interfaces.append(interface)
                    
                    resources.append({
                        'id': instance.id,
                        'type': 'compute_instance',
                        'name': instance.name,
                        'region': zone_name[:-2],  # Remove the zone letter suffix to get region
                        'zone': zone_name,
                        'status': status,
                        'created_at': created_at,
                        'properties': {
                            'machine_type': instance.machine_type.split('/')[-1],
                            'cpu_platform': instance.cpu_platform,
                            'network_interfaces': network_interfaces,
                            'disks': [{'name': disk.device_name, 'size_gb': disk.disk_size_gb} for disk in instance.disks]
                        },
                        'tags': tags
                    })
        
        if resource_type is None or resource_type == 'storage_bucket':
            # Get storage buckets
            buckets = self.storage_client.list_buckets()
            
            for bucket in buckets:
                # Extract creation timestamp
                created_at = None
                if bucket.time_created:
                    created_at = bucket.time_created.isoformat()
                
                # Extract labels
                labels = bucket.labels or {}
                
                resources.append({
                    'id': bucket.name,
                    'type': 'storage_bucket',
                    'name': bucket.name,
                    'region': bucket.location.lower(),
                    'status': 'available',
                    'created_at': created_at,
                    'properties': {
                        'storage_class': bucket.storage_class,
                        'location_type': bucket.location_type,
                        'versioning_enabled': bucket.versioning_enabled
                    },
                    'tags': labels
                })
        
        return resources
    
    def get_resource(self, resource_id: str, resource_type: str) -> Dict[str, Any]:
        """Get a specific resource from GCP."""
        if not self.authenticated:
            raise Exception("Not authenticated with GCP")
        
        if resource_type == 'compute_instance':
            # For compute instances, we need to know the zone
            # First, search in all zones
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            zones = zones_client.list(project=self.project_id)
            
            for zone in zones:
                zone_name = zone.name
                
                try:
                    # Try to get instance in this zone
                    request = compute_v1.GetInstanceRequest(
                        project=self.project_id,
                        zone=zone_name,
                        instance=resource_id
                    )
                    
                    instance = self.compute_client.get(request=request)
                    
                    # Extract status
                    status = instance.status.lower()
                    
                    # Extract creation timestamp
                    created_at = None
                    if instance.creation_timestamp:
                        created_at = instance.creation_timestamp
                    
                    # Extract tags
                    tags = {}
                    if instance.labels:
                        tags = dict(instance.labels)
                    
                    # Extract network interfaces
                    network_interfaces = []
                    for nic in instance.network_interfaces:
                        interface = {
                            'network': nic.network.split('/')[-1],
                            'subnet': nic.subnetwork.split('/')[-1] if nic.subnetwork else None,
                            'internal_ip': nic.network_i_p,
                            'external_ips': []
                        }
                        
                        # Extract external IPs
                        for access_config in nic.access_configs:
                            if access_config.nat_i_p:
                                interface['external_ips'].append(access_config.nat_i_p)
                        
                        network_interfaces.append(interface)
                    
                    return {
                        'id': instance.id,
                        'type': 'compute_instance',
                        'name': instance.name,
                        'region': zone_name[:-2],  # Remove the zone letter suffix to get region
                        'zone': zone_name,
                        'status': status,
                        'created_at': created_at,
                        'properties': {
                            'machine_type': instance.machine_type.split('/')[-1],
                            'cpu_platform': instance.cpu_platform,
                            'network_interfaces': network_interfaces,
                            'disks': [{'name': disk.device_name, 'size_gb': disk.disk_size_gb} for disk in instance.disks]
                        },
                        'tags': tags
                    }
                except Exception:
                    # Instance not found in this zone, continue to next zone
                    continue
            
            # If we get here, the instance was not found in any zone
            raise Exception(f"Compute instance {resource_id} not found in project {self.project_id}")
        
        elif resource_type == 'storage_bucket':
            try:
                # Get bucket
                bucket = self.storage_client.get_bucket(resource_id)
                
                # Extract creation timestamp
                created_at = None
                if bucket.time_created:
                    created_at = bucket.time_created.isoformat()
                
                # Extract labels
                labels = bucket.labels or {}
                
                return {
                    'id': bucket.name,
                    'type': 'storage_bucket',
                    'name': bucket.name,
                    'region': bucket.location.lower(),
                    'status': 'available',
                    'created_at': created_at,
                    'properties': {
                        'storage_class': bucket.storage_class,
                        'location_type': bucket.location_type,
                        'versioning_enabled': bucket.versioning_enabled
                    },
                    'tags': labels
                }
            except Exception as e:
                raise Exception(f"Storage bucket {resource_id} not found: {str(e)}")
        
        else:
            raise Exception(f"Unsupported resource type: {resource_type}")
    
    def get_cost_data(self, start_date: str, end_date: str, granularity: str) -> List[Dict[str, Any]]:
        """Get cost data from GCP."""
        if not self.authenticated:
            raise Exception("Not authenticated with GCP")
        
        # Note: This is a simplified implementation
        # In a real implementation, you would use the Cloud Billing API
        # to get detailed cost data
        
        # For this example, we'll return a placeholder
        # In a real implementation, you would:
        # 1. Get the billing account associated with the project
        # 2. Query the billing export in BigQuery or use the Billing API
        
        # Find billing account for the project
        try:
            billing_info = self.billing_client.get_project_billing_info(
                name=f"projects/{self.project_id}"
            )
            
            billing_account = billing_info.billing_account_name
            
            if not billing_account:
                return []
            
            # In a real implementation, you would query the billing data
            # This is a placeholder for demonstration purposes
            return [
                {
                    'timestamp': start_date,
                    'service': 'Compute Engine',
                    'amount': 100.0,
                    'currency': 'USD',
                    'granularity': granularity.lower()
                },
                {
                    'timestamp': start_date,
                    'service': 'Cloud Storage',
                    'amount': 50.0,
                    'currency': 'USD',
                    'granularity': granularity.lower()
                }
            ]
        
        except Exception as e:
            print(f"Error getting GCP cost data: {str(e)}")
            return []
    
    def get_metrics(self, resource_id: str, resource_type: str, metric_names: List[str], 
                   start_time: str, end_time: str, period: int) -> Dict[str, Any]:
        """Get metrics for a specific resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with GCP")
        
        metrics_data = {}
        
        # Convert string dates to datetime objects
        start_datetime = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_datetime = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        # Convert to timestamps
        start_seconds = int(start_datetime.timestamp())
        end_seconds = int(end_datetime.timestamp())
        
        if resource_type == 'compute_instance':
            # For compute instances, we need to find the zone first
            instance_info = self.get_resource(resource_id, 'compute_instance')
            zone = instance_info['zone']
            
            for metric_name in metric_names:
                # Map to GCP metric name
                gcp_metric = self._map_to_gcp_metric(metric_name, resource_type)
                
                if not gcp_metric:
                    metrics_data[metric_name] = {
                        'datapoints': [],
                        'label': metric_name,
                        'error': f"Unsupported metric: {metric_name}"
                    }
                    continue
                
                try:
                    # Create time interval
                    interval = monitoring_v3.TimeInterval(
                        start_time={"seconds": start_seconds},
                        end_time={"seconds": end_seconds}
                    )
                    
                    # Create metric
                    metric_type = f"compute.googleapis.com/{gcp_metric}"
                    
                    # Create filter
                    filter_str = (
                        f'metric.type="{metric_type}" AND '
                        f'resource.type="gce_instance" AND '
                        f'resource.labels.instance_id="{resource_id}" AND '
                        f'resource.labels.zone="{zone}"'
                    )
                    
                    # Query metrics
                    results = self.monitoring_client.list_time_series(
                        request={
                            "name": f"projects/{self.project_id}",
                            "filter": filter_str,
                            "interval": interval,
                            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                            "aggregation": {
                                "alignment_period": {"seconds": period},
                                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                                "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
                            }
                        }
                    )
                    
                    # Process results
                    datapoints = []
                    for time_series in results:
                        for point in time_series.points:
                            timestamp = datetime.datetime.fromtimestamp(
                                point.interval.start_time.seconds
                            ).isoformat()
                            
                            value = None
                            if hasattr(point.value, 'double_value'):
                                value = point.value.double_value
                            elif hasattr(point.value, 'int64_value'):
                                value = point.value.int64_value
                            
                            if value is not None:
                                datapoints.append({
                                    'timestamp': timestamp,
                                    'average': value,
                                    'maximum': value,  # GCP doesn't provide max directly in this API
                                    'unit': time_series.metric.unit
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
            raise Exception("Not authenticated with GCP")
        
        result = {
            'action_type': action_type,
            'resource_id': resource_id,
            'resource_type': resource_type,
            'success': False,
            'message': '',
            'details': {}
        }
        
        try:
            # Compute Instance Actions
            if resource_type == 'compute_instance':
                # For compute instances, we need to find the zone first
                instance_info = self.get_resource(resource_id, 'compute_instance')
                zone = instance_info['zone']
                instance_name = instance_info['name']
                
                # Create instance client for operations
                instances_client = compute_v1.InstancesClient(credentials=self.credentials)
                
                if action_type == 'start_instance':
                    # Start instance
                    operation = instances_client.start(
                        project=self.project_id,
                        zone=zone,
                        instance=instance_name
                    )
                    
                    # Wait for operation to complete
                    operation_client = compute_v1.ZoneOperationsClient(credentials=self.credentials)
                    operation_client.wait(
                        operation=operation.name,
                        project=self.project_id,
                        zone=zone
                    )
                    
                    result['success'] = True
                    result['message'] = f"Started compute instance {instance_name}"
                
                elif action_type == 'stop_instance':
                    # Stop instance
                    operation = instances_client.stop(
                        project=self.project_id,
                        zone=zone,
                        instance=instance_name
                    )
                    
                    # Wait for operation to complete
                    operation_client = compute_v1.ZoneOperationsClient(credentials=self.credentials)
                    operation_client.wait(
                        operation=operation.name,
                        project=self.project_id,
                        zone=zone
                    )
                    
                    result['success'] = True
                    result['message'] = f"Stopped compute instance {instance_name}"
                
                elif action_type == 'resize_instance':
                    # Resize instance
                    machine_type = parameters.get('machine_type')
                    if not machine_type:
                        raise ValueError("machine_type parameter is required")
                    
                    # Check if instance is running
                    if instance_info['status'] == 'running':
                        # Stop instance first
                        stop_operation = instances_client.stop(
                            project=self.project_id,
                            zone=zone,
                            instance=instance_name
                        )
                        
                        # Wait for stop operation to complete
                        operation_client = compute_v1.ZoneOperationsClient(credentials=self.credentials)
                        operation_client.wait(
                            operation=stop_operation.name,
                            project=self.project_id,
                            zone=zone
                        )
                    
                    # Set machine type
                    machine_type_url = f"projects/{self.project_id}/zones/{zone}/machineTypes/{machine_type}"
                    
                    # Create set machine type request
                    request = compute_v1.SetMachineTypeInstanceRequest(
                        project=self.project_id,
                        zone=zone,
                        instance=instance_name,
                        instance_set_machine_type_request_resource=compute_v1.InstancesSetMachineTypeRequest(
                            machine_type=machine_type_url
                        )
                    )
                    
                    # Execute resize
                    operation = instances_client.set_machine_type(request=request)
                    
                    # Wait for operation to complete
                    operation_client = compute_v1.ZoneOperationsClient(credentials=self.credentials)
                    operation_client.wait(
                        operation=operation.name,
                        project=self.project_id,
                        zone=zone
                    )
                    
                    # Start instance if it was running before
                    if instance_info['status'] == 'running':
                        start_operation = instances_client.start(
                            project=self.project_id,
                            zone=zone,
                            instance=instance_name
                        )
                        
                        # Wait for start operation to complete
                        operation_client.wait(
                            operation=start_operation.name,
                            project=self.project_id,
                            zone=zone
                        )
                    
                    result['success'] = True
                    result['message'] = f"Resized compute instance {instance_name} to {machine_type}"
                    result['details'] = {'new_machine_type': machine_type}
                
                elif action_type == 'delete_instance':
                    # Delete instance
                    operation = instances_client.delete(
                        project=self.project_id,
                        zone=zone,
                        instance=instance_name
                    )
                    
                    # Wait for operation to complete
                    operation_client = compute_v1.ZoneOperationsClient(credentials=self.credentials)
                    operation_client.wait(
                        operation=operation.name,
                        project=self.project_id,
                        zone=zone
                    )
                    
                    result['success'] = True
                    result['message'] = f"Deleted compute instance {instance_name}"
            
            # Storage Bucket Actions
            elif resource_type == 'storage_bucket':
                bucket_name = resource_id
                
                if action_type == 'delete_bucket':
                    # Check if bucket is empty
                    force_empty = parameters.get('force_empty', False)
                    
                    bucket = self.storage_client.get_bucket(bucket_name)
                    
                    if force_empty:
                        # Delete all objects
                        blobs = bucket.list_blobs()
                        for blob in blobs:
                            blob.delete()
                    
                    # Delete bucket
                    bucket.delete()
                    
                    result['success'] = True
                    result['message'] = f"Deleted storage bucket {bucket_name}"
                    result['details'] = {'force_empty': force_empty}
                
                elif action_type == 'update_storage_class':
                    # Update storage class
                    storage_class = parameters.get('storage_class')
                    if not storage_class:
                        raise ValueError("storage_class parameter is required")
                    
                    bucket = self.storage_client.get_bucket(bucket_name)
                    bucket.storage_class = storage_class
                    bucket.patch()
                    
                    result['success'] = True
                    result['message'] = f"Updated storage class for bucket {bucket_name} to {storage_class}"
                    result['details'] = {'new_storage_class': storage_class}
            
            else:
                result['message'] = f"Unsupported resource type: {resource_type}"
        
        except Exception as e:
            result['message'] = str(e)
        
        return result
    
    def tag_resource(self, resource_id: str, resource_type: str, tags: Dict[str, str]) -> bool:
        """Tag a resource."""
        if not self.authenticated:
            raise Exception("Not authenticated with GCP")
        
        try:
            if resource_type == 'compute_instance':
                # For compute instances, we need to find the zone first
                instance_info = self.get_resource(resource_id, 'compute_instance')
                zone = instance_info['zone']
                instance_name = instance_info['name']
                
                # Get current instance
                request = compute_v1.GetInstanceRequest(
                    project=self.project_id,
                    zone=zone,
                    instance=instance_name
                )
                
                instance = self.compute_client.get(request=request)
                
                # Update labels
                current_labels = dict(instance.labels) if instance.labels else {}
                current_labels.update(tags)
                
                # Create set labels request
                set_labels_request = compute_v1.InstancesSetLabelsRequest(
                    labels=current_labels,
                    label_fingerprint=instance.label_fingerprint
                )
                
                # Execute set labels
                operation = self.compute_client.set_labels(
                    project=self.project_id,
                    zone=zone,
                    instance=instance_name,
                    instances_set_labels_request_resource=set_labels_request
                )
                
                # Wait for operation to complete
                operation_client = compute_v1.ZoneOperationsClient(credentials=self.credentials)
                operation_client.wait(
                    operation=operation.name,
                    project=self.project_id,
                    zone=zone
                )
                
                return True
            
            elif resource_type == 'storage_bucket':
                bucket_name = resource_id
                
                # Get bucket
                bucket = self.storage_client.get_bucket(bucket_name)
                
                # Update labels
                current_labels = bucket.labels or {}
                current_labels.update(tags)
                bucket.labels = current_labels
                
                # Save changes
                bucket.patch()
                
                return True
            
            else:
                return False
        
        except Exception as e:
            print(f"Error tagging resource: {str(e)}")
            return False
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get cost optimization recommendations from GCP."""
        if not self.authenticated:
            raise Exception("Not authenticated with GCP")
        
        recommendations = []
        
        try:
            # Get recommendations for all zones
            zones_client = compute_v1.ZonesClient(credentials=self.credentials)
            zones = zones_client.list(project=self.project_id)
            
            for zone in zones:
                zone_name = zone.name
                
                # Get parent name for recommender
                parent = f"projects/{self.project_id}/locations/{zone_name}/recommenders/google.compute.instance.MachineTypeRecommender"
                
                try:
                    # Get recommendations
                    recommendations_list = self.recommender_client.list_recommendations(parent=parent)
                    
                    for rec in recommendations_list:
                        # Extract resource details
                        resource_id = None
                        for target in rec.content.operation_groups[0].operations:
                            if target.resource:
                                resource_id = target.resource
                                break
                        
                        # Extract savings information
                        savings = 0.0
                        savings_currency = 'USD'
                        
                        for impact in rec.primary_impact.cost_projection.cost.cost_micros:
                            savings += abs(impact.units + (impact.nanos / 1e9))
                            savings_currency = impact.currency_code
                        
                        recommendations.append({
                            'id': rec.name,
                            'type': 'machine_type',
                            'resource_type': 'compute_instance',
                            'resource_id': resource_id,
                            'description': rec.description,
                            'estimated_savings': savings,
                            'savings_currency': savings_currency,
                            'savings_period': 'monthly',
                            'details': {
                                'state': rec.state_info.state,
                                'last_refresh_time': rec.last_refresh_time.isoformat() if rec.last_refresh_time else None,
                                'priority': rec.priority
                            }
                        })
                
                except Exception as e:
                    print(f"Error getting recommendations for zone {zone_name}: {str(e)}")
        
        except Exception as e:
            print(f"Error getting GCP recommendations: {str(e)}")
        
        return recommendations
    
    # Helper methods
    
    def _map_to_gcp_metric(self, metric_name: str, resource_type: str) -> Optional[str]:
        """Map generic metric name to GCP-specific metric name."""
        if resource_type == 'compute_instance':
            metric_mapping = {
                'cpu_utilization': 'instance/cpu/utilization',
                'memory_utilization': 'instance/memory/percent_used',
                'disk_read_ops': 'instance/disk/read_ops_count',
                'disk_write_ops': 'instance/disk/write_ops_count',
                'network_in': 'instance/network/received_bytes_count',
                'network_out': 'instance/network/sent_bytes_count'
            }
            
            return metric_mapping.get(metric_name.lower())
        
        return None
