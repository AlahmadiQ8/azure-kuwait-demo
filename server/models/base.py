# Base model class providing common functionality for all database models.
# This module defines the BaseModel abstract class that serves as the foundation
# for all SQLAlchemy models in the application, providing common validation utilities.

from . import db

class BaseModel(db.Model):
    """Abstract base model class for all database models.
    
    Provides common functionality and validation methods that can be used
    by all model classes in the application.
    """
    __abstract__ = True
    
    @staticmethod
    def validate_string_length(field_name: str, value: str, min_length: int = 2, allow_none: bool = False) -> str:
        """Validate the length of a string field.
        
        Args:
            field_name: The name of the field being validated (for error messages)
            value: The string value to validate
            min_length: The minimum allowed length (defaults to 2)
            allow_none: Whether to allow None values (defaults to False)
            
        Returns:
            The validated string value
            
        Raises:
            ValueError: If the value is None and not allowed, not a string,
                       or shorter than the minimum length
        """
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value