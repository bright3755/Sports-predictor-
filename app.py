from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    d = request.json
    home_score = d['home_goals']*0.6 + d['home_shots']*0.05 + d['home_sot']*0.1
    away_score = d['away_goals']*0.6 + d['away_shots']*0.05 + d['away_sot']*0.1
    diff = home_score - away_score
    if diff > 0.4:
        pred, conf, ph, pd, pa = "Home Win", 65, 65, 10, 25
    elif diff < -0.4:
        pred, conf, ph, pd, pa = "Away Win", 62, 25, 13, 62
    else:
        pred, conf, ph, pd, pa = "Draw", 55, 35, 30, 35
    return jsonify({"prediction": pred, "confidence": conf, "probabilities": {"home": ph, "draw": pd, "away": pa}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
