from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Category(BaseModel):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one category has many restaurants
    restaurants = relationship("Restaurant", back_populates="category")
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate category name field.
        
        Args:
            key (str): The field name being validated
            name (str): The name value to validate
            
        Returns:
            str: The validated name value
        """
        return self.validate_string_length('Category name', name, min_length=2)
        
    @validates('description')
    def validate_description(self, key, description):
        """Validate category description field.
        
        Args:
            key (str): The field name being validated
            description (str): The description value to validate
            
        Returns:
            str: The validated description value
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)
    
    def __repr__(self):
        """Return string representation of the category.
        
        Returns:
            str: String representation including category name
        """
        return f'<Category {self.name}>'
        
    def to_dict(self):
        """Convert category instance to dictionary format.
        
        Returns:
            dict: Dictionary representation of the category with all fields
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'restaurant_count': len(self.restaurants) if self.restaurants else 0
        }