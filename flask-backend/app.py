from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session
import os
import json
import uuid

app = Flask(__name__)
CORS(app)

# Dialogflow CX configuration
PROJECT_ID = "gen-ai-guru-gdg-pune"
LOCATION = "asia-south1"
AGENT_ID = "b2c5e90b-20ef-4b0c-96d1-49537c77a2cf"
LANGUAGE_CODE = "en-us"

# Set the environment variable for the Google Cloud credentials
credentials_path = os.path.join(os.path.dirname(__file__), 'dialogflow-credentials.json')
if os.path.exists(credentials_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

def detect_intent_text(text, session_id=None):
    """Returns the result of detect intent with webhook disabled"""
    try:
        # Set up client options for regional endpoint
        client_options = None
        if LOCATION != "global":
            api_endpoint = f"{LOCATION}-dialogflow.googleapis.com:443"
            print(f"API Endpoint: {api_endpoint}")
            client_options = {"api_endpoint": api_endpoint}
        
        session_client = SessionsClient(client_options=client_options)
        
        if not session_id:
            session_id = str(uuid.uuid4())
            
        session_path = session_client.session_path(
            project=PROJECT_ID,
            location=LOCATION,
            agent=AGENT_ID,
            session=session_id,
        )
        print(f"Session Path: {session_path}")

        # Prepare request
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=LANGUAGE_CODE)
        query_params = session.QueryParameters(
            disable_webhook=True,
        )
        request = session.DetectIntentRequest(
            session=session_path,
            query_input=query_input,
            query_params=query_params,
        )

        print(f"Sending request to Dialogflow CX...")
        response = session_client.detect_intent(request=request)
        print(f"Received response from Dialogflow CX")

        # Process response
        response_messages = []
        for message in response.query_result.response_messages:
            if message.text:
                response_messages.extend(message.text.text)
                print(f"Agent Response: {message.text.text}")

        return {
            'response': response_messages[0] if response_messages else "",
            'all_responses': response_messages,
            'intent': response.query_result.intent.display_name if response.query_result.intent else "No intent matched",
            'confidence': response.query_result.intent_detection_confidence,
            'session_id': session_id
        }
    except Exception as e:
        print(f"Error in detect_intent_text: {str(e)}")
        raise

@app.route('/')
def index():
    return jsonify({'message': 'Flask backend for Dialogflow CX API integration'})

@app.route('/api/dialogflow', methods=['POST'])
def dialogflow_api():
    print("\n=== New request to /api/dialogflow ===")
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        
        if not data:
            print("Error: No data provided")
            return jsonify({'error': 'No data provided'}), 400
            
        user_message = data.get('message')
        session_id = data.get('session_id')  # Optional session ID for conversation continuity
        
        if not user_message:
            print("Error: No message provided")
            return jsonify({'error': 'No message provided'}), 400

        # Check if credentials are properly set
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            print("Error: Dialogflow credentials not configured")
            return jsonify({
                'error': 'Dialogflow credentials not configured',
                'response': 'Sorry, the chatbot is not properly configured. Please check the server logs.',
                'intent': 'error',
                'confidence': 0
            }), 500
        
        # Get response from Dialogflow
        result = detect_intent_text(user_message, session_id)
        return jsonify(result)
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            'error': str(e),
            'response': 'Sorry, there was an error processing your request. Please try again.',
            'intent': 'error',
            'confidence': 0
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
