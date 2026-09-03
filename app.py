from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "TS Predictor is running",
        "how_to_use": "POST JSON to /predict"
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Please send JSON with Content-Type: application/json"}), 400
    
    # Example logic - replace with your real model later
    try:
        value = float(data.get('value', 0))
        result = value * 1.5  # dummy prediction
        return jsonify({"prediction": result, "input_received": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
