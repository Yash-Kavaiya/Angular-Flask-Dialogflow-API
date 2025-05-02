from flask import Flask
from flask_cors import CORS
import os
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_class)
    
    # Set up CORS to allow requests from Angular frontend
    CORS(app)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import and register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app