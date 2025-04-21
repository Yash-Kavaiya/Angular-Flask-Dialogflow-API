# Flask Backend for Dialogflow CX API Integration

This backend serves as a bridge between your Angular frontend and Google's Dialogflow CX API. It handles sending user queries to Dialogflow CX and returning the responses to your frontend application.

## Setup Instructions

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Dialogflow CX credentials:
   - Create a Dialogflow CX agent in the Google Cloud Console
   - Download your service account key file
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` path in `app.py` to point to your key file
   - Update the configuration variables in `app.py`:
     - `PROJECT_ID`: Your Google Cloud project ID
     - `LOCATION`: Region where your agent is deployed (e.g., "global", "us-central1")
     - `AGENT_ID`: Your Dialogflow CX agent ID

4. Run the application:
   ```bash
   python app.py
   ```

The server will start on `http://127.0.0.1:5000`.

## API Endpoints

- `GET /`: Simple health check endpoint
- `POST /api/dialogflow`: Send a text message to Dialogflow CX
  - Request body: `{"message": "Your user message here"}`
  - Response: JSON with Dialogflow's response
- `POST /api/dialogflow/audio`: (Future implementation) Send audio to Dialogflow CX

## Dialogflow CX Setup Recommendations

1. Design a conversation flow with states and routes
2. Create intents for different user queries
3. Use entity types to capture specific information
4. Set up fulfillment for more complex responses
5. Test your flows in the Dialogflow CX Console

## Production Considerations

- Use a production WSGI server like Gunicorn instead of Flask's development server
- Set up proper error handling and logging
- Implement authentication for the API endpoints
- Consider deployment on cloud platforms like Google Cloud Run, AWS, or Heroku
