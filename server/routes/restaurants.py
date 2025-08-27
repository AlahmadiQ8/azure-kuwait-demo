from flask import jsonify, Response, request
from models import db, Restaurant, Publisher, Category
from sqlalchemy.orm import Query
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from werkzeug.exceptions import UnsupportedMediaType

# Create a Blueprint for restaurants routes
restaurants_bp = APIBlueprint('restaurants', __name__, abp_tags=[Tag(name='Restaurants', description='Operations related to restaurants')])

class RestaurantPathModel(BaseModel):
    """Path parameters for restaurant endpoint."""
    id: int

class RestaurantCreateModel(BaseModel):
    """Model for creating a new restaurant."""
    title: str
    description: str
    star_rating: Optional[float] = None
    category_id: int
    publisher_id: int
    
    @field_validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Title must be at least 2 characters')
        return v.strip()
    
    @field_validator('description')
    def validate_description(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Description must be at least 10 characters')
        return v.strip()
    
    @field_validator('star_rating')
    def validate_star_rating(cls, v):
        if v is not None and (v < 0 or v > 5):
            raise ValueError('Star rating must be between 0 and 5')
        return v

class RestaurantUpdateModel(BaseModel):
    """Model for updating an existing restaurant."""
    title: Optional[str] = None
    description: Optional[str] = None
    star_rating: Optional[float] = None
    category_id: Optional[int] = None
    publisher_id: Optional[int] = None
    
    @field_validator('title')
    def validate_title(cls, v):
        if v is not None and (not v or len(v.strip()) < 2):
            raise ValueError('Title must be at least 2 characters')
        return v.strip() if v else v
    
    @field_validator('description')
    def validate_description(cls, v):
        if v is not None and (not v or len(v.strip()) < 10):
            raise ValueError('Description must be at least 10 characters')
        return v.strip() if v else v
    
    @field_validator('star_rating')
    def validate_star_rating(cls, v):
        if v is not None and (v < 0 or v > 5):
            raise ValueError('Star rating must be between 0 and 5')
        return v

def get_restaurants_base_query() -> Query:
    return db.session.query(Restaurant).join(
        Publisher, 
        Restaurant.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Restaurant.category_id == Category.id, 
        isouter=True
    )

@restaurants_bp.get('/api/restaurants')
def get_restaurants() -> Response:
    """Get all restaurants with their publisher and category information."""
    # Use the base query for all restaurants
    restaurants_query = get_restaurants_base_query().all()
    
    # Convert the results using the model's to_dict method
    restaurants_list = [restaurant.to_dict() for restaurant in restaurants_query]
    
    return jsonify(restaurants_list)

@restaurants_bp.get('/api/restaurants/<int:id>')
def get_restaurant(path: RestaurantPathModel) -> tuple[Response, int] | Response:
    """Get a specific restaurant by ID with its publisher and category information."""
    # Use the base query and add filter for specific restaurant
    restaurant_query = get_restaurants_base_query().filter(Restaurant.id == path.id).first()
    
    # Return 404 if restaurant not found
    if not restaurant_query: 
        return jsonify({"error": "Restaurant not found"}), 404
    
    # Convert the result using the model's to_dict method
    restaurant = restaurant_query.to_dict()
    
    return jsonify(restaurant)

@restaurants_bp.post('/api/restaurants')
def create_restaurant() -> tuple[Response, int]:
    """Create a new restaurant."""
    try:
        # Parse and validate request data
        request_data = request.get_json()
        if request_data is None:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Validate data using Pydantic model
        restaurant_data = RestaurantCreateModel(**request_data)
        
        # Check if publisher exists
        publisher = db.session.query(Publisher).filter(Publisher.id == restaurant_data.publisher_id).first()
        if not publisher:
            return jsonify({"error": "Publisher not found"}), 400
            
        # Check if category exists
        category = db.session.query(Category).filter(Category.id == restaurant_data.category_id).first()
        if not category:
            return jsonify({"error": "Category not found"}), 400
        
        # Create new restaurant
        new_restaurant = Restaurant(
            title=restaurant_data.title,
            description=restaurant_data.description,
            star_rating=restaurant_data.star_rating,
            category_id=restaurant_data.category_id,
            publisher_id=restaurant_data.publisher_id
        )
        
        # Add to database
        db.session.add(new_restaurant)
        db.session.commit()
        
        # Return created restaurant
        created_restaurant = get_restaurants_base_query().filter(Restaurant.id == new_restaurant.id).first()
        return jsonify(created_restaurant.to_dict()), 201
        
    except UnsupportedMediaType:
        return jsonify({"error": "Request body must be JSON"}), 400
    except ValidationError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create restaurant"}), 500

@restaurants_bp.put('/api/restaurants/<int:id>')
def update_restaurant(path: RestaurantPathModel) -> tuple[Response, int]:
    """Update an existing restaurant."""
    try:
        # Parse and validate request data
        request_data = request.get_json()
        if request_data is None:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Validate data using Pydantic model
        restaurant_data = RestaurantUpdateModel(**request_data)
        
        # Find existing restaurant
        restaurant = db.session.query(Restaurant).filter(Restaurant.id == path.id).first()
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        # Check if publisher exists (if being updated)
        if restaurant_data.publisher_id is not None:
            publisher = db.session.query(Publisher).filter(Publisher.id == restaurant_data.publisher_id).first()
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 400
                
        # Check if category exists (if being updated)
        if restaurant_data.category_id is not None:
            category = db.session.query(Category).filter(Category.id == restaurant_data.category_id).first()
            if not category:
                return jsonify({"error": "Category not found"}), 400
        
        # Update restaurant fields
        if restaurant_data.title is not None:
            restaurant.title = restaurant_data.title
        if restaurant_data.description is not None:
            restaurant.description = restaurant_data.description
        if restaurant_data.star_rating is not None:
            restaurant.star_rating = restaurant_data.star_rating
        if restaurant_data.category_id is not None:
            restaurant.category_id = restaurant_data.category_id
        if restaurant_data.publisher_id is not None:
            restaurant.publisher_id = restaurant_data.publisher_id
        
        # Commit changes
        db.session.commit()
        
        # Return updated restaurant
        updated_restaurant = get_restaurants_base_query().filter(Restaurant.id == restaurant.id).first()
        return jsonify(updated_restaurant.to_dict()), 200
        
    except UnsupportedMediaType:
        return jsonify({"error": "Request body must be JSON"}), 400
    except ValidationError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update restaurant"}), 500

@restaurants_bp.delete('/api/restaurants/<int:id>')
def delete_restaurant(path: RestaurantPathModel) -> tuple[Response, int]:
    """Delete a restaurant."""
    try:
        # Find existing restaurant
        restaurant = db.session.query(Restaurant).filter(Restaurant.id == path.id).first()
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        # Delete restaurant
        db.session.delete(restaurant)
        db.session.commit()
        
        return jsonify({"message": "Restaurant deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete restaurant"}), 500
