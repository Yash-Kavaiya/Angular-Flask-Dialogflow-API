from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud.dialogflowcx_v3 import SessionsClient, AgentsClient
from google.cloud.dialogflowcx_v3.types import session, TextInput, QueryInput, DetectIntentRequest
import os
import json
import uuid

app = Flask(__name__)
CORS(app)

# Set the environment variable for the Google Cloud credentials
credentials_path = os.path.join(os.path.dirname(__file__), 'dialogflow-credentials.json')
if os.path.exists(credentials_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Dialogflow CX configuration
PROJECT_ID = "gen-ai-guru-gdg-pune"
LOCATION = "asia-south1"
AGENT_ID = "b2c5e90b-20ef-4b0c-96d1-49537c77a2cf"
LANGUAGE_CODE = "en-us"

# Store sessions in memory (in production, use a proper database)
sessions = {}

def get_or_create_session(user_id):
    """Get an existing session for the user or create a new one."""
    if user_id not in sessions:
        sessions[user_id] = str(uuid.uuid4())
    return sessions[user_id]

def detect_intent_text(session_id, text):
    """Detect intent for a single text input."""
    print(f"\n=== Starting detect_intent_text ===")
    print(f"Session ID: {session_id}")
    print(f"User message: {text}")
    
    agent = f"projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}"
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}")
    
    # Set up client options based on location
    client_options = None
    if LOCATION != "global":
        api_endpoint = f"{LOCATION}-dialogflow.googleapis.com:443"
        print(f"Using regional endpoint: {api_endpoint}")
        client_options = {"api_endpoint": api_endpoint}
    
    # Initialize the session client
    session_client = SessionsClient(client_options=client_options)
    
    # Create the text input and query
    text_input = TextInput(text=text)
    query_input = QueryInput(text=text_input, language_code=LANGUAGE_CODE)
    
    # Create and send the request
    request = DetectIntentRequest(
        session=session_path,
        query_input=query_input
    )
    
    try:
        print("Sending request to Dialogflow CX...")
        response = session_client.detect_intent(request=request)
        print("Received response from Dialogflow CX")
        return response
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
        
        # Get or create a session for this user
        user_id = request.remote_addr
        print(f"User IP: {user_id}")
        session_id = get_or_create_session(user_id)
        print(f"Using session ID: {session_id}")
        
        # Get the response from Dialogflow
        print("Calling Dialogflow CX...")
        response = detect_intent_text(session_id, user_message)
        print("Received response from Dialogflow CX")
        
        # Process the response
        response_messages = []
        rich_response = None
        
        # Extract text responses
        print("Processing response messages...")
        for msg in response.query_result.response_messages:
            if msg.text.text:
                response_messages.extend(msg.text.text)
            if msg.payload:
                rich_response = json.loads(msg.payload.decode('utf-8'))
        
        # Get the primary response text
        fulfillment_text = ' '.join(response_messages) if response_messages else ""
        
        # Get intent information
        intent = response.query_result.intent.display_name if response.query_result.intent else "No intent matched"
        confidence = response.query_result.intent_detection_confidence
        
        print(f"Intent detected: {intent} (confidence: {confidence})")
        print(f"Response text: {fulfillment_text}")
        
        return jsonify({
            'response': fulfillment_text,
            'intent': intent,
            'confidence': confidence,
            'rich_response': rich_response,
            'all_responses': response_messages,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            'error': str(e),
            'response': 'Sorry, there was an error processing your request. Please try again.',
            'intent': 'error',
            'confidence': 0
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
