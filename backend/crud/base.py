"""
Base CRUD operations for MediFlow OS
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from database.connection import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """
    Base class for CRUD operations
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with a specific model
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Model instance or None
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_all(self, db: Session) -> List[ModelType]:
        """
        Get all records
        
        Args:
            db: Database session
            
        Returns:
            List of all model instances
        """
        return db.query(self.model).all()
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new record
        
        Args:
            db: Database session
            obj_in: Dictionary of field values
            
        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        """
        Update an existing record
        
        Args:
            db: Database session
            db_obj: Existing model instance
            obj_in: Dictionary of field values to update
            
        Returns:
            Updated model instance
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        Delete a record by ID
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Deleted model instance or None
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def count(self, db: Session) -> int:
        """
        Count total records
        
        Args:
            db: Database session
            
        Returns:
            Total count
        """
        return db.query(self.model).count()

# Made with Bob
