# Main Flask application entry point for the Kuwait Fine Dining directory.
# This module initializes the Flask application using OpenAPI, configures the database,
# and registers API blueprints for restaurant management functionality.

import os
from models import init_db
from routes.restaurants import restaurants_bp
from utils.database import init_db
from flask_openapi3.openapi import OpenAPI

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app = OpenAPI(__name__)

# Initialize the database with the app
init_db(app)

# Register blueprints
app.register_api(restaurants_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5100) # Port 5100 to avoid macOS conflicts