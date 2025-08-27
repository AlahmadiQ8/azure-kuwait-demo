from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many restaurants
    restaurants = relationship("Restaurant", back_populates="publisher")

    @validates('name')
    def validate_name(self, key, name):
        """Validate publisher name field.
        
        Args:
            key (str): The field name being validated
            name (str): The name value to validate
            
        Returns:
            str: The validated name value
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        """Validate publisher description field.
        
        Args:
            key (str): The field name being validated
            description (str): The description value to validate
            
        Returns:
            str: The validated description value
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        """Return string representation of the publisher.
        
        Returns:
            str: String representation including publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self):
        """Convert publisher instance to dictionary format.
        
        Returns:
            dict: Dictionary representation of the publisher with all fields
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'restaurant_count': len(self.restaurants) if self.restaurants else 0
        }