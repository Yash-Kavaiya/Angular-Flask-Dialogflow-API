# MCP Backend for Dialogflow CX Chatbot

This is the Flask backend for the Angular-Flask-Dialogflow-API chatbot. It provides API endpoints for:

- Sending messages to Dialogflow CX using the Model Context Protocol
- Uploading files for chat attachments
- Health check monitoring

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Dialogflow CX credentials:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
   - Update `app/config.py` with your project details

4. Run the application:
   ```
   python main.py
   ```

## API Endpoints

- POST `/chat` - Send a message to Dialogflow
- POST `/upload` - Upload a file attachment
- GET `/health` - Health check endpoint

## MCP Implementation

The Model Context Protocol (MCP) is implemented in the `dialogflow.py` file. The implementation follows these steps:

1. Initialize a session with Dialogflow CX
2. Send user messages to Dialogflow and receive responses
3. Extract and process response data to be sent back to the client

The implementation maintains conversation context between requests using session IDs.