from flask import Flask, request, jsonify
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

POWER = {
 "Man City":95,"Arsenal":92,"Liverpool":93,"Chelsea":88,"Man United":86,"Tottenham":84,"Newcastle":83,"Aston Villa":82,"Ipswich Town":65,"Ipswich":65,
 "Real Madrid":95,"Barcelona":93,"Atletico Madrid":88,
 "Bayern Munich":92,"Leverkusen":88,"Dortmund":85,
 "Inter":90,"Napoli":87,"AC Milan":86,"Juventus":85,"Inter Milan":90,
 "PSG":90,"Marseille":82,"Monaco":81,
 "Ajax":84,"PSV":83,"Feyenoord":82
}

HTML = """
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<style>
body{background:#0f172a;color:#fff;font-family:Arial;padding:15px}
.card{background:#1e293b;padding:22px;border-radius:16px;max-width:520px;margin:auto}
input,select,button{width:100%;padding:14px;margin:7px 0;border-radius:10px;border:0;font-size:16px}
button{background:#22c55e;font-weight:bold;color:#000}
.res{background:#0f172a;padding:15px;border-radius:10px;margin-top:12px;line-height:1.8}
.badge{display:inline-block;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:bold}
.green{background:#22c55e;color:#000}.yellow{background:#eab308;color:#000}.red{background:#ef4444}
small{color:#94a3b8}
</style></head><body>
<div class='card'>
<h2>⚽ FINAL - Money Version</h2>
<p><small>Leave goals empty = auto. Fill for more accuracy.</small></p>
<select id='lg'><option>Premier League</option><option>La Liga</option><option>Serie A</option><option>Bundesliga</option><option>Ligue 1</option><option>Champions League</option><option>Other</option></select>
<input id='home' placeholder='Home Team e.g. Ipswich Town'>
<input id='away' placeholder='Away Team e.g. Liverpool'>
<input id='hg' placeholder='Home last 5 goals OPTIONAL e.g. 0,0,1,0,1'>
<input id='ag' placeholder='Away last 5 goals OPTIONAL e.g. 3,2,2,4,1'>
<button onclick='go()'>PREDICT - SHOULD I BET?</button>
<div id='r'></div>
</div>
<script>
async function go(){
 let h=document.getElementById('home').value||'Home';
 let a=document.getElementById('away').value||'Away';
 let lg=document.getElementById('lg').value;
 let hg=document.getElementById('hg').value;
 let ag=document.getElementById('ag').value;
 document.getElementById('r').innerHTML='Calculating...';
 let res=await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({home:h,away:a,league:lg,home_goals:hg,away_goals:ag})});
 let d=await res.json();
 let cls=d.conf>=70?'green':d.conf>=60?'yellow':'red';
 document.getElementById('r').innerHTML="<div class='res'><b>"+d.match+"</b> - "+d.league+"<br><span class='badge "+cls+"'>Confidence: "+d.conf+"% - "+d.action+"</span><br><br>🏆 Winner: <b>"+d.winner+"</b><br>🛡️ Double Chance: "+d.dc+"<br>⚽ Goals: "+d.goals+" ("+d.goals_conf+"%)<br>🥅 BTTS: "+d.btts+"<br><br><small>"+d.note+"</small><br><br><b style='color:"+(d.action=='BET'?'#22c55e':'#eab308')+"'>Advice: "+d.advice+"</b></div>";
}
</script></body></html>
"""

@app.route('/')
def i(): return HTML

def avg_goals(s):
    try:
        nums=[float(x) for x in s.replace(' ','').split(',') if x!='']
        return sum(nums)/len(nums) if nums else None
    except: return None

@app.route('/predict', methods=['POST'])
def predict():
    j=request.get_json()
    h=j.get('home','Home').strip()
    a=j.get('away','Away').strip()
    lg=j.get('league','Other')
    hg_s=j.get('home_goals','')
    ag_s=j.get('away_goals','')
    
    hp=POWER.get(h,75)
    ap=POWER.get(a,75)
    hp_base=hp
    ap_base=ap
    hp+=5 # home adv

    hg_avg=avg_goals(hg_s)
    ag_avg=avg_goals(ag_s)
    
    if hg_avg is not None and ag_avg is not None:
        # combine power + form = most trusted
        diff=(hp-ap)+(hg_avg-ag_avg)*8
        note=f"Using REAL form: {h} avg {hg_avg:.1f} vs {a} avg {ag_avg:.1f} + power"
        conf_boost=15
    else:
        diff=hp-ap
        note=f"Auto mode: {h} power {hp_base} vs {a} power {ap_base}. For more trust, add last 5 goals."
        conf_boost=0

    # Winner
    if diff>18: winner=f"{h} WIN"; conf=min(82+conf_boost//2,88); dc="1X"
    elif diff>8: winner=f"{h} WIN"; conf=random.randint(62,70)+conf_boost//2; dc="1X"
    elif diff<-18: winner=f"{a} WIN"; conf=min(82+conf_boost//2,88); dc="X2"
    elif diff<-8: winner=f"{a} WIN"; conf=random.randint(62,70)+conf_boost//2; dc="X2"
    else: winner="DRAW"; conf=random.randint(50,58)+conf_boost//2; dc="1X or X2"

    conf=int(max(45,min(conf,90)))
    action="BET" if conf>=65 else "SKIP"
    
    # Goals
    if hg_avg is not None:
        total=hg_avg+ag_avg
        goals="Over 1.5" if total>1.8 else "Under 1.5"
        goals_conf=75 if total>2.5 or total<1.2 else 60
        if total>2.8: goals="Over 2.5"; goals_conf=70
    else:
        avg_p=(hp_base+ap_base)/2
        goals="Over 1.5" if avg_p>72 else "Under 2.5"
        goals_conf=70

    btts="YES" if abs(diff)<18 and conf<75 else "NO" if abs(diff)>20 else "YES"
    advice="BET Double Chance + "+goals+" is safest" if action=="BET" else "Don't bet this game - too close. Find another match with >65%"
    
    return jsonify({
        "match":f"{h} vs {a}","league":lg,"winner":winner,"dc":dc,
        "goals":goals,"goals_conf":goals_conf,"btts":btts,
        "conf":conf,"action":action,"advice":advice,"note":note
    })

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
