#!/usr/bin/env python3
"""
Basic tests for the movie recommendation app
"""
import os
import sys
import unittest
import tempfile
from unittest.mock import patch, MagicMock

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables before importing app
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["DEBUG"] = "False"

from app import app, validate_user_input, init_database

class TestMovieRecommendationApp(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        app.config['DATABASE_URL'] = self.temp_db.name
        
        self.client = self.app.test_client()
        
        # Initialize database
        init_database()
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_validate_user_input_valid(self):
        """Test input validation with valid input"""
        result = validate_user_input("Hello, recommend me a movie!")
        self.assertIsNotNone(result)
        self.assertIn("recommend", result)
    
    def test_validate_user_input_empty(self):
        """Test input validation with empty input"""
        result = validate_user_input("")
        self.assertIsNone(result)
        
        result = validate_user_input("   ")
        self.assertIsNone(result)
    
    def test_validate_user_input_too_long(self):
        """Test input validation with overly long input"""
        long_input = "A" * 1500  # Exceeds 1000 char limit
        result = validate_user_input(long_input)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1000)
    
    def test_validate_user_input_special_chars(self):
        """Test input validation with special characters"""
        result = validate_user_input("<script>alert('test')</script>")
        self.assertIsNotNone(result)
        # Should be escaped
        self.assertNotIn("<script>", result)
    
    def test_home_page_get(self):
        """Test GET request to home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Recommendation', response.data)
    
    def test_home_page_post_empty(self):
        """Test POST request with empty message"""
        response = self.client.post('/', data={'message': ''})
        self.assertEqual(response.status_code, 200)
    
    @patch('app.client')
    def test_home_page_post_with_message(self, mock_client):
        """Test POST request with valid message"""
        # Mock the OpenAI client response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "I recommend watching Inception!"
        mock_client.chat.completions.create.return_value = mock_response
        
        response = self.client.post('/', data={'message': 'Recommend a sci-fi movie'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inception', response.data)
    
    @patch('app.client')
    def test_api_error_handling(self, mock_client):
        """Test handling of API errors"""
        # Mock an API error
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        response = self.client.post('/', data={'message': 'Recommend a movie'})
        self.assertEqual(response.status_code, 200)
        # Should contain error message
        self.assertIn(b'trouble processing', response.data)

if __name__ == '__main__':
    unittest.main()