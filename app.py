from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os
app = Flask(__name__)
CORS(app)
GROQ_KEY = os.environ.get("GROQ_KEY", "weka gsk_ yako hapa")
@app.route("/")
def home():
    return "HEZRON AI REAL IS LIVE - From Mau Narok"
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are HEZRON AI from Mau Narok, built by Hezron. You know everything, you are updated to 2026. Speak Swahili/Sheng/English like Kenyan best friend."},
                    {"role": "user", "content": msg}
                ]
            },
            timeout=30
        )
        ans = res.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": ans})
    except Exception as e:
        return jsonify({"answer": "Pole mkuu: " + str(e)})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
