from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Football Predictor</title>
<style>
body{font-family:Arial;background:#0f172a;color:#fff;padding:20px}
.card{background:#1e293b;padding:20px;border-radius:15px;max-width:500px;margin:auto}
input,button{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none}
input{background:#334155;color:#fff}
button{background:#22c55e;font-weight:bold;font-size:16px}
#res{display:none;background:#0f172a;padding:15px;border-radius:10px;margin-top:15px}
</style>
</head>
<body>
<div class="card">
<h2>⚽ Football Predictor - Any League</h2>
<input id="home" placeholder="Home Team (e.g Man City)">
<input id="away" placeholder="Away Team (e.g Arsenal)">
<input id="hform" placeholder="Home last 5 goals: 2,1,0,3,1">
<input id="aform" placeholder="Away last 5 goals: 1,0,1,1,2">
<button onclick="go()">PREDICT MATCH</button>
<div id="res"></div>
</div>
<script>
async function go(){
 let h=document.getElementById('home').value;
 let a=document.getElementById('away').value;
 let hf=document.getElementById('hform').value.split(',').map(Number);
 let af=document.getElementById('aform').value.split(',').map(Number);
 let r=await fetch('/predict',{
   method:'POST',
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify({home_team:h,away_team:a,home_form:hf,away_form:af})
 });
 let d=await r.json();
 let el=document.getElementById('res');
 el.style.display='block';
 el.innerHTML=`<h3>${d.match}</h3>
 <p><b>Winner:</b> ${d.winner} ${d.confidence}</p>
 <p><b>Double Chance:</b> ${d.double_chance}</p>
 <p><b>Goals:</b> ${d.goals}</p>
 <p><b>BTTS:</b> ${d.btts}</p>`;
}
</script>
</body>
</html>
"""

@app.route('/predict', methods=['POST'])
def predict():
    j=request.get_json()
    h=j.get('home_team','Home')
    a=j.get('away_team','Away')
    hf=j.get('home_form',[1])
    af=j.get('away_form',[1])
    ha=sum(hf)/len(hf)
    aa=sum(af)/len(af)
    diff=ha-aa
    tot=ha+aa
    if diff>0.6:
        win=f"{h} WIN"; dc="1X"; c="72%"
    elif diff<-0.6:
        win=f"{a} WIN"; dc="X2"; c="70%"
    else:
        win="DRAW"; dc="1X or X2"; c="58%"
    goals="Over 2.5" if tot>2.4 else "Over 1.5" if tot>1.5 else "Under 1.5"
    btts="YES" if ha>0.8 and aa>0.8 else "NO"
    return jsonify({
        "match":f"{h} vs {a}",
        "winner":win,
        "double_chance":dc,
        "goals":goals,
        "btts":btts,
        "confidence":c
    })

if __name__ == '__main__':
    app.run()
