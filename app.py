from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Football Predictor</title>
<style>
body{font-family:Arial;background:#0f172a;color:#fff;padding:20px;margin:0}
.card{background:#1e293b;padding:20px;border-radius:15px;max-width:600px;margin:auto;box-shadow:0 10px 30px rgba(0,0,0,0.5)}
input,select,button{width:100%;padding:13px;margin:8px 0;border-radius:8px;border:none;box-sizing:border-box}
input,select{background:#334155;color:#fff;font-size:15px}
button{background:#22c55e;color:#000;font-weight:bold;font-size:17px;cursor:pointer}
#res{display:none;background:#0f172a;padding:15px;border-radius:10px;margin-top:15px;border:1px solid #22c55e;white-space:pre-line}
h2{text-align:center}
</style></head><body><div class='card'>
<h2>⚽ All Leagues Predictor (No Ghana)</h2>
<select id='league'>
<option value='premier'>Premier League - England</option>
<option value='laliga'>La Liga - Spain</option>
<option value='seriea'>Serie A - Italy</option>
<option value='bundes'>Bundesliga - Germany</option>
<option value='ligue1'>Ligue 1 - France</option>
<option value='eredivisie'>Eredivisie - Netherlands</option>
<option value='portugal'>Primeira Liga - Portugal</option>
<option value='ucl'>Champions League</option>
<option value='europa'>Europa League</option>
<option value='mls'>MLS - USA</option>
<option value='saudi'>Saudi Pro League</option>
<option value='brasil'>Brasileirão - Brazil</option>
<option value='argentina'>Liga Argentina</option>
<option value='turkey'>Super Lig - Turkey</option>
<option value='other'>Other League</option>
</select>
<input id='home' placeholder='Home Team (e.g Man City)'>
<input id='away' placeholder='Away Team (e.g Arsenal)'>
<input id='hform' placeholder='Home last 5 goals: 2,1,3,0,1'>
<input id='aform' placeholder='Away last 5 goals: 1,1,0,2,1'>
<button onclick='go()'>PREDICT MATCH</button>
<div id='res'></div></div>
<script>
async function go(){
let league=document.getElementById('league').value;
let h=document.getElementById('home').value || 'Home';
let a=document.getElementById('away').value || 'Away';
let hf=document.getElementById('hform').value.split(',').map(Number).filter(n=>!isNaN(n));
let af=document.getElementById('aform').value.split(',').map(Number).filter(n=>!isNaN(n));
if(hf.length==0) hf=[1,1,1]; if(af.length==0) af=[1,0,1];
let r=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({league:league,home_team:h,away_team:a,home_form:hf,away_form:af})});
let d=await r.json(); let el=document.getElementById('res'); el.style.display='block';
el.innerHTML='<h3>'+d.match+'</h3><small>'+d.league_name+'</small><p><b>Winner:</b> '+d.winner+' '+d.confidence+'</p><p><b>Double Chance:</b> '+d.double_chance+'</p><p><b>Goals:</b> '+d.goals+'</p><p><b>BTTS:</b> '+d.btts+'</p><p><small>'+d.note+'</small></p>';}
</script></body></html>
"""
@app.route('/predict', methods=['POST'])
def predict():
    j=request.get_json()
    league=j.get('league','other'); h=j.get('home_team','Home'); a=j.get('away_team','Away')
    hf=j.get('home_form',[1]); af=j.get('
