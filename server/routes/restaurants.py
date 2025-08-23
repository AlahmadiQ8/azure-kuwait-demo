from flask import jsonify, Response, request
from models import db, Restaurant, Publisher, Category
from sqlalchemy.orm import Query
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.exc import IntegrityError

# Create a Blueprint for restaurants routes
restaurants_bp = APIBlueprint('restaurants', __name__, abp_tags=[Tag(name='Restaurants', description='Operations related to restaurants')])

class RestaurantPathModel(BaseModel):
    """Path parameters for restaurant endpoint."""
    id: int

class RestaurantCreateModel(BaseModel):
    """Request body model for creating a restaurant."""
    title: str
    description: str
    category_id: int
    publisher_id: int
    star_rating: Optional[float] = None

class RestaurantUpdateModel(BaseModel):
    """Request body model for updating a restaurant."""
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    publisher_id: Optional[int] = None
    star_rating: Optional[float] = None

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
def create_restaurant(body: RestaurantCreateModel) -> tuple[Response, int]:
    """Create a new restaurant."""
    try:
        # Validate that publisher exists
        publisher = db.session.query(Publisher).filter(Publisher.id == body.publisher_id).first()
        if not publisher:
            return jsonify({"error": "Publisher not found"}), 400
            
        # Validate that category exists
        category = db.session.query(Category).filter(Category.id == body.category_id).first()
        if not category:
            return jsonify({"error": "Category not found"}), 400
        
        # Create new restaurant
        new_restaurant = Restaurant(
            title=body.title,
            description=body.description,
            category_id=body.category_id,
            publisher_id=body.publisher_id,
            star_rating=body.star_rating
        )
        
        db.session.add(new_restaurant)
        db.session.commit()
        
        # Return the created restaurant using base query to include relationships
        created_restaurant = get_restaurants_base_query().filter(Restaurant.id == new_restaurant.id).first()
        return jsonify(created_restaurant.to_dict()), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@restaurants_bp.put('/api/restaurants/<int:id>')
def update_restaurant(path: RestaurantPathModel, body: RestaurantUpdateModel) -> tuple[Response, int] | Response:
    """Update an existing restaurant."""
    try:
        # Find the restaurant to update
        restaurant = db.session.query(Restaurant).filter(Restaurant.id == path.id).first()
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        # Validate publisher if provided
        if body.publisher_id is not None:
            publisher = db.session.query(Publisher).filter(Publisher.id == body.publisher_id).first()
            if not publisher:
                return jsonify({"error": "Publisher not found"}), 400
        
        # Validate category if provided
        if body.category_id is not None:
            category = db.session.query(Category).filter(Category.id == body.category_id).first()
            if not category:
                return jsonify({"error": "Category not found"}), 400
        
        # Update only provided fields
        if body.title is not None:
            restaurant.title = body.title
        if body.description is not None:
            restaurant.description = body.description
        if body.category_id is not None:
            restaurant.category_id = body.category_id
        if body.publisher_id is not None:
            restaurant.publisher_id = body.publisher_id
        if body.star_rating is not None:
            restaurant.star_rating = body.star_rating
        
        db.session.commit()
        
        # Return the updated restaurant using base query to include relationships
        updated_restaurant = get_restaurants_base_query().filter(Restaurant.id == restaurant.id).first()
        return jsonify(updated_restaurant.to_dict())
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

@restaurants_bp.delete('/api/restaurants/<int:id>')
def delete_restaurant(path: RestaurantPathModel) -> tuple[Response, int]:
    """Delete a restaurant."""
    try:
        # Find the restaurant to delete
        restaurant = db.session.query(Restaurant).filter(Restaurant.id == path.id).first()
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        
        db.session.delete(restaurant)
        db.session.commit()
        
        return jsonify({"message": "Restaurant deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
