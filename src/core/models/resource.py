"""
Cloud account and resource models for the Cloud Cost Optimizer.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Table, UniqueConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.core.models.base import BaseModel, Base

# Association table for cloud account-team relationship
cloud_account_teams = Table(
    'cloud_account_teams',
    Base.metadata,
    Column('cloud_account_id', UUID(as_uuid=True), ForeignKey('cloud_accounts.id'), primary_key=True),
    Column('team_id', UUID(as_uuid=True), ForeignKey('teams.id'), primary_key=True),
    Column('access_level', String(50), nullable=False)
)

class CloudAccount(BaseModel):
    """Cloud account model representing a cloud provider account."""
    
    __tablename__ = 'cloud_accounts'
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False)  # 'aws', 'azure', 'gcp'
    account_id = Column(String(255), nullable=False)
    credentials = Column(JSONB, nullable=True)
    status = Column(String(50), default='active')
    last_sync = Column(DateTime, nullable=True)
    settings = Column(JSONB, nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="cloud_accounts")
    resources = relationship("Resource", back_populates="cloud_account", cascade="all, delete-orphan")
    resource_groups = relationship("ResourceGroup", back_populates="cloud_account", cascade="all, delete-orphan")
    teams = relationship("Team", secondary=cloud_account_teams)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('organization_id', 'provider', 'account_id', name='uq_cloud_account_per_org'),
    )
    
    def __repr__(self):
        return f"<CloudAccount(id='{self.id}', name='{self.name}', provider='{self.provider}', account_id='{self.account_id}')>"


class ResourceGroup(BaseModel):
    """Resource group model representing a logical grouping of resources."""
    
    __tablename__ = 'resource_groups'
    
    cloud_account_id = Column(UUID(as_uuid=True), ForeignKey('cloud_accounts.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    cloud_account = relationship("CloudAccount", back_populates="resource_groups")
    resources = relationship("Resource", secondary="resource_group_memberships", back_populates="resource_groups")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('cloud_account_id', 'name', name='uq_resource_group_name_per_account'),
    )
    
    def __repr__(self):
        return f"<ResourceGroup(id='{self.id}', name='{self.name}', cloud_account_id='{self.cloud_account_id}')>"


class Resource(BaseModel):
    """Resource model representing a cloud resource."""
    
    __tablename__ = 'resources'
    
    cloud_account_id = Column(UUID(as_uuid=True), ForeignKey('cloud_accounts.id'), nullable=False)
    resource_id = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=False)
    name = Column(String(255), nullable=True)
    region = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
    last_seen = Column(DateTime, nullable=False)
    properties = Column(JSONB, nullable=True)
    
    # Relationships
    cloud_account = relationship("CloudAccount", back_populates="resources")
    tags = relationship("Tag", back_populates="resource", cascade="all, delete-orphan")
    resource_groups = relationship("ResourceGroup", secondary="resource_group_memberships", back_populates="resources")
    recommendations = relationship("Recommendation", back_populates="resource")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('cloud_account_id', 'resource_id', name='uq_resource_id_per_account'),
    )
    
    def __repr__(self):
        return f"<Resource(id='{self.id}', resource_id='{self.resource_id}', resource_type='{self.resource_type}', name='{self.name}')>"


# Association table for resource-resource group relationship
resource_group_memberships = Table(
    'resource_group_memberships',
    Base.metadata,
    Column('resource_id', UUID(as_uuid=True), ForeignKey('resources.id'), primary_key=True),
    Column('resource_group_id', UUID(as_uuid=True), ForeignKey('resource_groups.id'), primary_key=True)
)


class Tag(BaseModel):
    """Tag model representing a key-value tag on a resource."""
    
    __tablename__ = 'tags'
    
    resource_id = Column(UUID(as_uuid=True), ForeignKey('resources.id'), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=True)
    
    # Relationships
    resource = relationship("Resource", back_populates="tags")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('resource_id', 'key', name='uq_tag_key_per_resource'),
    )
    
    def __repr__(self):
        return f"<Tag(id='{self.id}', resource_id='{self.resource_id}', key='{self.key}', value='{self.value}')>"
