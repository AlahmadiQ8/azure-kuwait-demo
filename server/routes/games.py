from flask import jsonify, Response
from models import db, Game, Publisher, Category
from sqlalchemy.orm import Query
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag



# Create a Blueprint for games routes
games_bp = APIBlueprint('games', __name__, abp_tags=[Tag(name='Games', description='Operations related to games')])

def get_games_base_query() -> Query:
    return db.session.query(Game).join(
        Publisher, 
        Game.publisher_id == Publisher.id, 
        isouter=True
    ).join(
        Category, 
        Game.category_id == Category.id, 
        isouter=True
    )

@games_bp.get('/api/games')
def get_games() -> Response:
    """Get all games with their publisher and category information."""
    # Use the base query for all games
    games_query = get_games_base_query().all()
    
    # Convert the results using the model's to_dict method
    games_list = [game.to_dict() for game in games_query]
    
    return jsonify(games_list)

@games_bp.get('/api/games/<int:id>')
def get_game(id: int) -> tuple[Response, int] | Response:
    # Use the base query and add filter for specific game
    game_query = get_games_base_query().filter(Game.id == id).first()
    
    # Return 404 if game not found
    if not game_query: 
        return jsonify({"error": "Game not found"}), 404
    
    # Convert the result using the model's to_dict method
    game = game_query.to_dict()
    
    return jsonify(game)
