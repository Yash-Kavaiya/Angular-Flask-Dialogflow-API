# Flask Backend for Dialogflow API Integration

This backend serves as a bridge between your Angular frontend and Google's Dialogflow API. It handles sending user queries to Dialogflow and returning the responses to your frontend application.

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

3. Set up your Dialogflow credentials:
   - Create a Dialogflow agent in the Google Cloud Console
   - Download your service account key file
   - Update the `GOOGLE_APPLICATION_CREDENTIALS` path in `app.py` to point to your key file
   - Update the `PROJECT_ID` in `app.py` with your Dialogflow project ID

4. Run the application:
   ```bash
   python app.py
   ```

The server will start on `http://127.0.0.1:5000`.

## API Endpoints

- `GET /`: Simple health check endpoint
- `POST /api/dialogflow`: Send a message to Dialogflow
  - Request body: `{"message": "Your user message here"}`
  - Response: JSON with Dialogflow's response

## Dialogflow Setup Recommendations

1. Create intents for common user queries
2. Use entities for capturing specific information
3. Consider using contexts for multi-turn conversations
4. Set up fulfillment if you need to perform actions based on user queries

## Production Considerations

- Use a production WSGI server like Gunicorn instead of Flask's development server
- Set up proper error handling and logging
- Implement authentication for the API endpoints
- Consider deployment on cloud platforms like Google Cloud Run, AWS, or Heroku
