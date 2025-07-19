from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS
import os
import time
import json
import re

app = Flask(__name__, static_url_path='/static')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Using the most basic model with highest free tier limits
model = genai.GenerativeModel('gemini-2.0-flash-lite')

def analyze_symptoms(symptoms_text):
    # Improved prompt for pure JSON output with first aid
    prompt = f"""
    Analyze these baby symptoms: {symptoms_text}

    Respond ONLY with a valid JSON object containing these exact keys:
    - risk_level: one of "URGENT", "HIGH", "MEDIUM", "LOW"
    - recommendation: string
    - explanation: string
    - symptoms_identified: array of strings
    - immediate_actions: array of strings
    - first_aid_suggestions: array of safe, basic first aid steps (only if applicable and safe for home use)
    - seek_care_within: string

    Be concise but thorough. Err on caution. Include first aid only if it's safe and appropriate.
    Do not include any text outside the JSON object. No explanations, no code blocks, no markdown.
    """
    
    max_retries = 3
    retry_delay = 10  # reduced delay
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove any potential markdown code blocks
            if response_text.startswith('```json'):
                response_text = response_text[7:].strip()
            if response_text.endswith('```'):
                response_text = response_text[:-3].strip()
            
            # Parse to validate it's JSON
            json_data = json.loads(response_text)
            return json.dumps(json_data)  # Return clean JSON string
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from text
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                try:
                    json_data = json.loads(match.group(0))
                    return json.dumps(json_data)
                except:
                    pass
        except Exception as e:
            error_str = str(e)
            if "429" in error_str and attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            if "429" in error_str:
                return json.dumps({
                    "risk_level": "UNKNOWN",
                    "recommendation": "Service temporarily busy. Please try again shortly.",
                    "explanation": "Free tier limit reached. Wait a moment and retry.",
                    "symptoms_identified": [],
                    "immediate_actions": ["Wait 10 seconds", "Try again", "If urgent, seek medical care"],
                    "seek_care_within": "If concerned, don't wait - see a doctor"
                })
            return json.dumps({"error": f"Error analyzing symptoms: {str(e)}"})

    return json.dumps({"error": "Max retries exceeded"})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    symptoms = data.get('symptoms', '')
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    analysis = analyze_symptoms(symptoms)
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    app.run(debug=True) 
