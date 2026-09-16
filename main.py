import os
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Sarcastic fallback messages
SNARK_RESPONSES = [
    "Fascinating tap. Truly groundbreaking.",
    "Is this really what you're doing right now?",
    "You clicked a button. Here is your invisible trophy.",
    "Another tap closer to ultimate enlightenment. Or not.",
    "Your dedication to doing nothing is inspiring.",
    "Error 404: Purpose not found."
]

MANIFEST_DATA = {
    "name": "Productivity Zero",
    "short_name": "ProdZero",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0d0d0d",
    "theme_color": "#0d0d0d",
    "orientation": "portrait",
    "icons": [
        {
            "src": "https://via.placeholder.com/512.png?text=ZERO",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return render_template_string(html_content)

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST_DATA)

@app.route('/api/tap')
def tap():
    try:
        count = int(request.args.get('count', 0))
    except ValueError:
        count = 0
    
    msg_index = count % len(SNARK_RESPONSES)
    return jsonify({"message": SNARK_RESPONSES[msg_index]})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)