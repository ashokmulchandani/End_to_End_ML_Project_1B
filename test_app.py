import unittest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestBostonHousePricing(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Test home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'html', response.data.lower())
    
    def test_predict_api_valid_data(self):
        """Test prediction API with valid data"""
        test_data = {
            "data": {
                "CRIM": 0.00632,
                "ZN": 18.0,
                "INDUS": 2.31,
                "CHAS": 0,
                "NOX": 0.538,
                "RM": 6.575,
                "AGE": 65.2,
                "DIS": 4.0900,
                "RAD": 1,
                "TAX": 296,
                "PTRATIO": 15.3,
                "B": 396.90,
                "LSTAT": 4.98
            }
        }
        
        response = self.app.post('/predict_api',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        # Check if response is a valid number
        result = json.loads(response.data)
        self.assertIsInstance(result, (int, float))
        self.assertGreater(result, 0)  # House price should be positive
    
    def test_predict_api_invalid_data(self):
        """Test prediction API with invalid data"""
        test_data = {"invalid": "data"}
        
        response = self.app.post('/predict_api',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        # Should return error (500 or 400)
        self.assertIn(response.status_code, [400, 500])
    
    def test_predict_form_valid_data(self):
        """Test prediction form with valid data"""
        form_data = {
            'CRIM': '0.00632',
            'ZN': '18.0',
            'INDUS': '2.31',
            'CHAS': '0',
            'NOX': '0.538',
            'RM': '6.575',
            'AGE': '65.2',
            'DIS': '4.0900',
            'RAD': '1',
            'TAX': '296',
            'PTRATIO': '15.3',
            'B': '396.90',
            'LSTAT': '4.98'
        }
        
        response = self.app.post('/predict', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'prediction', response.data.lower())

if __name__ == '__main__':
    unittest.main()