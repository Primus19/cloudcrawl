"""
Recommendation engine for cloud cost optimization.
"""
from typing import Dict, List, Any, Optional
from uuid import UUID
import datetime
from decimal import Decimal

from src.core.services.resource_service import ResourceService
from src.core.services.cost_service import CostService
from src.core.services.automation_service import AutomationService
from src.providers.base import CloudProviderInterface


class RecommendationEngine:
    """Engine for generating cost optimization recommendations."""
    
    def __init__(self, 
                 resource_service: ResourceService,
                 cost_service: CostService,
                 automation_service: AutomationService):
        self.resource_service = resource_service
        self.cost_service = cost_service
        self.automation_service = automation_service
    
    def generate_recommendations(self, cloud_account_id: UUID, provider: CloudProviderInterface) -> List[Dict[str, Any]]:
        """Generate recommendations for a cloud account."""
        recommendations = []
        
        # Get provider-specific recommendations
        try:
            provider_recommendations = provider.get_recommendations()
            
            # Process and store provider recommendations
            for rec in provider_recommendations:
                # Map provider recommendation to our model
                recommendation_type = self._map_recommendation_type(rec['type'])
                priority = self._determine_priority(rec)
                
                # Create recommendation
                recommendation = self.automation_service.create_recommendation(
                    cloud_account_id=cloud_account_id,
                    recommendation_type=recommendation_type,
                    priority=priority,
                    estimated_savings=Decimal(str(rec['estimated_savings'])) if 'estimated_savings' in rec else None,
                    savings_currency=rec.get('savings_currency'),
                    savings_period=rec.get('savings_period', 'monthly'),
                    resource_id=UUID(rec['resource_id']) if 'resource_id' in rec and rec['resource_id'] else None,
                    details={
                        'provider_recommendation_id': rec.get('id'),
                        'description': rec.get('description'),
                        'provider_type': rec.get('type'),
                        'provider_details': rec.get('details', {})
                    }
                )
                
                recommendations.append(recommendation)
        except Exception as e:
            print(f"Error getting provider recommendations: {str(e)}")
        
        # Generate custom recommendations
        custom_recommendations = self._generate_custom_recommendations(cloud_account_id, provider)
        recommendations.extend(custom_recommendations)
        
        return recommendations
    
    def _generate_custom_recommendations(self, cloud_account_id: UUID, provider: CloudProviderInterface) -> List[Dict[str, Any]]:
        """Generate custom recommendations beyond what the provider offers."""
        custom_recommendations = []
        
        # Get resources for the account
        resources = self.resource_service.get_resources_by_cloud_account(cloud_account_id)
        
        # Check for idle resources
        idle_resources = self._identify_idle_resources(cloud_account_id, resources, provider)
        for resource in idle_resources:
            # Create recommendation for idle resource
            recommendation = self.automation_service.create_recommendation(
                cloud_account_id=cloud_account_id,
                recommendation_type='idle_resource',
                priority='medium',
                estimated_savings=resource['estimated_savings'],
                savings_currency=resource['savings_currency'],
                savings_period='monthly',
                resource_id=resource['resource_id'],
                details={
                    'description': f"Idle {resource['resource_type']} detected: {resource['resource_name']}",
                    'metrics': resource['metrics'],
                    'suggested_action': resource['suggested_action']
                }
            )
            
            custom_recommendations.append(recommendation)
        
        # Check for resources without tags
        untagged_resources = self._identify_untagged_resources(resources)
        for resource in untagged_resources:
            # Create recommendation for untagged resource
            recommendation = self.automation_service.create_recommendation(
                cloud_account_id=cloud_account_id,
                recommendation_type='missing_tags',
                priority='low',
                resource_id=resource['id'],
                details={
                    'description': f"Missing required tags on {resource['type']}: {resource['name']}",
                    'suggested_tags': ['Environment', 'Owner', 'CostCenter', 'Project']
                }
            )
            
            custom_recommendations.append(recommendation)
        
        # Check for cost anomalies
        cost_anomalies = self._identify_cost_anomalies(cloud_account_id)
        for anomaly in cost_anomalies:
            # Create recommendation for cost anomaly
            recommendation = self.automation_service.create_recommendation(
                cloud_account_id=cloud_account_id,
                recommendation_type='cost_anomaly',
                priority='high',
                estimated_savings=anomaly['estimated_savings'],
                savings_currency=anomaly['currency'],
                savings_period='monthly',
                resource_id=anomaly.get('resource_id'),
                details={
                    'description': anomaly['description'],
                    'anomaly_details': anomaly['details']
                }
            )
            
            custom_recommendations.append(recommendation)
        
        return custom_recommendations
    
    def _identify_idle_resources(self, cloud_account_id: UUID, resources: List[Any], provider: CloudProviderInterface) -> List[Dict[str, Any]]:
        """Identify idle resources based on metrics."""
        idle_resources = []
        
        # Get current date and 7 days ago for metrics
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=7)
        
        for resource in resources:
            # Skip resources that are already stopped
            if resource.status in ['stopped', 'deallocated', 'terminated']:
                continue
            
            # Check metrics based on resource type
            if resource.resource_type == 'ec2_instance' or resource.resource_type == 'virtual_machine' or resource.resource_type == 'compute_instance':
                # Get CPU utilization metrics
                metrics = provider.get_metrics(
                    resource_id=resource.resource_id,
                    resource_type=resource.resource_type,
                    metric_names=['cpu_utilization'],
                    start_time=start_time.isoformat(),
                    end_time=end_time.isoformat(),
                    period=3600  # 1 hour
                )
                
                # Check if CPU utilization is consistently low
                if 'cpu_utilization' in metrics and metrics['cpu_utilization']['datapoints']:
                    avg_utilization = sum(point.get('average', 0) for point in metrics['cpu_utilization']['datapoints']) / len(metrics['cpu_utilization']['datapoints'])
                    
                    if avg_utilization < 0.05:  # Less than 5% CPU utilization
                        # Estimate savings
                        estimated_savings = self._estimate_resource_cost(resource)
                        
                        idle_resources.append({
                            'resource_id': resource.id,
                            'resource_type': resource.resource_type,
                            'resource_name': resource.name,
                            'estimated_savings': estimated_savings,
                            'savings_currency': 'USD',
                            'metrics': {
                                'avg_cpu_utilization': avg_utilization
                            },
                            'suggested_action': 'stop_instance' if resource.resource_type == 'ec2_instance' else 'stop_vm'
                        })
        
        return idle_resources
    
    def _identify_untagged_resources(self, resources: List[Any]) -> List[Dict[str, Any]]:
        """Identify resources missing required tags."""
        untagged_resources = []
        required_tags = ['Environment', 'Owner', 'CostCenter', 'Project']
        
        for resource in resources:
            # Check if resource has all required tags
            missing_tags = [tag for tag in required_tags if tag not in resource.tags]
            
            if missing_tags:
                untagged_resources.append({
                    'id': resource.id,
                    'type': resource.resource_type,
                    'name': resource.name,
                    'missing_tags': missing_tags
                })
        
        return untagged_resources
    
    def _identify_cost_anomalies(self, cloud_account_id: UUID) -> List[Dict[str, Any]]:
        """Identify cost anomalies."""
        anomalies = []
        
        # Get current date and previous month
        end_date = datetime.date.today()
        start_date = end_date.replace(day=1) - datetime.timedelta(days=1)  # Last day of previous month
        start_date = start_date.replace(day=1)  # First day of previous month
        
        # Get cost data for previous month
        costs = self.cost_service.get_cost_data_by_account(
            cloud_account_id=cloud_account_id,
            start_date=datetime.datetime.combine(start_date, datetime.time.min),
            end_date=datetime.datetime.combine(end_date, datetime.time.min),
            granularity='daily'
        )
        
        # Group costs by day
        daily_costs = {}
        for cost in costs:
            day = cost.timestamp.date()
            if day not in daily_costs:
                daily_costs[day] = Decimal('0')
            daily_costs[day] += cost.amount
        
        # Calculate average daily cost
        if daily_costs:
            avg_daily_cost = sum(daily_costs.values()) / len(daily_costs)
            
            # Check for days with significant cost increase
            for day, cost in daily_costs.items():
                if cost > avg_daily_cost * Decimal('1.5'):  # 50% higher than average
                    anomalies.append({
                        'description': f"Cost spike detected on {day.isoformat()}",
                        'estimated_savings': (cost - avg_daily_cost) * Decimal('30'),  # Estimate monthly savings
                        'currency': costs[0].currency if costs else 'USD',
                        'details': {
                            'date': day.isoformat(),
                            'cost': float(cost),
                            'average_cost': float(avg_daily_cost),
                            'percent_increase': float((cost / avg_daily_cost - Decimal('1')) * Decimal('100'))
                        }
                    })
        
        return anomalies
    
    def _map_recommendation_type(self, provider_type: str) -> str:
        """Map provider-specific recommendation type to our standard types."""
        mapping = {
            'rightsizing': 'resize_resource',
            'reservation': 'purchase_reservation',
            'idle': 'idle_resource',
            'machine_type': 'resize_resource',
            'azure_advisor': 'general_optimization'
        }
        
        return mapping.get(provider_type.lower(), 'general_optimization')
    
    def _determine_priority(self, recommendation: Dict[str, Any]) -> str:
        """Determine recommendation priority based on savings and other factors."""
        # Default to medium priority
        priority = 'medium'
        
        # Check if savings information is available
        if 'estimated_savings' in recommendation:
            savings = recommendation['estimated_savings']
            
            # High priority for significant savings
            if savings > 100:
                priority = 'high'
            # Low priority for minimal savings
            elif savings < 10:
                priority = 'low'
        
        # Override based on recommendation type
        if recommendation.get('type') == 'idle':
            priority = 'high'  # Idle resources are always high priority
        
        return priority
    
    def _estimate_resource_cost(self, resource: Any) -> Decimal:
        """Estimate monthly cost of a resource."""
        # This is a simplified implementation
        # In a real implementation, this would use pricing data
        
        if resource.resource_type == 'ec2_instance':
            # Simplified EC2 pricing
            instance_type = resource.properties.get('instance_type', 't3.micro')
            
            pricing = {
                't3.micro': Decimal('8.50'),
                't3.small': Decimal('17.00'),
                't3.medium': Decimal('34.00'),
                't3.large': Decimal('68.00'),
                't3.xlarge': Decimal('136.00'),
                't3.2xlarge': Decimal('272.00'),
                'm5.large': Decimal('77.00'),
                'm5.xlarge': Decimal('154.00'),
                'm5.2xlarge': Decimal('308.00'),
                'm5.4xlarge': Decimal('616.00')
            }
            
            return pricing.get(instance_type, Decimal('30.00'))
        
        elif resource.resource_type == 'virtual_machine':
            # Simplified Azure VM pricing
            vm_size = resource.properties.get('vm_size', 'Standard_B1s')
            
            pricing = {
                'Standard_B1s': Decimal('8.76'),
                'Standard_B2s': Decimal('35.04'),
                'Standard_D2s_v3': Decimal('70.08'),
                'Standard_D4s_v3': Decimal('140.16'),
                'Standard_E2s_v3': Decimal('87.60'),
                'Standard_E4s_v3': Decimal('175.20')
            }
            
            return pricing.get(vm_size, Decimal('40.00'))
        
        elif resource.resource_type == 'compute_instance':
            # Simplified GCP pricing
            machine_type = resource.properties.get('machine_type', 'e2-micro')
            
            pricing = {
                'e2-micro': Decimal('7.60'),
                'e2-small': Decimal('15.20'),
                'e2-medium': Decimal('30.40'),
                'n1-standard-1': Decimal('25.00'),
                'n1-standard-2': Decimal('50.00'),
                'n1-standard-4': Decimal('100.00'),
                'n1-standard-8': Decimal('200.00')
            }
            
            return pricing.get(machine_type, Decimal('30.00'))
        
        # Default for other resource types
        return Decimal('10.00')
