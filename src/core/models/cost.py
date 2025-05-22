"""
Cost and budget models for the Cloud Cost Optimizer.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Numeric, Date, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.core.models.base import BaseModel, Base


class CostData(BaseModel):
    """Cost data model representing cloud resource costs."""
    
    __tablename__ = 'cost_data'
    
    cloud_account_id = Column(UUID(as_uuid=True), ForeignKey('cloud_accounts.id'), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resources.id'), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Numeric(20, 6), nullable=False)
    currency = Column(String(3), nullable=False)
    granularity = Column(String(20), nullable=False)  # hourly, daily, monthly
    dimensions = Column(JSONB, nullable=True)
    
    # Relationships
    cloud_account = relationship("CloudAccount")
    resource = relationship("Resource")
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_cost_data_cloud_account_timestamp', cloud_account_id, timestamp),
        Index('idx_cost_data_resource_timestamp', resource_id, timestamp),
    )
    
    def __repr__(self):
        return f"<CostData(id='{self.id}', cloud_account_id='{self.cloud_account_id}', timestamp='{self.timestamp}', amount='{self.amount}')>"


class Budget(BaseModel):
    """Budget model representing spending limits."""
    
    __tablename__ = 'budgets'
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(Numeric(20, 6), nullable=False)
    currency = Column(String(3), nullable=False)
    period = Column(String(20), nullable=False)  # monthly, quarterly, yearly
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    filters = Column(JSONB, nullable=True)
    
    # Relationships
    organization = relationship("Organization")
    alerts = relationship("BudgetAlert", back_populates="budget", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Budget(id='{self.id}', name='{self.name}', amount='{self.amount}', period='{self.period}')>"


class BudgetAlert(BaseModel):
    """Budget alert model representing notification thresholds for budgets."""
    
    __tablename__ = 'budget_alerts'
    
    budget_id = Column(UUID(as_uuid=True), ForeignKey('budgets.id'), nullable=False)
    threshold = Column(Numeric(5, 2), nullable=False)  # percentage
    notification_channels = Column(JSONB, nullable=False)
    
    # Relationships
    budget = relationship("Budget", back_populates="alerts")
    
    def __repr__(self):
        return f"<BudgetAlert(id='{self.id}', budget_id='{self.budget_id}', threshold='{self.threshold}')>"
