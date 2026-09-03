from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# This is the whole website + API in one file
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Football Predictor</title>
<style>
body{font-family:Arial; background:#0f172a; color:white; padding:20px}
.card{background:#1e293b; padding:20px; border-radius:15px; max-width:500px; margin:auto}
input,button{width:100%; padding:12px; margin:8px 0; border-radius:8px; border:none}
input{background:#334155; color:white}
button{background:#22c55e; color:black; font-weight:bold; font-size:16px}
.result{background:#0f172a; padding:15px; border-radius:10px; margin-top:15px; display:none}
</style>
</head>
<body>
<div class="card">
<h2>⚽ Universal Football Predictor</h2>
<input id="home" placeholder="Home Team (e.g Man City)">
<input id="away" placeholder="Away Team (e.g Arsenal)">
<input id="hform" placeholder="Home last 5 goals (e.g 2,1,3,0,2)">
<input id="aform" placeholder="Away last 5 goals (e.g 1,1,0,2,1)">
<button onclick="predict()">PREDICT MATCH</button>
<div id="res" class="result"></div>
</div>
<script>
async function predict(){
  const home = document.getElementById('home').value;
  const away = document.getElementById('away').value;
  const hform = document.getElementById('hform').value.split(',').map(Number);
  const aform = document.getElementById('aform').value.split(',').map(Number);

  const r = await fetch('/predict', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({home_team:home, away_team:away, home_form:hform, away_form:aform})
  });
  const data = await r.json();
  const div = document.getElementById('res');
  div.style.display='block';
  div.innerHTML = `
    <h3>${data.match}</h3>
    <p><b>Winner:</b> ${data.winner} (${data.confidence})</p>
    <p><b>Double Chance:</b> ${data.double_chance}</p>
    <p><b>Goals:</b> ${data.goals}</p>
    <p><b>BTTS:</b> ${data.btts}</p>
  `;
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/predict', methods=['POST'])
def predict():
    d = request.get_json()
    h = d.get('home_team','Home')
    a = d.get('away_team','Away')
    hf = d.get('home_form',[1,1,1])
    af = d.get('away_form',[1,1,1])

    ha = sum(hf)/len(hf) if hf else 1
    aa = sum(af)/len(af) if af else 1
    diff = ha - aa
    total = ha + aa

    if diff > 0.6: winner = f"{h} WIN"; dc="1X"; conf="72%"
    elif diff < -0.6: winner = f"{a} WIN"; dc="X2"; conf="70%"
    else: winner = "DRAW"; dc="1X or X2"; conf="58%"

    goals = "Over 2.5" if total > 2.4 else "Over 1.5" if total > 1.5 else "Under 1.5"
    btts = "YES" if ha>0.8 and aa>0.8 else "NO"

    return jsonify({
        "match": f"{h} vs {a}",
        "winner": winner,
        "double_chance": dc,
        "goals": goals,
        "btts": btts,
        "confidence": conf
    })

if __name__ == '__main__':
    app.run()
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/predict', methods=['POST'])
def predict():
    d = request.get_json()
    h = d.get('home_team','Home')
    a = d.get('away_team','Away')
    hf = d.get('home_form',[1,1,1])
    af = d.get('away_form',[1,1,1])

    ha = sum(hf)/len(hf) if hf else 1
    aa = sum(af)/len(af) if af else 1
    diff = ha - aa
    total = ha + aa

    if diff > 0.6: winner = f"{h} WIN"; dc="1X"; conf="72%"
    elif diff < -0.6: winner = f"{a} WIN"; dc="X2"; conf="70%"
    else: winner = "DRAW"; dc="1X or X2"; conf="58%"

    goals = "Over 2.5" if total > 2.4 else "Over 1.5" if total > 1.5 else "Under 1.5"
    btts = "YES" if ha>0.8 and aa>0.8 else "NO"

    return jsonify({
        "match": f"{h} vs {a}",
        "winner": winner,
        "double_chance": dc,
        "goals": goals,
        "btts": btts,
        "confidence": conf
    })

if __name__ == '__main__':
    app.run()
