# This file contains the API routes for publisher-related operations.
# It provides endpoints to retrieve publisher information for the Kuwait Fine Dining platform.

from flask import jsonify, Response
from models import db, Publisher
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

# Create a Blueprint for publishers routes
publishers_bp = APIBlueprint('publishers', __name__, abp_tags=[Tag(name='Publishers', description='Operations related to publishers')])

@publishers_bp.get('/api/publishers')
def get_publishers() -> Response:
    """Get all publishers with their id and name information.
    
    Returns:
        Response: JSON array of publisher objects containing id and name fields
    """
    # Query all publishers from the database
    publishers_query = db.session.query(Publisher).all()
    
    # Convert to simplified format with only id and name
    publishers_list = [
        {
            'id': publisher.id,
            'name': publisher.name
        }
        for publisher in publishers_query
    ]
    
    return jsonify(publishers_list)
