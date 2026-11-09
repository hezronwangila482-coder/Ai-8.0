from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>HEZRON AI</title>
<style>
body{font-family:sans-serif;background:#0f0f0f;color:white;margin:0;padding:15px}
h2{text-align:center;color:#00ff88}
#chat{background:#1a1a1a;height:65vh;overflow:auto;padding:10px;border-radius:10px}
.msg{padding:8px 10px;margin:6px 0;border-radius:10px;max-width:85%}
.me{background:#00ff88;color:black;margin-left:auto}
.ai{background:#333}
#box{display:flex;margin-top:10px;gap:8px}
input{flex:1;padding:12px;border-radius:20px;border:none;outline:none}
button{padding:12px 18px;border:none;border-radius:20px;background:#00ff88;font-weight:bold}
</style></head>
<body>
<h2>🤖 HEZRON AI - Mau Narok</h2>
<div id="chat"><div class="msg ai">Mambo mkuu! Mimi ni HEZRON. Niambie nini?</div></div>
<div id="box"><input id="inp" placeholder="Andika hapa..."><button onclick="send()">Tuma</button></div>
<script>
async function send(){
 let inp=document.getElementById('inp');
 let txt=inp.value.trim(); if(!txt) return;
 let chat=document.getElementById('chat');
 chat.innerHTML+='<div class="msg me">'+txt+'</div>'; inp.value='';
 chat.innerHTML+='<div class="msg ai" id="loading">HEZRON anaandika...</div>'; chat.scrollTop=chat.scrollHeight;
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
 let d=await r.json();
 document.getElementById('loading').remove();
 chat.innerHTML+='<div class="msg ai">'+d.reply+'</div>'; chat.scrollTop=chat.scrollHeight;
}
document.getElementById('inp').addEventListener('keydown',e=>{if(e.key==='Enter') send()});
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    if not msg:
        return jsonify({"reply": "Niambie kitu mkuu!"})
    if not GROQ_KEY:
        return jsonify({"reply": 
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Wewe ni HEZRON AI, msaidizi mwerevu, mcheshi na mkarimu kutoka Mau Narok, Kenya. Jibu kwa Sheng / Kiswahili rahisi. Kuwa mfupi na msaada."},
                    {"role": "user", "content": msg}
                ],
                "temperature": 0.7,
                "max_tokens": 800
            },
            timeout=30
        )
        data = res.json()
        if "choices" not in data:
            return jsonify({"reply": f"Groq error: {data.get('error', {}).get('message', 'Unknown')}"})
        return jsonify({"reply": data["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"reply": f"Pole mkuu: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
