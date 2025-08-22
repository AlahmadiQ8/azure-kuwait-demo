# This file provides API endpoints for managing publisher operations in the crowd funding platform.
# It implements REST API endpoints for retrieving publisher information.

from flask import jsonify, Response
from models import db, Publisher
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

# Create a Blueprint for publishers routes
publishers_bp = APIBlueprint('publishers', __name__, abp_tags=[Tag(name='Publishers', description='Operations related to publishers')])

@publishers_bp.get('/api/publishers')
def get_publishers() -> Response:
    """Get all publishers with their ID and name information."""
    # Query all publishers from the database
    publishers = db.session.query(Publisher).all()
    
    # Convert to simplified format with only id and name
    publishers_list = [{"id": p.id, "name": p.name} for p in publishers]
    
    return jsonify(publishers_list)
