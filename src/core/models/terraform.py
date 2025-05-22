"""
Terraform integration models for the Cloud Cost Optimizer.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.core.models.base import BaseModel, Base


class TerraformState(BaseModel):
    """Terraform state model representing a Terraform state file."""
    
    __tablename__ = 'terraform_states'
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    state_data = Column(JSONB, nullable=False)
    version = Column(String(50), nullable=False)
    
    # Relationships
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<TerraformState(id='{self.id}', name='{self.name}', version='{self.version}')>"


class TerraformModule(BaseModel):
    """Terraform module model representing a reusable Terraform module."""
    
    __tablename__ = 'terraform_modules'
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_type = Column(String(50), nullable=False)  # git, local, registry
    source_url = Column(String(255), nullable=False)
    version = Column(String(50), nullable=True)
    variables = Column(JSONB, nullable=True)
    is_optimized = Column(Boolean, default=False)
    
    # Relationships
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<TerraformModule(id='{self.id}', name='{self.name}', source_type='{self.source_type}')>"


class TerraformTemplate(BaseModel):
    """Terraform template model representing a Terraform configuration."""
    
    __tablename__ = 'terraform_templates'
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    variables = Column(JSONB, nullable=True)
    estimated_cost = Column(JSONB, nullable=True)
    optimization_status = Column(String(50), default='not_analyzed')  # not_analyzed, analyzed, optimized
    
    # Relationships
    organization = relationship("Organization")
    
    def __repr__(self):
        return f"<TerraformTemplate(id='{self.id}', name='{self.name}', optimization_status='{self.optimization_status}')>"
