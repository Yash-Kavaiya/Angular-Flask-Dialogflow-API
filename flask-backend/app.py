from flask import Flask, request, jsonify
from flask_cors import CORS
import google.cloud.dialogflowcx_v3 as dialogflow
import os
import json

app = Flask(__name__)
CORS(app)

# Set the environment variable for the Google Cloud credentials
# You'll need to update this with your own Dialogflow CX credentials path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-dialogflow-cx-credentials.json"

# Your Dialogflow CX configuration
# Update these with your own Dialogflow CX details
PROJECT_ID = "your-project-id"
LOCATION = "global"  # Or your specific region like us-central1
AGENT_ID = "your-agent-id"
LANGUAGE_CODE = "en-US"

@app.route('/')
def index():
    return jsonify({'message': 'Flask backend for Dialogflow CX API integration'})

@app.route('/api/dialogflow', methods=['POST'])
def dialogflow_api():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Initialize session
        session_client = dialogflow.SessionsClient()
        session_path = session_client.session_path(
            project=PROJECT_ID,
            location=LOCATION,
            agent=AGENT_ID,
            session=request.remote_addr  # Use client IP as session ID for uniqueness
        )
        
        # Build the text input
        text_input = dialogflow.TextInput(text=user_message)
        query_input = dialogflow.QueryInput(text=text_input, language_code=LANGUAGE_CODE)
        
        # Send the request to Dialogflow CX
        response = session_client.detect_intent(request={"session": session_path, "query_input": query_input})
        
        # Process the response
        response_messages = []
        rich_response = None
        
        # Extract the response messages
        for message in response.query_result.response_messages:
            if message.text.text:
                response_messages.extend(message.text.text)
            
            # Check for payload (rich responses)
            if message.payload:
                rich_response = json.loads(message.payload.decode('utf-8'))
        
        # Use the first response message as our primary response
        fulfillment_text = response_messages[0] if response_messages else ""
        
        # Get intent information
        intent = response.query_result.intent.display_name if response.query_result.intent else "No intent matched"
        confidence = response.query_result.intent_detection_confidence
        
        return jsonify({
            'response': fulfillment_text,
            'intent': intent,
            'confidence': confidence,
            'rich_response': rich_response,
            'all_responses': response_messages
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dialogflow/audio', methods=['POST'])
def dialogflow_audio_api():
    # Handle audio input (future implementation)
    return jsonify({'error': 'Audio input not yet implemented'}), 501

if __name__ == '__main__':
    app.run(debug=True)
