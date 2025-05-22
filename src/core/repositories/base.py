"""
Base repository interface and implementation for the Cloud Cost Optimizer.
"""
from typing import TypeVar, Generic, List, Optional, Type, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """Base repository interface for database operations."""
    
    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class
    
    def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get entity by ID."""
        return self.session.query(self.model_class).filter(self.model_class.id == entity_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        return self.session.query(self.model_class).offset(skip).limit(limit).all()
    
    def create(self, entity: T) -> T:
        """Create a new entity."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def delete(self, entity_id: UUID) -> bool:
        """Delete an entity by ID."""
        entity = self.get_by_id(entity_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False
    
    def filter_by(self, **kwargs) -> List[T]:
        """Filter entities by attributes."""
        return self.session.query(self.model_class).filter_by(**kwargs).all()
    
    def count(self) -> int:
        """Count total entities."""
        return self.session.query(self.model_class).count()
