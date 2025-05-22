"""
Recommendation and action execution service.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import datetime
from decimal import Decimal

from src.core.repositories.base import BaseRepository
from src.core.models.automation import (
    Recommendation, Action, ActionApproval, ActionExecution,
    Workflow, WorkflowExecution
)


class AutomationService:
    """Service for recommendations and action execution."""
    
    def __init__(self, 
                 recommendation_repository: BaseRepository[Recommendation],
                 action_repository: BaseRepository[Action],
                 action_approval_repository: BaseRepository[ActionApproval],
                 action_execution_repository: BaseRepository[ActionExecution],
                 workflow_repository: BaseRepository[Workflow],
                 workflow_execution_repository: BaseRepository[WorkflowExecution]):
        self.recommendation_repository = recommendation_repository
        self.action_repository = action_repository
        self.action_approval_repository = action_approval_repository
        self.action_execution_repository = action_execution_repository
        self.workflow_repository = workflow_repository
        self.workflow_execution_repository = workflow_execution_repository
    
    # Recommendation Management
    
    def create_recommendation(self, 
                            cloud_account_id: UUID, 
                            recommendation_type: str,
                            priority: str,
                            estimated_savings: Decimal = None,
                            savings_currency: str = None,
                            savings_period: str = 'monthly',
                            resource_id: UUID = None,
                            details: Dict[str, Any] = None) -> Recommendation:
        """Create a new recommendation."""
        recommendation = Recommendation(
            cloud_account_id=cloud_account_id,
            resource_id=resource_id,
            recommendation_type=recommendation_type,
            priority=priority,
            estimated_savings=estimated_savings,
            savings_currency=savings_currency,
            savings_period=savings_period,
            details=details,
            status='open'
        )
        return self.recommendation_repository.create(recommendation)
    
    def get_recommendation(self, recommendation_id: UUID) -> Optional[Recommendation]:
        """Get a recommendation by ID."""
        return self.recommendation_repository.get_by_id(recommendation_id)
    
    def get_recommendations_by_account(self, cloud_account_id: UUID, status: str = None) -> List[Recommendation]:
        """Get recommendations for a cloud account."""
        if status:
            return self.recommendation_repository.filter_by(
                cloud_account_id=cloud_account_id,
                status=status
            )
        return self.recommendation_repository.filter_by(cloud_account_id=cloud_account_id)
    
    def get_recommendations_by_resource(self, resource_id: UUID, status: str = None) -> List[Recommendation]:
        """Get recommendations for a specific resource."""
        if status:
            return self.recommendation_repository.filter_by(
                resource_id=resource_id,
                status=status
            )
        return self.recommendation_repository.filter_by(resource_id=resource_id)
    
    def update_recommendation_status(self, recommendation_id: UUID, status: str) -> Recommendation:
        """Update the status of a recommendation."""
        recommendation = self.recommendation_repository.get_by_id(recommendation_id)
        if not recommendation:
            raise ValueError(f"Recommendation with ID {recommendation_id} not found")
        
        recommendation.status = status
        return self.recommendation_repository.update(recommendation)
    
    def get_recommendations_summary(self, cloud_account_id: UUID) -> Dict[str, Any]:
        """Get a summary of recommendations for a cloud account."""
        recommendations = self.get_recommendations_by_account(cloud_account_id)
        
        # Count by status
        status_counts = {}
        for rec in recommendations:
            if rec.status not in status_counts:
                status_counts[rec.status] = 0
            status_counts[rec.status] += 1
        
        # Count by priority
        priority_counts = {}
        for rec in recommendations:
            if rec.priority not in priority_counts:
                priority_counts[rec.priority] = 0
            priority_counts[rec.priority] += 1
        
        # Count by type
        type_counts = {}
        for rec in recommendations:
            if rec.recommendation_type not in type_counts:
                type_counts[rec.recommendation_type] = 0
            type_counts[rec.recommendation_type] += 1
        
        # Calculate total potential savings
        total_savings = Decimal('0')
        savings_by_currency = {}
        
        for rec in recommendations:
            if rec.status == 'open' and rec.estimated_savings and rec.savings_currency:
                if rec.savings_currency not in savings_by_currency:
                    savings_by_currency[rec.savings_currency] = Decimal('0')
                
                savings_by_currency[rec.savings_currency] += rec.estimated_savings
        
        return {
            'total_count': len(recommendations),
            'status_counts': status_counts,
            'priority_counts': priority_counts,
            'type_counts': type_counts,
            'savings_by_currency': {k: float(v) for k, v in savings_by_currency.items()}
        }
    
    # Action Management
    
    def create_action(self, 
                    cloud_account_id: UUID, 
                    action_type: str,
                    parameters: Dict[str, Any],
                    recommendation_id: UUID = None,
                    resource_id: UUID = None,
                    created_by: UUID = None,
                    requires_approval: bool = True,
                    scheduled_time: datetime.datetime = None) -> Action:
        """Create a new action."""
        action = Action(
            cloud_account_id=cloud_account_id,
            recommendation_id=recommendation_id,
            resource_id=resource_id,
            action_type=action_type,
            parameters=parameters,
            created_by=created_by,
            requires_approval=requires_approval,
            scheduled_time=scheduled_time,
            status='pending',
            approval_status='pending' if requires_approval else 'approved'
        )
        return self.action_repository.create(action)
    
    def get_action(self, action_id: UUID) -> Optional[Action]:
        """Get an action by ID."""
        return self.action_repository.get_by_id(action_id)
    
    def get_actions_by_account(self, cloud_account_id: UUID, status: str = None) -> List[Action]:
        """Get actions for a cloud account."""
        if status:
            return self.action_repository.filter_by(
                cloud_account_id=cloud_account_id,
                status=status
            )
        return self.action_repository.filter_by(cloud_account_id=cloud_account_id)
    
    def approve_action(self, action_id: UUID, approver_id: UUID, comments: str = None) -> Action:
        """Approve an action."""
        action = self.action_repository.get_by_id(action_id)
        if not action:
            raise ValueError(f"Action with ID {action_id} not found")
        
        if not action.requires_approval:
            raise ValueError(f"Action with ID {action_id} does not require approval")
        
        if action.approval_status != 'pending':
            raise ValueError(f"Action with ID {action_id} is not pending approval")
        
        # Create approval record
        approval = ActionApproval(
            action_id=action_id,
            approver_id=approver_id,
            status='approved',
            comments=comments
        )
        self.action_approval_repository.create(approval)
        
        # Update action status
        action.approval_status = 'approved'
        return self.action_repository.update(action)
    
    def reject_action(self, action_id: UUID, approver_id: UUID, comments: str = None) -> Action:
        """Reject an action."""
        action = self.action_repository.get_by_id(action_id)
        if not action:
            raise ValueError(f"Action with ID {action_id} not found")
        
        if not action.requires_approval:
            raise ValueError(f"Action with ID {action_id} does not require approval")
        
        if action.approval_status != 'pending':
            raise ValueError(f"Action with ID {action_id} is not pending approval")
        
        # Create approval record
        approval = ActionApproval(
            action_id=action_id,
            approver_id=approver_id,
            status='rejected',
            comments=comments
        )
        self.action_approval_repository.create(approval)
        
        # Update action status
        action.approval_status = 'rejected'
        action.status = 'cancelled'
        return self.action_repository.update(action)
    
    def execute_action(self, action_id: UUID, executor_id: UUID = None) -> ActionExecution:
        """Execute an action."""
        action = self.action_repository.get_by_id(action_id)
        if not action:
            raise ValueError(f"Action with ID {action_id} not found")
        
        if action.requires_approval and action.approval_status != 'approved':
            raise ValueError(f"Action with ID {action_id} requires approval before execution")
        
        if action.status not in ['pending', 'failed']:
            raise ValueError(f"Action with ID {action_id} cannot be executed in status {action.status}")
        
        # Update action status
        action.status = 'in_progress'
        action.executed_time = datetime.datetime.utcnow()
        self.action_repository.update(action)
        
        # Create execution record
        execution = ActionExecution(
            action_id=action_id,
            executor_id=executor_id,
            status='in_progress',
            start_time=datetime.datetime.utcnow()
        )
        return self.action_execution_repository.create(execution)
    
    def complete_action_execution(self, 
                                execution_id: UUID, 
                                status: str,
                                result: Dict[str, Any] = None,
                                logs: str = None) -> ActionExecution:
        """Complete an action execution."""
        execution = self.action_execution_repository.get_by_id(execution_id)
        if not execution:
            raise ValueError(f"Action execution with ID {execution_id} not found")
        
        if execution.status != 'in_progress':
            raise ValueError(f"Action execution with ID {execution_id} is not in progress")
        
        # Update execution record
        execution.status = status
        execution.end_time = datetime.datetime.utcnow()
        execution.result = result
        execution.logs = logs
        self.action_execution_repository.update(execution)
        
        # Update action status
        action = self.action_repository.get_by_id(execution.action_id)
        action.status = status
        action.completed_time = datetime.datetime.utcnow()
        action.result = result
        self.action_repository.update(action)
        
        # If action was from a recommendation, update recommendation status
        if action.recommendation_id and status == 'completed':
            recommendation = self.recommendation_repository.get_by_id(action.recommendation_id)
            if recommendation and recommendation.status == 'open':
                recommendation.status = 'applied'
                self.recommendation_repository.update(recommendation)
        
        return execution
    
    # Workflow Management
    
    def create_workflow(self, 
                      organization_id: UUID, 
                      name: str,
                      trigger_type: str,
                      steps: List[Dict[str, Any]],
                      description: str = None,
                      trigger_config: Dict[str, Any] = None) -> Workflow:
        """Create a new workflow."""
        workflow = Workflow(
            organization_id=organization_id,
            name=name,
            description=description,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            steps=steps,
            status='active'
        )
        return self.workflow_repository.create(workflow)
    
    def execute_workflow(self, workflow_id: UUID, initiator_id: UUID = None) -> WorkflowExecution:
        """Execute a workflow."""
        workflow = self.workflow_repository.get_by_id(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with ID {workflow_id} not found")
        
        if workflow.status != 'active':
            raise ValueError(f"Workflow with ID {workflow_id} is not active")
        
        # Create workflow execution record
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            initiator_id=initiator_id,
            status='in_progress',
            start_time=datetime.datetime.utcnow()
        )
        return self.workflow_execution_repository.create(execution)
    
    def process_workflow_step(self, 
                            execution_id: UUID, 
                            step_index: int,
                            step_result: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a workflow step and return the next step."""
        execution = self.workflow_execution_repository.get_by_id(execution_id)
        if not execution:
            raise ValueError(f"Workflow execution with ID {execution_id} not found")
        
        if execution.status != 'in_progress':
            raise ValueError(f"Workflow execution with ID {execution_id} is not in progress")
        
        workflow = self.workflow_repository.get_by_id(execution.workflow_id)
        
        # Update results with step result
        results = execution.results or {}
        if step_result:
            results[f"step_{step_index}"] = step_result
            execution.results = results
            self.workflow_execution_repository.update(execution)
        
        # Check if we've reached the end of the workflow
        if step_index >= len(workflow.steps) - 1:
            execution.status = 'completed'
            execution.end_time = datetime.datetime.utcnow()
            self.workflow_execution_repository.update(execution)
            return {"status": "completed"}
        
        # Return the next step
        next_step = workflow.steps[step_index + 1]
        return {
            "status": "continue",
            "next_step_index": step_index + 1,
            "next_step": next_step
        }
    
    def cancel_workflow_execution(self, execution_id: UUID, reason: str = None) -> WorkflowExecution:
        """Cancel a workflow execution."""
        execution = self.workflow_execution_repository.get_by_id(execution_id)
        if not execution:
            raise ValueError(f"Workflow execution with ID {execution_id} not found")
        
        if execution.status != 'in_progress':
            raise ValueError(f"Workflow execution with ID {execution_id} is not in progress")
        
        # Update execution record
        execution.status = 'cancelled'
        execution.end_time = datetime.datetime.utcnow()
        
        # Add cancellation reason to results
        results = execution.results or {}
        results["cancellation_reason"] = reason
        execution.results = results
        
        return self.workflow_execution_repository.update(execution)
