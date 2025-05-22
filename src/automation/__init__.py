"""
Main automation module for cloud cost optimizer.
"""
from typing import Dict, List, Any, Optional
from uuid import UUID

from src.core.services.automation_service import AutomationService
from src.core.services.resource_service import ResourceService
from src.core.services.cost_service import CostService
from src.providers.base import CloudProviderInterface
from src.automation.recommendation.recommendation_engine import RecommendationEngine
from src.automation.execution.action_engine import ActionExecutionEngine
from src.automation.workflow.workflow_engine import WorkflowEngine


class AutomationManager:
    """Manager for coordinating recommendation, action, and workflow engines."""
    
    def __init__(self, 
                 automation_service: AutomationService,
                 resource_service: ResourceService,
                 cost_service: CostService):
        self.automation_service = automation_service
        self.resource_service = resource_service
        self.cost_service = cost_service
        
        # Initialize engines
        self.recommendation_engine = RecommendationEngine(
            resource_service=resource_service,
            cost_service=cost_service,
            automation_service=automation_service
        )
        
        self.action_engine = ActionExecutionEngine(
            automation_service=automation_service,
            resource_service=resource_service
        )
        
        self.workflow_engine = WorkflowEngine(
            automation_service=automation_service,
            action_engine=self.action_engine
        )
    
    def generate_recommendations(self, cloud_account_id: UUID, provider: CloudProviderInterface) -> List[Dict[str, Any]]:
        """Generate recommendations for a cloud account."""
        return self.recommendation_engine.generate_recommendations(cloud_account_id, provider)
    
    def create_action_from_recommendation(self, 
                                        recommendation_id: UUID, 
                                        created_by: UUID = None,
                                        requires_approval: bool = True) -> Dict[str, Any]:
        """Create an action from a recommendation."""
        return self.action_engine.create_action_from_recommendation(
            recommendation_id=recommendation_id,
            created_by=created_by,
            requires_approval=requires_approval
        )
    
    def execute_action(self, action_id: UUID, provider: CloudProviderInterface, executor_id: UUID = None) -> Dict[str, Any]:
        """Execute an action."""
        return self.action_engine.execute_action(action_id, provider, executor_id)
    
    def create_workflow(self, 
                      organization_id: UUID, 
                      name: str,
                      trigger_type: str,
                      steps: List[Dict[str, Any]],
                      description: str = None,
                      trigger_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a workflow."""
        return self.workflow_engine.create_workflow(
            organization_id=organization_id,
            name=name,
            trigger_type=trigger_type,
            steps=steps,
            description=description,
            trigger_config=trigger_config
        )
    
    def execute_workflow(self, workflow_id: UUID, provider_map: Dict[str, Any], initiator_id: UUID = None) -> Dict[str, Any]:
        """Execute a workflow."""
        return self.workflow_engine.execute_workflow(workflow_id, provider_map, initiator_id)
    
    def process_scheduled_items(self, provider_map: Dict[str, Any]) -> Dict[str, Any]:
        """Process all scheduled actions and workflows."""
        results = {
            'actions': [],
            'workflows': []
        }
        
        # Process scheduled actions
        for cloud_account_id, provider in provider_map.items():
            action_results = self.action_engine.process_scheduled_actions(provider)
            results['actions'].extend(action_results)
        
        # Process scheduled workflows
        workflow_results = self.workflow_engine.process_scheduled_workflows(provider_map)
        results['workflows'] = workflow_results
        
        return results
