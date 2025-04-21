from flask import Flask, request, jsonify
from flask_cors import CORS
import google.cloud.dialogflow_v2 as dialogflow
import os
import json

app = Flask(__name__)
CORS(app)

# Set the environment variable for the Google Cloud credentials
# You'll need to update this with your own Dialogflow credentials path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-dialogflow-credentials.json"

# Your Dialogflow project ID
# You'll need to update this with your own Dialogflow project ID
PROJECT_ID = "your-dialogflow-project-id"
SESSION_ID = "unique-session-id"  # This can be any unique string
LANGUAGE_CODE = "en-US"

@app.route('/')
def index():
    return jsonify({'message': 'Flask backend for Dialogflow API integration'})

@app.route('/api/dialogflow', methods=['POST'])
def dialogflow_api():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Create a session client
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(PROJECT_ID, SESSION_ID)
        
        # Create a text input
        text_input = dialogflow.TextInput(text=user_message, language_code=LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)
        
        # Detect intent
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        
        # Process the response
        query_result = response.query_result
        fulfillment_text = query_result.fulfillment_text
        intent = query_result.intent.display_name
        confidence = query_result.intent_detection_confidence
        
        # Check if there are any response messages with payload
        rich_response = None
        for msg in query_result.fulfillment_messages:
            if msg.payload:
                rich_response = json.loads(msg.payload.json)
                break
        
        return jsonify({
            'response': fulfillment_text,
            'intent': intent,
            'confidence': confidence,
            'rich_response': rich_response
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
