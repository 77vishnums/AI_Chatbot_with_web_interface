from flask import Flask, render_template, request, jsonify
import os
import requests

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if GEMINI_API_KEY == 'YOUR_API_KEY_HERE':
        error_message = "ERROR: Google Gemini API key is not configured."
        print(error_message)
        return jsonify({"error": error_message}), 500

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        payload = {
            "contents": [{
                "parts": [{"text": user_message}]
            }]
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        api_response = response.json()
        
        ai_message = api_response['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"reply": ai_message})

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return jsonify({"error": "Failed to communicate with the AI service. Please check your network connection and API key."}), 503
    except (KeyError, IndexError) as e:
        print(f"API Response Parsing Error: {e} - Response: {api_response}")
        return jsonify({"error": "Received an invalid response format from the AI service."}), 500

if __name__ == '__main__':
    app.run(debug=True)
