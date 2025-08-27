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

    def test_create_restaurant_success(self) -> None:
        """Test successful creation of a new restaurant"""
        # Arrange
        new_restaurant_data = {
            "title": "New Test Restaurant",
            "description": "A fantastic new restaurant for testing purposes",
            "star_rating": 4.8,
            "category_id": 1,
            "publisher_id": 1
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(new_restaurant_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['title'], new_restaurant_data['title'])
        self.assertEqual(data['description'], new_restaurant_data['description'])
        self.assertEqual(data['starRating'], new_restaurant_data['star_rating'])
        self.assertIsNotNone(data['id'])
        self.assertIsNotNone(data['publisher'])
        self.assertIsNotNone(data['category'])

    def test_create_restaurant_missing_required_fields(self) -> None:
        """Test creation with missing required fields"""
        # Arrange
        incomplete_data = {
            "title": "Incomplete Restaurant"
            # Missing description, category_id, publisher_id
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_create_restaurant_invalid_title(self) -> None:
        """Test creation with invalid title (too short)"""
        # Arrange
        invalid_data = {
            "title": "A",  # Too short
            "description": "A restaurant with invalid title",
            "category_id": 1,
            "publisher_id": 1
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn('Title must be at least 2 characters', data['error'])

    def test_create_restaurant_invalid_description(self) -> None:
        """Test creation with invalid description (too short)"""
        # Arrange
        invalid_data = {
            "title": "Valid Title",
            "description": "Short",  # Too short
            "category_id": 1,
            "publisher_id": 1
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn('Description must be at least 10 characters', data['error'])

    def test_create_restaurant_invalid_star_rating(self) -> None:
        """Test creation with invalid star rating (out of range)"""
        # Arrange
        invalid_data = {
            "title": "Valid Title",
            "description": "Valid description for this restaurant",
            "star_rating": 6.0,  # Out of range (0-5)
            "category_id": 1,
            "publisher_id": 1
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn('Star rating must be between 0 and 5', data['error'])

    def test_create_restaurant_nonexistent_publisher(self) -> None:
        """Test creation with nonexistent publisher ID"""
        # Arrange
        invalid_data = {
            "title": "Valid Title",
            "description": "Valid description for this restaurant",
            "category_id": 1,
            "publisher_id": 999  # Nonexistent
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Publisher not found")

    def test_create_restaurant_nonexistent_category(self) -> None:
        """Test creation with nonexistent category ID"""
        # Arrange
        invalid_data = {
            "title": "Valid Title",
            "description": "Valid description for this restaurant",
            "category_id": 999,  # Nonexistent
            "publisher_id": 1
        }
        
        # Act
        response = self.client.post(
            self.RESTAURANTS_API_PATH,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Category not found")

    def test_create_restaurant_no_json_body(self) -> None:
        """Test creation with no JSON body"""
        # Act
        response = self.client.post(self.RESTAURANTS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Request body must be JSON")

    def test_update_restaurant_success(self) -> None:
        """Test successful update of an existing restaurant"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        
        # Arrange update data
        update_data = {
            "title": "Updated Restaurant Name",
            "star_rating": 4.9
        }
        
        # Act
        response = self.client.put(
            f'{self.RESTAURANTS_API_PATH}/{restaurant_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], update_data['title'])
        self.assertEqual(data['starRating'], update_data['star_rating'])

    def test_update_restaurant_partial_update(self) -> None:
        """Test partial update of restaurant (only one field)"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        original_title = restaurants[0]['title']
        
        # Arrange update data (only description)
        update_data = {
            "description": "This is an updated description for the restaurant"
        }
        
        # Act
        response = self.client.put(
            f'{self.RESTAURANTS_API_PATH}/{restaurant_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], original_title)  # Title should remain unchanged
        self.assertEqual(data['description'], update_data['description'])

    def test_update_restaurant_not_found(self) -> None:
        """Test update of non-existent restaurant"""
        # Arrange
        update_data = {
            "title": "Updated Restaurant Name"
        }
        
        # Act
        response = self.client.put(
            f'{self.RESTAURANTS_API_PATH}/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], "Restaurant not found")

    def test_update_restaurant_invalid_title(self) -> None:
        """Test update with invalid title"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        
        # Arrange invalid update data
        update_data = {
            "title": "A"  # Too short
        }
        
        # Act
        response = self.client.put(
            f'{self.RESTAURANTS_API_PATH}/{restaurant_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn('Title must be at least 2 characters', data['error'])

    def test_update_restaurant_nonexistent_publisher(self) -> None:
        """Test update with nonexistent publisher ID"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        
        # Arrange invalid update data
        update_data = {
            "publisher_id": 999  # Nonexistent
        }
        
        # Act
        response = self.client.put(
            f'{self.RESTAURANTS_API_PATH}/{restaurant_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Publisher not found")

    def test_update_restaurant_no_json_body(self) -> None:
        """Test update with no JSON body"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        
        # Act
        response = self.client.put(f'{self.RESTAURANTS_API_PATH}/{restaurant_id}')
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "Request body must be JSON")

    def test_delete_restaurant_success(self) -> None:
        """Test successful deletion of a restaurant"""
        # Get the first restaurant's ID from the list endpoint
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        restaurant_id = restaurants[0]['id']
        original_count = len(restaurants)
        
        # Act
        response = self.client.delete(f'{self.RESTAURANTS_API_PATH}/{restaurant_id}')
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Restaurant deleted successfully")
        
        # Verify restaurant is actually deleted
        response = self.client.get(self.RESTAURANTS_API_PATH)
        restaurants = self._get_response_data(response)
        self.assertEqual(len(restaurants), original_count - 1)

    def test_delete_restaurant_not_found(self) -> None:
        """Test deletion of non-existent restaurant"""
        # Act
        response = self.client.delete(f'{self.RESTAURANTS_API_PATH}/999')
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], "Restaurant not found")

if __name__ == '__main__':
    unittest.main()