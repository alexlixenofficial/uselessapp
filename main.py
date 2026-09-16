import os
import json
import random
import urllib.request
from flask import Flask, jsonify, request

app = Flask(__name__)

SYSTEM_INSTRUCTION = (
    "You are an AI living inside a completely useless app. "
    "Every time the user taps the button, give a 1-sentence sarcastic, "
    "passive-aggressive, or hilariously unhelpful response. "
    "Keep it under 15 words. Never offer real help."
)

FALLBACK_SNARKS = [
    "Fascinating tap. Truly groundbreaking.",
    "Is this really what you're doing right now?",
    "You clicked a button. Here is your invisible trophy.",
    "Your dedication to doing nothing is inspiring.",
    "Another tap. Another second gone forever."
]

def query_gemini(count):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"The user has tapped the useless button {count} times."}]}],
        "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]}
    }
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception:
        return None

@app.route('/')
def index():
    with open("index.html", "r") as f:
        return f.read()

@app.route('/api/tap')
def trigger_tap():
    count = request.args.get('count', '1')
    message = query_gemini(count)
    
    if not message:
        message = random.choice(FALLBACK_SNARKS)
        
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(port=8000, debug=True)