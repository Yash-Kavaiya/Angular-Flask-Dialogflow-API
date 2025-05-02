import os
import uuid
from flask import current_app, url_for
from werkzeug.utils import secure_filename

def save_uploaded_file(file):
    """Save an uploaded file and return its URL."""
    if file and file.filename:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Generate URL for the uploaded file
        file_url = url_for('static', filename=f'uploads/{unique_filename}', _external=True)
        
        return {
            'success': True,
            'filename': unique_filename,
            'original_name': filename,
            'url': file_url
        }
    
    return {
        'success': False,
        'error': 'Invalid file'
    }