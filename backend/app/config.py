import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-development'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Dialogflow CX configuration
    PROJECT_ID = os.environ.get('PROJECT_ID') or 'your-project-id'
    LOCATION = os.environ.get('LOCATION') or 'global'
    AGENT_ID = os.environ.get('AGENT_ID') or 'your-agent-id'