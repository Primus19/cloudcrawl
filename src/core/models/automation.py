"""
Recommendation and action models for the Cloud Cost Optimizer.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Numeric, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.core.models.base import BaseModel, Base


class Recommendation(BaseModel):
    """Recommendation model representing cost optimization suggestions."""
    
    __tablename__ = 'recommendations'
    
    cloud_account_id = Column(UUID(as_uuid=True), ForeignKey('cloud_accounts.id'), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resources.id'), nullable=True)
    recommendation_type = Column(String(100), nullable=False)
    status = Column(String(50), default='open')  # open, applied, dismissed, expired
    priority = Column(String(20), nullable=False)  # high, medium, low
    estimated_savings = Column(Numeric(20, 6), nullable=True)
    savings_currency = Column(String(3), nullable=True)
    savings_period = Column(String(20), default='monthly')  # monthly, yearly
    details = Column(JSONB, nullable=True)
    
    # Relationships
    cloud_account = relationship("CloudAccount")
    resource = relationship("Resource", back_populates="recommendations")
    actions = relationship("Action", back_populates="recommendation")
    
    def __repr__(self):
        return f"<Recommendation(id='{self.id}', recommendation_type='{self.recommendation_type}', status='{self.status}', priority='{self.priority}')>"


class Action(BaseModel):
    """Action model representing executable operations on cloud resources."""
    
    __tablename__ = 'actions'
    
    recommendation_id = Column(UUID(as_uuid=True), ForeignKey('recommendations.id'), nullable=True)
    cloud_account_id = Column(UUID(as_uuid=True), ForeignKey('cloud_accounts.id'), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resources.id'), nullable=True)
    action_type = Column(String(100), nullable=False)
    status = Column(String(50), default='pending')  # pending, in_progress, completed, failed, cancelled
    parameters = Column(JSONB, nullable=True)
    result = Column(JSONB, nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
    executed_time = Column(DateTime, nullable=True)
    completed_time = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    requires_approval = Column(Boolean, default=True)
    approval_status = Column(String(50), default='pending')  # pending, approved, rejected
    
    # Relationships
    recommendation = relationship("Recommendation", back_populates="actions")
    cloud_account = relationship("CloudAccount")
    resource = relationship("Resource")
    creator = relationship("User")
    approvals = relationship("ActionApproval", back_populates="action", cascade="all, delete-orphan")
    executions = relationship("ActionExecution", back_populates="action", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Action(id='{self.id}', action_type='{self.action_type}', status='{self.status}', approval_status='{self.approval_status}')>"


class ActionApproval(BaseModel):
    """Action approval model representing approval workflow for actions."""
    
    __tablename__ = 'action_approvals'
    
    action_id = Column(UUID(as_uuid=True), ForeignKey('actions.id'), nullable=False)
    approver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default='pending')  # pending, approved, rejected
    comments = Column(Text, nullable=True)
    
    # Relationships
    action = relationship("Action", back_populates="approvals")
    approver = relationship("User")
    
    def __repr__(self):
        return f"<ActionApproval(id='{self.id}', action_id='{self.action_id}', approver_id='{self.approver_id}', status='{self.status}')>"


class ActionExecution(BaseModel):
    """Action execution model representing the execution history of an action."""
    
    __tablename__ = 'action_executions'
    
    action_id = Column(UUID(as_uuid=True), ForeignKey('actions.id'), nullable=False)
    executor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    status = Column(String(50), default='in_progress')  # in_progress, completed, failed, cancelled
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    result = Column(JSONB, nullable=True)
    logs = Column(Text, nullable=True)
    attempt = Column(Integer, default=1)
    
    # Relationships
    action = relationship("Action", back_populates="executions")
    executor = relationship("User")
    
    def __repr__(self):
        return f"<ActionExecution(id='{self.id}', action_id='{self.action_id}', status='{self.status}', attempt='{self.attempt}')>"


class Workflow(BaseModel):
    """Workflow model representing a sequence of actions."""
    
    __tablename__ = 'workflows'
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    trigger_type = Column(String(50), nullable=False)  # manual, scheduled, event
    trigger_config = Column(JSONB, nullable=True)
    steps = Column(JSONB, nullable=False)
    status = Column(String(50), default='active')  # active, inactive, archived
    
    # Relationships
    organization = relationship("Organization")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow(id='{self.id}', name='{self.name}', trigger_type='{self.trigger_type}', status='{self.status}')>"


class WorkflowExecution(BaseModel):
    """Workflow execution model representing the execution history of a workflow."""
    
    __tablename__ = 'workflow_executions'
    
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflows.id'), nullable=False)
    initiator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    status = Column(String(50), default='in_progress')  # in_progress, completed, failed, cancelled
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    results = Column(JSONB, nullable=True)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="executions")
    initiator = relationship("User")
    
    def __repr__(self):
        return f"<WorkflowExecution(id='{self.id}', workflow_id='{self.workflow_id}', status='{self.status}')>"
