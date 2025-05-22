"""
Action execution engine for cloud cost optimization.
"""
from typing import Dict, List, Any, Optional
from uuid import UUID
import datetime
import logging
from decimal import Decimal

from src.core.services.automation_service import AutomationService
from src.core.services.resource_service import ResourceService
from src.providers.base import CloudProviderInterface


class ActionExecutionEngine:
    """Engine for executing actions on cloud resources."""
    
    def __init__(self, 
                 automation_service: AutomationService,
                 resource_service: ResourceService):
        self.automation_service = automation_service
        self.resource_service = resource_service
        self.logger = logging.getLogger(__name__)
    
    def execute_action(self, action_id: UUID, provider: CloudProviderInterface, executor_id: UUID = None) -> Dict[str, Any]:
        """Execute an action on a cloud resource."""
        # Get action details
        action = self.automation_service.get_action(action_id)
        if not action:
            raise ValueError(f"Action with ID {action_id} not found")
        
        # Check if action is approved
        if action.requires_approval and action.approval_status != 'approved':
            raise ValueError(f"Action with ID {action_id} requires approval before execution")
        
        # Create execution record
        execution = self.automation_service.execute_action(action_id, executor_id)
        
        result = {
            'action_id': str(action_id),
            'execution_id': str(execution.id),
            'status': 'failed',
            'message': '',
            'details': {}
        }
        
        try:
            # Get resource details if available
            resource_id = None
            resource_type = None
            
            if action.resource_id:
                resource = self.resource_service.get_resource(action.resource_id)
                if resource:
                    resource_id = resource.resource_id
                    resource_type = resource.resource_type
            
            # Map action type to provider action
            provider_action = self._map_to_provider_action(action.action_type, resource_type)
            
            # Execute action through provider
            provider_result = provider.execute_action(
                action_type=provider_action,
                resource_id=resource_id,
                resource_type=resource_type,
                parameters=action.parameters or {}
            )
            
            # Update result
            result['status'] = 'completed' if provider_result.get('success', False) else 'failed'
            result['message'] = provider_result.get('message', '')
            result['details'] = provider_result.get('details', {})
            
            # Complete execution record
            self.automation_service.complete_action_execution(
                execution_id=execution.id,
                status=result['status'],
                result=provider_result,
                logs=f"Action executed at {datetime.datetime.utcnow().isoformat()}\nResult: {result['message']}"
            )
            
            # If action was successful and from a recommendation, update recommendation status
            if result['status'] == 'completed' and action.recommendation_id:
                self.automation_service.update_recommendation_status(
                    recommendation_id=action.recommendation_id,
                    status='applied'
                )
            
            return result
        
        except Exception as e:
            error_message = f"Error executing action: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            
            # Complete execution record with error
            self.automation_service.complete_action_execution(
                execution_id=execution.id,
                status='failed',
                result={'error': str(e)},
                logs=f"Action execution failed at {datetime.datetime.utcnow().isoformat()}\nError: {error_message}"
            )
            
            result['message'] = error_message
            return result
    
    def create_action_from_recommendation(self, 
                                        recommendation_id: UUID, 
                                        created_by: UUID = None,
                                        requires_approval: bool = True,
                                        scheduled_time: datetime.datetime = None) -> Dict[str, Any]:
        """Create an action from a recommendation."""
        # Get recommendation details
        recommendation = self.automation_service.get_recommendation(recommendation_id)
        if not recommendation:
            raise ValueError(f"Recommendation with ID {recommendation_id} not found")
        
        # Map recommendation type to action type
        action_type = self._map_recommendation_to_action(recommendation.recommendation_type)
        
        # Generate parameters based on recommendation
        parameters = self._generate_action_parameters(recommendation)
        
        # Create action
        action = self.automation_service.create_action(
            cloud_account_id=recommendation.cloud_account_id,
            action_type=action_type,
            parameters=parameters,
            recommendation_id=recommendation_id,
            resource_id=recommendation.resource_id,
            created_by=created_by,
            requires_approval=requires_approval,
            scheduled_time=scheduled_time
        )
        
        return {
            'action_id': str(action.id),
            'action_type': action.action_type,
            'status': action.status,
            'approval_status': action.approval_status,
            'parameters': action.parameters,
            'recommendation_id': str(recommendation_id),
            'resource_id': str(action.resource_id) if action.resource_id else None,
            'requires_approval': action.requires_approval,
            'scheduled_time': action.scheduled_time.isoformat() if action.scheduled_time else None
        }
    
    def schedule_actions(self, actions: List[Dict[str, Any]], schedule_time: datetime.datetime) -> List[Dict[str, Any]]:
        """Schedule multiple actions for execution at a specific time."""
        scheduled_actions = []
        
        for action_data in actions:
            action_id = action_data.get('action_id')
            if not action_id:
                continue
            
            action = self.automation_service.get_action(UUID(action_id))
            if not action:
                continue
            
            # Update scheduled time
            action.scheduled_time = schedule_time
            self.automation_service.update_action(action)
            
            scheduled_actions.append({
                'action_id': str(action.id),
                'action_type': action.action_type,
                'status': action.status,
                'scheduled_time': action.scheduled_time.isoformat()
            })
        
        return scheduled_actions
    
    def process_scheduled_actions(self, provider: CloudProviderInterface) -> List[Dict[str, Any]]:
        """Process all scheduled actions that are due for execution."""
        now = datetime.datetime.utcnow()
        results = []
        
        # Get all pending actions with scheduled_time in the past
        actions = self.automation_service.get_actions_by_status('pending')
        for action in actions:
            if action.scheduled_time and action.scheduled_time <= now:
                # Execute action
                result = self.execute_action(action.id, provider)
                results.append(result)
        
        return results
    
    def _map_to_provider_action(self, action_type: str, resource_type: str) -> str:
        """Map internal action type to provider-specific action type."""
        # AWS mappings
        if resource_type == 'ec2_instance':
            mapping = {
                'start_resource': 'start_instance',
                'stop_resource': 'stop_instance',
                'resize_resource': 'resize_instance',
                'delete_resource': 'terminate_instance'
            }
            return mapping.get(action_type, action_type)
        
        elif resource_type == 'rds_instance':
            mapping = {
                'start_resource': 'start_instance',
                'stop_resource': 'stop_instance',
                'resize_resource': 'resize_instance',
                'delete_resource': 'delete_instance'
            }
            return mapping.get(action_type, action_type)
        
        elif resource_type == 's3_bucket':
            mapping = {
                'delete_resource': 'delete_bucket',
                'optimize_storage': 'update_lifecycle'
            }
            return mapping.get(action_type, action_type)
        
        # Azure mappings
        elif resource_type == 'virtual_machine':
            mapping = {
                'start_resource': 'start_vm',
                'stop_resource': 'stop_vm',
                'resize_resource': 'resize_vm',
                'delete_resource': 'delete_vm'
            }
            return mapping.get(action_type, action_type)
        
        elif resource_type == 'storage_account':
            mapping = {
                'optimize_storage': 'update_tier',
                'delete_resource': 'delete_storage_account'
            }
            return mapping.get(action_type, action_type)
        
        # GCP mappings
        elif resource_type == 'compute_instance':
            mapping = {
                'start_resource': 'start_instance',
                'stop_resource': 'stop_instance',
                'resize_resource': 'resize_instance',
                'delete_resource': 'delete_instance'
            }
            return mapping.get(action_type, action_type)
        
        elif resource_type == 'storage_bucket':
            mapping = {
                'delete_resource': 'delete_bucket',
                'optimize_storage': 'update_storage_class'
            }
            return mapping.get(action_type, action_type)
        
        # Default: return the original action type
        return action_type
    
    def _map_recommendation_to_action(self, recommendation_type: str) -> str:
        """Map recommendation type to action type."""
        mapping = {
            'resize_resource': 'resize_resource',
            'idle_resource': 'stop_resource',
            'delete_resource': 'delete_resource',
            'purchase_reservation': 'purchase_reservation',
            'missing_tags': 'add_tags',
            'cost_anomaly': 'investigate_cost',
            'general_optimization': 'optimize_resource'
        }
        
        return mapping.get(recommendation_type, 'optimize_resource')
    
    def _generate_action_parameters(self, recommendation: Any) -> Dict[str, Any]:
        """Generate action parameters based on recommendation details."""
        parameters = {}
        
        # Extract details from recommendation
        details = recommendation.details or {}
        
        if recommendation.recommendation_type == 'resize_resource':
            # For resize recommendations
            if 'recommended_instance_type' in details:
                parameters['instance_type'] = details['recommended_instance_type']
            elif 'recommended_vm_size' in details:
                parameters['vm_size'] = details['recommended_vm_size']
            elif 'recommended_machine_type' in details:
                parameters['machine_type'] = details['recommended_machine_type']
            
            # For Azure, add apply_immediately parameter
            if 'provider_type' in details and details['provider_type'] == 'azure_advisor':
                parameters['apply_immediately'] = True
        
        elif recommendation.recommendation_type == 'idle_resource':
            # For idle resource recommendations
            if 'suggested_action' in details:
                if details['suggested_action'] == 'stop_instance':
                    parameters['force'] = True
                elif details['suggested_action'] == 'stop_vm':
                    parameters['deallocate'] = True
        
        elif recommendation.recommendation_type == 'missing_tags':
            # For missing tags recommendations
            if 'suggested_tags' in details:
                tags = {}
                for tag in details['suggested_tags']:
                    tags[tag] = 'Please update'
                parameters['tags'] = tags
        
        elif recommendation.recommendation_type == 'optimize_storage':
            # For storage optimization recommendations
            if 'recommended_storage_class' in details:
                parameters['storage_class'] = details['recommended_storage_class']
            elif 'recommended_access_tier' in details:
                parameters['access_tier'] = details['recommended_access_tier']
            elif 'lifecycle_configuration' in details:
                parameters['lifecycle_configuration'] = details['lifecycle_configuration']
        
        return parameters
