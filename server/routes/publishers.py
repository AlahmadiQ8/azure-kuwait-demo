from flask import jsonify, Response
from models import db, Publisher
from sqlalchemy.orm import Query
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

# Create a Blueprint for publishers routes
publishers_bp = APIBlueprint('publishers', __name__, abp_tags=[Tag(name='Publishers', description='Operations related to publishers')])

def get_publishers_base_query() -> Query:
    """Get base query for publishers."""
    return db.session.query(Publisher)

@publishers_bp.get('/api/publishers')
def get_publishers() -> Response:
    """Get all publishers with their id and name only."""
    # Get all publishers using the base query
    publishers_query = get_publishers_base_query().all()
    
    # Convert the results to return only id and name as required
    publishers_list = [{'id': publisher.id, 'name': publisher.name} for publisher in publishers_query]
    
    return jsonify(publishers_list)
