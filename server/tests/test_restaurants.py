# Unit tests for restaurant API routes in the Kuwait Fine Dining directory application.
# This module contains comprehensive test cases for the restaurant endpoints,
# validating API responses, data structure, and error handling.

import unittest
import json
from typing import Dict, List, Any, Optional
from flask import Flask, Response
from models import Restaurant, Publisher, Category, db, init_db
from routes.restaurants import restaurants_bp

class TestRestaurantsRoutes(unittest.TestCase):
    # Test data as complete objects
    TEST_DATA: Dict[str, Any] = {
        "publishers": [
            {"name": "Alghaner Group"},
            {"name": "Mais Alghanem"}
        ],
        "categories": [
            {"name": "Lebanese"},
            {"name": "Japanese"}
        ],
        "restaurants": [
            {
                "title": "Mais Alghanim",
                "description": "Renowned Lebanese-Arabic grill spot near Kuwait Towers, rated 4.5 on Talabat with popular dishes like Tabouleh, Hummus, Family Savers Meal and Arayes meat.",
                "publisher_index": 0,
                "category_index": 0,
                "star_rating": 4.5
            },
            {
                "title": "White Robata",
                "description": "Highly rated at Wanderlog for charcoal-grilled Japanese fusion dishes in a sleek setting at Sheikh Jaber Al-Ahmed Cultural Centre",
                "publisher_index": 1,
                "category_index": 1,
                "star_rating": 4.2
            }
        ]
    }
    
    # API paths
    RESTAURANTS_API_PATH: str = '/api/restaurants'

    def setUp(self) -> None:
        """Set up test database and seed data"""
        # Create a fresh Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Register the restaurants blueprint
        self.app.register_blueprint(restaurants_bp)
        
        # Initialize the test client
        self.client = self.app.test_client()
        
        # Initialize in-memory database for testing
        init_db(self.app, testing=True)
        
        # Create tables and seed data
        with self.app.app_context():
            db.create_all()
            self._seed_test_data()

    def tearDown(self) -> None:
        """Clean up test database and ensure proper connection closure"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _seed_test_data(self) -> None:
        """Helper method to seed test data"""
        # Create test publishers
        publishers = [
            Publisher(**publisher_data) for publisher_data in self.TEST_DATA["publishers"]
        ]
        db.session.add_all(publishers)
        
        # Create test categories
        categories = [
            Category(**category_data) for category_data in self.TEST_DATA["categories"]
        ]
        db.session.add_all(categories)
        
        # Commit to get IDs
        db.session.commit()
        
        # Create test restaurants
        restaurants = []
        for restaurant_data in self.TEST_DATA["restaurants"]:
            restaurant_dict = restaurant_data.copy()
            publisher_index = restaurant_dict.pop("publisher_index")
            category_index = restaurant_dict.pop("category_index")
            
            restaurants.append(Restaurant(
                **restaurant_dict,
                publisher=publishers[publisher_index],
                category=categories[category_index]
            ))
            
        db.session.add_all(restaurants)
        db.session.commit()

    def _get_response_data(self, response: Response) -> Any:
        """Helper method to parse response data"""
        return json.loads(response.data)

    def test_get_restaurant_success(self) -> None:
        """Test successful retrieval of multiple restaurants"""
        # Act
        response = self.client.get(self.RESTAURANTS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self.TEST_DATA["restaurants"]))
        
        # Verify all restaurants using loop instead of manual testing
        for i, restaurant_data in enumerate(data):
            test_restaurant = self.TEST_DATA["restaurants"][i]
            test_publisher = self.TEST_DATA["publishers"][test_restaurant["publisher_index"]]
            test_category = self.TEST_DATA["categories"][test_restaurant["category_index"]]
            
            self.assertEqual(restaurant_data['title'], test_restaurant["title"])
            self.assertEqual(restaurant_data['publisher']['name'], test_publisher["name"])
            self.assertEqual(restaurant_data['category']['name'], test_category["name"])
            self.assertEqual(restaurant_data['starRating'], test_restaurant["star_rating"])

    def test_get_restaurant_structure(self) -> None:
        """Test the response structure for restaurants"""
        # Act
        response = self.client.get(self.RESTAURANTS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA["restaurants"]))
        
        required_fields = ['id', 'title', 'description', 'publisher', 'category', 'starRating']
        for field in required_fields:
            self.assertIn(field, data[0])

    def test_get_restaurant_by_id_success(self) -> None:
        """Test successful retrieval of a single restaurant by ID"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        
        # Act
        response = self.client.get(f'{self.RESTAURANTS_API_PATH}/{restaurant_id}')
        data = self._get_response_data(response)
        
        # Assert
        first_restaurant = self.TEST_DATA["restaurants"][0]
        first_publisher = self.TEST_DATA["publishers"][first_restaurant["publisher_index"]]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], first_restaurant["title"])
        self.assertEqual(data['publisher']['name'], first_publisher["name"])
        
    def test_get_restaurant_by_id_not_found(self) -> None:
        """Test retrieval of a non-existent restaurant by ID"""
        # Act
        response = self.client.get(f'{self.RESTAURANTS_API_PATH}/999')
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], "Restaurant not found")

if __name__ == '__main__':
    unittest.main()