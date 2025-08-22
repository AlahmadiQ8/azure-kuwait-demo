from flask import jsonify, Response
from models import db, Restaurant, Publisher, Category
from sqlalchemy.orm import Query
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from pydantic import BaseModel

# Create a Blueprint for restaurants routes
restaurants_bp = APIBlueprint('restaurants', __name__, abp_tags=[Tag(name='Restaurants', description='Operations related to restaurants')])

class RestaurantPathModel(BaseModel):
    """Path parameters for restaurant endpoint."""
    id: int

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
