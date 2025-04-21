# Angular-Flask-Dialogflow CX Chatbot Widget

This project is a full-stack application that integrates an Angular frontend with a Flask backend to create a chatbot widget powered by Google's Dialogflow CX API.

## Features

- Interactive popup chatbot widget positioned in the bottom-right corner
- Voice input support using the Web Speech API
- File attachment capabilities
- Flask backend serving as a proxy to Dialogflow CX API
- Real-time chat interface with typing indicators
- Support for rich responses from Dialogflow (buttons, cards, etc.)
- Responsive design that works on mobile and desktop

## Project Structure

- `/dialogflow-api` - Angular frontend application
- `/flask-backend` - Flask backend for Dialogflow CX integration

## Setup Instructions

### Prerequisites

- Node.js and npm
- Python 3.6 or higher
- Google Cloud account with Dialogflow CX API enabled
- Dialogflow CX agent configured in Dialogflow CX Console

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd flask-backend
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your Dialogflow CX credentials:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file
   - Update the following variables in `app.py`:
     - `PROJECT_ID`: Your Google Cloud project ID
     - `LOCATION`: Region where your agent is deployed (e.g., "global", "us-central1")
     - `AGENT_ID`: Your Dialogflow CX agent ID

5. Start the Flask server:
   ```
   python app.py
   ```
   The server will start on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd dialogflow-api
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   ng serve
   ```
   The application will be available at http://localhost:4200

## Usage

1. Open the application in your browser
2. Click the chat bubble in the bottom-right corner to open the chatbot
3. Type a message or use voice input by clicking the microphone icon
4. Upload files using the attachment (paperclip) icon
5. The chatbot will respond based on your Dialogflow CX agent's configuration

## Customization

### Dialogflow CX Agent

- Create flows, pages, and routes in the Dialogflow CX Console
- Set up intents to handle different user queries
- Create entity types to extract specific information
- Configure fulfillment for complex responses

### Frontend Customization

- Modify the UI styles in the component CSS files
- Add additional rich response types in the chatbot component
- Implement authentication if needed

### Backend Customization

- Add error handling and logging
- Implement session management for multiple users
- Add support for other Dialogflow CX features

## Deployment

### Backend Deployment

- Use Gunicorn or uWSGI for production deployment
- Deploy on cloud platforms like Google Cloud Run, Heroku, or AWS

### Frontend Deployment

- Build the production version: `ng build --prod`
- Deploy the static files to a web server or hosting service like Firebase, Netlify, or GitHub Pages

## License

This project is open source and available under the MIT License.
