from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

@app.route("/")
def home():
    return "HEZRON AI REAL IS LIVE - From Mau Narok"

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    if not msg:
        return jsonify({"reply": "Niambie kitu mkuu, niko hapa!"})

    if not GROQ_KEY:
        return jsonify({"reply": "Mkuu, GROQ_API_KEY haijawekwa kwenye Render bado."})

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Wewe ni HEZRON AI, msaidizi m werevu, mcheshi na mkarimu kutoka Mau Narok, Kenya. Jibu kwa Sheng / Kiswahili rahisi kama user akiongea hivyo. Kuwa mfupi na msaada."},
                    {"role": "user", "content": msg}
                ],
                "temperature": 0.7,
                "max_tokens": 800
            },
            timeout=30
        )

        data = res.json()

        
        if "choices" not in data:
            print("GROQ ERROR:", data)
            return jsonify({"reply": f"Groq imerudisha error: {data.get('error', {}).get('message', 'Unknown error')}"})

        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"reply": f"Pole mkuu, server imekwama kidogo: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
