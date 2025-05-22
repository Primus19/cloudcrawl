"""
User service for authentication and user management.
"""
from typing import Optional, List
from uuid import UUID
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from src.core.repositories.base import BaseRepository
from src.core.models.user import User, Organization, Team


class UserService:
    """Service for user management and authentication."""
    
    def __init__(self, user_repository: BaseRepository[User], 
                 organization_repository: BaseRepository[Organization],
                 team_repository: BaseRepository[Team],
                 jwt_secret: str):
        self.user_repository = user_repository
        self.organization_repository = organization_repository
        self.team_repository = team_repository
        self.jwt_secret = jwt_secret
    
    def create_user(self, email: str, name: str, password: str) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_users = self.user_repository.filter_by(email=email)
        if existing_users:
            raise ValueError(f"User with email {email} already exists")
        
        # Create new user
        user = User(
            email=email,
            name=name,
            password_hash=generate_password_hash(password)
        )
        return self.user_repository.create(user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        users = self.user_repository.filter_by(email=email)
        if not users:
            return None
        
        user = users[0]
        if not check_password_hash(user.password_hash, password):
            return None
        
        # Update last login time
        user.last_login = datetime.datetime.utcnow()
        self.user_repository.update(user)
        
        return user
    
    def generate_token(self, user: User, expiration_hours: int = 24) -> str:
        """Generate a JWT token for the user."""
        payload = {
            'user_id': str(user.id),
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify a JWT token and return the payload."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.PyJWTError:
            return None
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        users = self.user_repository.filter_by(email=email)
        return users[0] if users else None
    
    def update_user(self, user: User) -> User:
        """Update a user."""
        return self.user_repository.update(user)
    
    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user by ID."""
        return self.user_repository.delete(user_id)
    
    def create_organization(self, name: str) -> Organization:
        """Create a new organization."""
        organization = Organization(name=name)
        return self.organization_repository.create(organization)
    
    def create_team(self, organization_id: UUID, name: str, description: str = None) -> Team:
        """Create a new team within an organization."""
        organization = self.organization_repository.get_by_id(organization_id)
        if not organization:
            raise ValueError(f"Organization with ID {organization_id} not found")
        
        team = Team(
            organization_id=organization_id,
            name=name,
            description=description
        )
        return self.team_repository.create(team)
    
    def add_user_to_team(self, user_id: UUID, team_id: UUID, role: str) -> None:
        """Add a user to a team with a specific role."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        team = self.team_repository.get_by_id(team_id)
        if not team:
            raise ValueError(f"Team with ID {team_id} not found")
        
        # Check if user is already in the team
        if team in user.teams:
            raise ValueError(f"User {user.email} is already a member of team {team.name}")
        
        # Add user to team with role
        user.teams.append(team)
        # Set role in the association table
        # This requires direct SQL manipulation or ORM-specific approach
        
        self.user_repository.update(user)
