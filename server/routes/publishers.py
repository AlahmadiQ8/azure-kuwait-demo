"""
Publishers routes - API endpoints for managing publishers
"""
from flask import jsonify, Response
from models import db, Publisher
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

# Create a Blueprint for publishers routes
publishers_bp = APIBlueprint('publishers', __name__, abp_tags=[Tag(name='Publishers', description='Operations related to publishers')])

@publishers_bp.get('/api/publishers')
def get_publishers() -> Response:
    """Get all publishers with their id and name fields only."""
    # Query all publishers from database
    publishers_query = db.session.query(Publisher).all()
    
    # Convert to simple format with only id and name fields
    publishers_list = [{'id': publisher.id, 'name': publisher.name} for publisher in publishers_query]
    
    return jsonify(publishers_list)
