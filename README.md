# Angular-Flask-Dialogflow API Chatbot

This project is a full-stack application that integrates an Angular frontend with a Flask backend to create a chatbot powered by Google's Dialogflow API.

## Features

- Interactive chatbot UI built with Angular
- Flask backend serving as a proxy to Dialogflow API
- Real-time chat interface with typing indicators
- Support for rich responses from Dialogflow (buttons, cards, etc.)
- Responsive design that works on mobile and desktop

## Project Structure

- `/dialogflow-api` - Angular frontend application
- `/flask-backend` - Flask backend for Dialogflow integration

## Setup Instructions

### Prerequisites

- Node.js and npm
- Python 3.6 or higher
- Google Cloud account with Dialogflow API enabled
- Dialogflow agent configured

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

4. Configure your Dialogflow credentials:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file
   - Update the `PROJECT_ID` in `app.py` with your Dialogflow project ID

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
2. Type a message in the chat input and press Enter or click Send
3. The chatbot will respond based on your Dialogflow agent's configuration

## Customization

### Dialogflow Agent

- Create intents in Dialogflow to handle different user queries
- Set up entities to extract specific information from user messages
- Use contexts for managing conversation flow
- Configure fulfillment to perform custom actions

### Frontend Customization

- Modify the UI styles in the component CSS files
- Add additional rich response types in the chatbot component
- Implement authentication if needed

### Backend Customization

- Add error handling and logging
- Implement session management for multiple users
- Add support for other Dialogflow features like audio input

## Deployment

### Backend Deployment

- Use Gunicorn or uWSGI for production deployment
- Deploy on cloud platforms like Google Cloud Run, Heroku, or AWS

### Frontend Deployment

- Build the production version: `ng build --prod`
- Deploy the static files to a web server or hosting service like Firebase, Netlify, or GitHub Pages

## License

This project is open source and available under the MIT License.
