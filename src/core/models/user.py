"""
User and organization models for the Cloud Cost Optimizer.
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Table, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from src.core.models.base import BaseModel, Base

# Association table for user-team relationship
user_teams = Table(
    'user_teams',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('team_id', UUID(as_uuid=True), ForeignKey('teams.id'), primary_key=True),
    Column('role', String(50), nullable=False)
)

class Organization(BaseModel):
    """Organization model representing a customer organization."""
    
    __tablename__ = 'organizations'
    
    name = Column(String(255), nullable=False)
    settings = Column(JSONB, nullable=True)
    
    # Relationships
    teams = relationship("Team", back_populates="organization", cascade="all, delete-orphan")
    cloud_accounts = relationship("CloudAccount", back_populates="organization", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Organization(id='{self.id}', name='{self.name}')>"


class Team(BaseModel):
    """Team model representing a group of users within an organization."""
    
    __tablename__ = 'teams'
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    settings = Column(JSONB, nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="teams")
    users = relationship("User", secondary=user_teams, back_populates="teams")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('organization_id', 'name', name='uq_team_name_per_org'),
    )
    
    def __repr__(self):
        return f"<Team(id='{self.id}', name='{self.name}', organization_id='{self.organization_id}')>"


class User(BaseModel):
    """User model representing a user of the system."""
    
    __tablename__ = 'users'
    
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=True)
    mfa_enabled = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    status = Column(String(50), default='active')
    settings = Column(JSONB, nullable=True)
    
    # Relationships
    teams = relationship("Team", secondary=user_teams, back_populates="users")
    
    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', name='{self.name}')>"


class Permission(BaseModel):
    """Permission model representing an action that can be performed on a resource."""
    
    __tablename__ = 'permissions'
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=False)
    action_type = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f"<Permission(id='{self.id}', name='{self.name}', resource_type='{self.resource_type}', action_type='{self.action_type}')>"


# Association table for role-permission relationship
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role', String(50), primary_key=True),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True),
    Column('organization_id', UUID(as_uuid=True), ForeignKey('organizations.id'), primary_key=True)
)
