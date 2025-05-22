"""
Workflow engine for automating sequences of actions.
"""
from typing import Dict, List, Any, Optional
from uuid import UUID
import datetime
import logging
import json

from src.core.services.automation_service import AutomationService
from src.automation.execution.action_engine import ActionExecutionEngine


class WorkflowEngine:
    """Engine for executing workflows of multiple actions."""
    
    def __init__(self, 
                 automation_service: AutomationService,
                 action_engine: ActionExecutionEngine):
        self.automation_service = automation_service
        self.action_engine = action_engine
        self.logger = logging.getLogger(__name__)
    
    def create_workflow(self, 
                      organization_id: UUID, 
                      name: str,
                      trigger_type: str,
                      steps: List[Dict[str, Any]],
                      description: str = None,
                      trigger_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new workflow."""
        # Validate steps
        self._validate_workflow_steps(steps)
        
        # Create workflow
        workflow = self.automation_service.create_workflow(
            organization_id=organization_id,
            name=name,
            description=description,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            steps=steps
        )
        
        return {
            'workflow_id': str(workflow.id),
            'name': workflow.name,
            'trigger_type': workflow.trigger_type,
            'status': workflow.status,
            'steps_count': len(workflow.steps)
        }
    
    def execute_workflow(self, workflow_id: UUID, provider_map: Dict[str, Any], initiator_id: UUID = None) -> Dict[str, Any]:
        """Execute a workflow."""
        # Start workflow execution
        execution = self.automation_service.execute_workflow(workflow_id, initiator_id)
        
        result = {
            'workflow_id': str(workflow_id),
            'execution_id': str(execution.id),
            'status': 'in_progress',
            'steps_results': [],
            'start_time': execution.start_time.isoformat() if execution.start_time else None
        }
        
        try:
            # Get workflow
            workflow = self.automation_service.get_workflow(workflow_id)
            if not workflow:
                raise ValueError(f"Workflow with ID {workflow_id} not found")
            
            # Execute steps sequentially
            current_step = 0
            step_results = []
            
            while current_step < len(workflow.steps):
                step = workflow.steps[current_step]
                step_result = self._execute_workflow_step(step, provider_map, execution.id, current_step)
                step_results.append(step_result)
                
                # Check if step was successful
                if step_result.get('status') != 'completed':
                    # Step failed, stop workflow
                    self.automation_service.cancel_workflow_execution(
                        execution_id=execution.id,
                        reason=f"Step {current_step} failed: {step_result.get('message', '')}"
                    )
                    
                    result['status'] = 'failed'
                    result['steps_results'] = step_results
                    result['failed_step'] = current_step
                    result['message'] = f"Workflow failed at step {current_step}: {step_result.get('message', '')}"
                    return result
                
                # Process next step
                next_step = self.automation_service.process_workflow_step(
                    execution_id=execution.id,
                    step_index=current_step,
                    step_result=step_result
                )
                
                if next_step.get('status') == 'completed':
                    # Workflow completed
                    result['status'] = 'completed'
                    result['steps_results'] = step_results
                    result['message'] = "Workflow completed successfully"
                    return result
                
                # Move to next step
                current_step = next_step.get('next_step_index', current_step + 1)
            
            # All steps completed
            result['status'] = 'completed'
            result['steps_results'] = step_results
            result['message'] = "Workflow completed successfully"
            return result
        
        except Exception as e:
            error_message = f"Error executing workflow: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            
            # Cancel workflow execution
            self.automation_service.cancel_workflow_execution(
                execution_id=execution.id,
                reason=error_message
            )
            
            result['status'] = 'failed'
            result['message'] = error_message
            return result
    
    def _execute_workflow_step(self, 
                             step: Dict[str, Any], 
                             provider_map: Dict[str, Any],
                             execution_id: UUID,
                             step_index: int) -> Dict[str, Any]:
        """Execute a single workflow step."""
        step_type = step.get('type')
        
        if step_type == 'action':
            # Execute action
            action_id = step.get('action_id')
            if not action_id:
                return {
                    'status': 'failed',
                    'message': "Missing action_id in workflow step"
                }
            
            # Get cloud account ID for the action
            action = self.automation_service.get_action(UUID(action_id))
            if not action:
                return {
                    'status': 'failed',
                    'message': f"Action with ID {action_id} not found"
                }
            
            # Get provider for the cloud account
            cloud_account = action.cloud_account
            if not cloud_account:
                return {
                    'status': 'failed',
                    'message': f"Cloud account not found for action {action_id}"
                }
            
            provider = provider_map.get(str(cloud_account.id))
            if not provider:
                return {
                    'status': 'failed',
                    'message': f"Provider not found for cloud account {cloud_account.id}"
                }
            
            # Execute action
            action_result = self.action_engine.execute_action(UUID(action_id), provider)
            
            return {
                'status': action_result.get('status'),
                'action_id': action_id,
                'message': action_result.get('message', ''),
                'details': action_result.get('details', {})
            }
        
        elif step_type == 'condition':
            # Evaluate condition
            condition = step.get('condition')
            if not condition:
                return {
                    'status': 'failed',
                    'message': "Missing condition in workflow step"
                }
            
            # Get previous step result if referenced
            if 'previous_step_result' in json.dumps(condition):
                # Get workflow execution results
                execution = self.automation_service.get_workflow_execution(execution_id)
                if not execution or not execution.results:
                    return {
                        'status': 'failed',
                        'message': "Cannot evaluate condition: no previous step results available"
                    }
                
                # Replace placeholders with actual values
                condition_str = json.dumps(condition)
                for i in range(step_index):
                    step_key = f"step_{i}"
                    if step_key in execution.results:
                        placeholder = f"{{previous_step_result[{i}]}}"
                        condition_str = condition_str.replace(placeholder, json.dumps(execution.results[step_key]))
                
                condition = json.loads(condition_str)
            
            # Evaluate condition
            result = self._evaluate_condition(condition)
            
            return {
                'status': 'completed',
                'condition_result': result,
                'message': f"Condition evaluated to {result}"
            }
        
        elif step_type == 'delay':
            # Delay execution
            duration_seconds = step.get('duration_seconds', 0)
            
            # In a real implementation, this would use a task queue or scheduler
            # For this example, we'll just return success
            return {
                'status': 'completed',
                'message': f"Delayed execution for {duration_seconds} seconds",
                'duration_seconds': duration_seconds
            }
        
        else:
            return {
                'status': 'failed',
                'message': f"Unsupported step type: {step_type}"
            }
    
    def _evaluate_condition(self, condition: Dict[str, Any]) -> bool:
        """Evaluate a condition expression."""
        operator = condition.get('operator')
        
        if operator == 'equals':
            return condition.get('left') == condition.get('right')
        
        elif operator == 'not_equals':
            return condition.get('left') != condition.get('right')
        
        elif operator == 'greater_than':
            return condition.get('left') > condition.get('right')
        
        elif operator == 'less_than':
            return condition.get('left') < condition.get('right')
        
        elif operator == 'contains':
            left = condition.get('left')
            right = condition.get('right')
            return right in left if isinstance(left, (list, str, dict)) else False
        
        elif operator == 'and':
            for subcondition in condition.get('conditions', []):
                if not self._evaluate_condition(subcondition):
                    return False
            return True
        
        elif operator == 'or':
            for subcondition in condition.get('conditions', []):
                if self._evaluate_condition(subcondition):
                    return True
            return False
        
        elif operator == 'not':
            return not self._evaluate_condition(condition.get('condition', {}))
        
        return False
    
    def _validate_workflow_steps(self, steps: List[Dict[str, Any]]) -> None:
        """Validate workflow steps."""
        if not steps:
            raise ValueError("Workflow must have at least one step")
        
        for i, step in enumerate(steps):
            step_type = step.get('type')
            if not step_type:
                raise ValueError(f"Step {i} is missing type")
            
            if step_type == 'action':
                if 'action_id' not in step:
                    raise ValueError(f"Step {i} is missing action_id")
            
            elif step_type == 'condition':
                if 'condition' not in step:
                    raise ValueError(f"Step {i} is missing condition")
                if 'true_branch' not in step and 'false_branch' not in step:
                    raise ValueError(f"Step {i} is missing true_branch and/or false_branch")
            
            elif step_type == 'delay':
                if 'duration_seconds' not in step:
                    raise ValueError(f"Step {i} is missing duration_seconds")
            
            else:
                raise ValueError(f"Step {i} has unsupported type: {step_type}")
    
    def process_scheduled_workflows(self, provider_map: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process all scheduled workflows that are due for execution."""
        now = datetime.datetime.utcnow()
        results = []
        
        # Get all active workflows with trigger_type = 'scheduled'
        workflows = self.automation_service.get_workflows_by_trigger_type('scheduled')
        
        for workflow in workflows:
            trigger_config = workflow.trigger_config or {}
            schedule = trigger_config.get('schedule')
            
            if not schedule:
                continue
            
            # Check if workflow should be executed now
            if self._should_execute_workflow(schedule, now):
                # Execute workflow
                result = self.execute_workflow(workflow.id, provider_map)
                results.append(result)
        
        return results
    
    def _should_execute_workflow(self, schedule: Dict[str, Any], now: datetime.datetime) -> bool:
        """Check if a workflow should be executed based on its schedule."""
        # This is a simplified implementation
        # In a real implementation, this would use a more sophisticated scheduler
        
        # Check if schedule has a cron expression
        if 'cron' in schedule:
            # Parse cron expression and check if it matches current time
            # For simplicity, we'll just return True for this example
            return True
        
        # Check if schedule has a fixed time
        if 'time' in schedule:
            schedule_time = datetime.datetime.fromisoformat(schedule['time'])
            # Check if current time is within 5 minutes of scheduled time
            delta = abs((now - schedule_time).total_seconds())
            return delta <= 300
        
        # Check if schedule has an interval
        if 'interval_hours' in schedule:
            interval_hours = schedule['interval_hours']
            last_execution = schedule.get('last_execution')
            
            if not last_execution:
                return True
            
            last_execution_time = datetime.datetime.fromisoformat(last_execution)
            elapsed_hours = (now - last_execution_time).total_seconds() / 3600
            
            return elapsed_hours >= interval_hours
        
        return False
