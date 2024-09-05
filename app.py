from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the saved machine learning model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not model:
            return jsonify({'error': 'Model is not loaded. Please check the model file.'}), 500

        # Get data from the POST request
        data = request.get_json()

        # Extract only the features used in training (e.g., 4 features)
        features = np.array([[
            float(data['sub_metering_1']),
            float(data['sub_metering_2']),
            float(data['voltage']),
            float(data['global_intensity'])
        ]])

        # Perform the prediction
        prediction = model.predict(features)

        return jsonify({'predicted_energy_consumption': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
