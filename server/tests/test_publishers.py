import unittest
import json
from typing import Dict, List, Any, Optional
from flask import Flask, Response
from models import Publisher, db, init_db
from routes.publishers import publishers_bp

class TestPublishersRoutes(unittest.TestCase):
    # Test data as complete objects
    TEST_DATA: Dict[str, Any] = {
        "publishers": [
            {"name": "Alghaner Group", "description": "A leading restaurant group in Kuwait"},
            {"name": "Mais Alghanem", "description": "Premium dining experiences in Kuwait"}
        ]
    }
    
    # API paths
    PUBLISHERS_API_PATH: str = '/api/publishers'

    def setUp(self) -> None:
        """Set up test database and seed data"""
        # Create a fresh Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Register the publishers blueprint
        self.app.register_blueprint(publishers_bp)
        
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
        db.session.commit()

    def _get_response_data(self, response: Response) -> Any:
        """Helper method to parse response data"""
        return json.loads(response.data)

    def test_get_publishers_success(self) -> None:
        """Test successful retrieval of multiple publishers"""
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self.TEST_DATA["publishers"]))
        
        # Verify all publishers using loop
        for i, publisher_data in enumerate(data):
            test_publisher = self.TEST_DATA["publishers"][i]
            self.assertEqual(publisher_data['name'], test_publisher["name"])
            # Ensure only id and name are returned (not description)
            self.assertIn('id', publisher_data)
            self.assertIn('name', publisher_data)
            self.assertNotIn('description', publisher_data)
            self.assertNotIn('restaurant_count', publisher_data)

    def test_get_publishers_structure(self) -> None:
        """Test the response structure for publishers"""
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA["publishers"]))
        
        # Verify required fields - only id and name as specified
        required_fields = ['id', 'name']
        for publisher in data:
            for field in required_fields:
                self.assertIn(field, publisher)
            # Ensure no extra fields are returned
            self.assertEqual(len(publisher.keys()), 2)

    def test_get_publishers_empty_database(self) -> None:
        """Test publishers endpoint returns empty array when no publishers exist"""
        # Clear the database
        with self.app.app_context():
            db.session.query(Publisher).delete()
            db.session.commit()
        
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_get_publishers_data_types(self) -> None:
        """Test that publishers endpoint returns correct data types"""
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        
        if len(data) > 0:
            publisher = data[0]
            self.assertIsInstance(publisher['id'], int)
            self.assertIsInstance(publisher['name'], str)

if __name__ == '__main__':
    unittest.main()