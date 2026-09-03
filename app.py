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
<title>Football Predictor - All Leagues</title>
<style>
body{font-family:Arial;background:#0f172a;color:#fff;padding:20px}
.card{background:#1e293b;padding:20px;border-radius:15px;max-width:600px;margin:auto}
input,select,button{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none}
input,select{background:#334155;color:#fff}
button{background:#22c55e;font-weight:bold;font-size:16px;cursor:pointer}
#res{display:none;background:#0f172a;padding:15px;border-radius:10px;margin-top:15px;border:1px solid #22c55e}
small{color:#94a3b8}
</style>
</head>
<body>
<div class="card">
<h2>⚽ All Leagues Predictor</h2>
<select id="league">
  <option value="premier">Premier League - England</option>
  <option value="laliga">La Liga - Spain</option>
  <option value="seriea">Serie A - Italy</option>
  <option value="bundes">Bundesliga - Germany</option>
  <option value="ligue1">Ligue 1 - France</option>
  <option value="eredivisie">Eredivisie - Netherlands</option>
  <option value="portugal">Primeira Liga - Portugal</option>
  <option value="ucl">Champions League - UEFA</option>
  <option value="europa">Europa League</option>
  <option value="mls">MLS - USA</option>
  <option value="saudi">Saudi Pro League</option>
  <option value="brasil">Brasileirão - Brazil</option>
  <option value="argentina">Liga Argentina</option>
  <option value="turkey">Süper Lig - Turkey</option>
  <option value="other">Other League</option>
</select>
<input id="home" placeholder="Home Team (e.g Real Madrid)">
<input id="away" placeholder="Away Team (e.g Barcelona)">
<input id="hform" placeholder="Home last 5 goals: 2,1,3,0,1">
<input id="aform" placeholder="Away last 5 goals: 1,1,0,2,1">
<button onclick="go()">PREDICT MATCH</button>
<div id="res"></div>
</div>
<script>
async function go(){
 let league=document.getElementById('league').value;
 let h=document.getElementById('home').value;
 let a=document.getElementById('away').value;
 let hf=document.getElementById('hform').value.split(',').map(Number);
 let af=document.getElementById('aform').value.split(',').map(Number);
 let r=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},
 body:JSON.stringify({league:league,home_team:h,away_team:a,home_form:hf,away_form:af})});
 let d=await r.json();
 let el=document.getElementById('res'); el.style.display='block';
 el.innerHTML=`<h3>${d.match}</h3><small>${d.league_name}</small>
 <p><b>Winner:</b> ${d.winner} ${d.confidence}</p>
 <p><b>Double Chance:</b> ${d.double_chance}</p>
 <p><b>Goals:</b> ${d.goals}</p>
 <p><b>BTTS:</b> ${d.btts}</p>
 <p><small>${d.note}</small></p>`;
}
</script>
</body>
</html>
"""

@app.route('/predict', methods=['POST'])
def predict():
    j=request.get_json()
    league=j.get('league','other')
    h=j.get('home_team','Home')
    a=j.get('away_team','Away')
    hf=j.get('home_form',[1])
    af=j.get('away_form',[1])

    leagues = {
        "premier": {"name":"Premier League","adv":0.30,"avg":2.85},
        "laliga": {"name":"La Liga","adv":0.25,"avg":2.65},
        "seriea": {"name":"Serie A","adv":0.28,"avg":2.55},
        "bundes": {"name":"Bundesliga","adv":0.32,"avg":3.10},
        "ligue1": {"name":"Ligue 1","adv":0.27,"avg":2.70},
        "eredivisie": {"name":"Eredivisie","adv":0.30,"avg":3.00},
        "portugal": {"name":"Primeira Liga","adv":0.35,"avg":2.50},
        "ucl": {"name":"Champions League","adv":0.20,"avg":2.90},
        "europa": {"name":"Europa League","adv":0.20,"avg":2.75},
        "mls": {"name":"MLS","adv":0.25,"avg":2.80},
        "saudi": {"name":"Saudi Pro League","adv":0.30,"avg":2.95},
        "brasil": {"name":"Brasileirão","adv":0.40,"avg":2.40},
        "argentina": {"name":"Argentina Liga","adv":0.38,"avg":2.20},
        "turkey": {"name":"Süper Lig","adv":0.35,"avg":2.85},
        "other": {"name":"Other League","adv":0.30,"avg":2.60}
    }
    f = leagues.get(league, leagues["other"])

    ha=sum(hf)/len(hf); aa=sum(af)/len(af)
    ha_adj = ha + f["adv"]
    diff = ha_adj - aa
    tot = ha + aa

    if diff>0.75: win=f"{h} WIN"; dc="1X"; c="76%"
    elif diff<-0.55: win=f"{a} WIN"; dc="X2"; c="74%"
    else: win="DRAW"; dc="1X or X2"; c="62%"

    goals="Over 2.5" if tot >= f["avg"] else "Over 1.5" if tot > 1.5 else "Under 1.5"
    btts="YES" if ha>0.7 and aa>0.7 else "NO"

    return jsonify({
        "match":f"{h} vs {a}",
        "league_name":f["name"],
        "winner":win,"double_chance":dc,"goals":goals,"btts":btts,"confidence":c,
        "note":f"Stats adjusted for {f['name']} (Avg goals {f['avg']})"
    })
