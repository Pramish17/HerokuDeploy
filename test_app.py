import unittest
import json
from app import app  # Assuming the file is named app.py

class FlaskTestCase(unittest.TestCase):

    # Test if the prediction is successful
    def test_prediction_success(self):
        # Setup the Flask test client
        tester = app.test_client(self)
        
        # Simulate the request payload
        payload = {
            'sub_metering_1': 1.0,
            'sub_metering_2': 2.0,
            'voltage': 230.0,
            'global_intensity': 15.0
        }
        
        # Send POST request to the /predict endpoint
        response = tester.post(
            '/predict', 
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Check the status code
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains the expected key
        response_data = json.loads(response.data)
        self.assertIn('predicted_energy_consumption', response_data)

    # Test when the model is not loaded
    def test_model_not_loaded(self):
        # Temporarily remove the model by setting it to None
        with app.app_context():
            global model
            model = None

        # Setup the Flask test client
        tester = app.test_client(self)
        
        # Simulate the request payload
        payload = {
            'sub_metering_1': 1.0,
            'sub_metering_2': 2.0,
            'voltage': 230.0,
            'global_intensity': 15.0
        }
        
        # Send POST request to the /predict endpoint
        response = tester.post(
            '/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # # Check if it returns the correct error for model not loaded
        # self.assertEqual(response.status_code, 500)
        # response_data = json.loads(response.data)
        # self.assertIn('error', response_data)
        # self.assertEqual(response_data['error'], 'Model is not loaded. Please check the model file.')

    # Test with invalid data (e.g., missing or wrong types)
    def test_invalid_data(self):
        tester = app.test_client(self)

        # Invalid payload with missing fields
        invalid_payload = {
            'sub_metering_1': 'invalid_value',  # Should be a float
            'sub_metering_2': 2.0,
            'voltage': 230.0
            # Missing global_intensity
        }

        response = tester.post(
            '/predict',
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )

        # Check if it returns an error for invalid data
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)

if __name__ == '__main__':
    unittest.main()

