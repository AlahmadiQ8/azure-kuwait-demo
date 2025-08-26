# Restaurant model for the Kuwait Fine Dining directory application.
# This module defines the Restaurant SQLAlchemy model with validation methods
# and relationships to Publisher and Category models.

from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Restaurant(BaseModel):
    """Model representing a restaurant in the Kuwait Fine Dining directory.
    
    This class defines the structure and validation rules for restaurant entities,
    including relationships to Publisher and Category models, and methods for
    data validation and serialization.
    """
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Float, nullable=True)
    
    # Foreign keys for one-to-many relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    
    # One-to-many relationships (many restaurants belong to one category/publisher)
    category = relationship("Category", back_populates="restaurants")
    publisher = relationship("Publisher", back_populates="restaurants")
    
    @validates('title')
    def validate_name(self, key: str, name: str) -> str:
        """Validate the restaurant title field.
        
        Args:
            key: The field name being validated
            name: The title value to validate
            
        Returns:
            The validated title string
            
        Raises:
            ValueError: If the title is invalid (too short, empty, etc.)
        """
        return self.validate_string_length('Restaurant title', name, min_length=2)
    
    @validates('description')
    def validate_description(self, key: str, description: str) -> str:
        """Validate the restaurant description field.
        
        Args:
            key: The field name being validated
            description: The description value to validate
            
        Returns:
            The validated description string or None
            
        Raises:
            ValueError: If the description is invalid when provided
        """
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self) -> str:
        """Return a string representation of the Restaurant object.
        
        Returns:
            A formatted string with restaurant title and ID
        """
        return f'<Restaurant {self.title}, ID: {self.id}>'

    def to_dict(self) -> dict:
        """Convert the Restaurant object to a dictionary representation.
        
        Returns:
            A dictionary containing the restaurant data including
            associated publisher and category information
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publisher': {'id': self.publisher.id, 'name': self.publisher.name} if self.publisher else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'starRating': self.star_rating  # Changed from star_rating to starRating
        }