from flask import Blueprint, request, jsonify, current_app, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from .dialogflow import DialogflowService

main_bp = Blueprint('main', __name__)

# Initialize Dialogflow service
dialogflow_service = None

@main_bp.before_app_first_request
def initialize_dialogflow():
    global dialogflow_service
    dialogflow_service = DialogflowService(
        current_app.config['PROJECT_ID'],
        current_app.config['LOCATION'],
        current_app.config['AGENT_ID']
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    message = data['message']
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    # Process any attachment information
    attachment = data.get('attachment')
    attachment_text = ""
    if attachment:
        attachment_text = f" (with attachment: {attachment.get('name', 'unnamed file')})"
    
    # Send message to Dialogflow
    try:
        df_response = dialogflow_service.detect_intent(session_id, message + attachment_text)
        processed_response = dialogflow_service.process_dialogflow_response(df_response)
        
        return jsonify({
            'session_id': session_id,
            'response': processed_response['text'],
            'intent': processed_response['intent'],
            'confidence': processed_response['confidence'],
            'payload': processed_response['payload']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate a safe filename with UUID to prevent conflicts
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Generate URL for the uploaded file
        file_url = url_for('static', filename=f'uploads/{unique_filename}', _external=True)
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'original_name': filename,
            'url': file_url
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'ok'}), 200