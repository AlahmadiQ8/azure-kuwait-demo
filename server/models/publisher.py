# Publisher model for the Kuwait Fine Dining directory application.
# This module defines the Publisher SQLAlchemy model that represents restaurant
# publishers with validation methods and relationships to Restaurant models.

from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    """Model representing a restaurant publisher.
    
    Publishers are organizations or entities that manage restaurants
    in the Kuwait Fine Dining directory.
    """
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many restaurants
    restaurants = relationship("Restaurant", back_populates="publisher")

    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """Validate the publisher name field.
        
        Args:
            key: The field name being validated
            name: The publisher name to validate
            
        Returns:
            The validated name string
            
        Raises:
            ValueError: If the name is invalid (too short, empty, etc.)
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key: str, description: str) -> str:
        """Validate the publisher description field.
        
        Args:
            key: The field name being validated
            description: The description value to validate
            
        Returns:
            The validated description string or None
            
        Raises:
            ValueError: If the description is invalid when provided
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self) -> str:
        """Return a string representation of the Publisher object.
        
        Returns:
            A formatted string with publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self) -> dict:
        """Convert the Publisher object to a dictionary representation.
        
        Returns:
            A dictionary containing the publisher data including
            the count of associated restaurants
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'restaurant_count': len(self.restaurants) if self.restaurants else 0
        }