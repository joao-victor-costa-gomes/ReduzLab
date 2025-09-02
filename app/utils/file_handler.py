import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    """Checks if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """
    Saves the uploaded file with a unique name to prevent overwrites
    and returns the unique filename.
    """
    # Get the original file extension
    original_filename = secure_filename(file.filename)
    _root, extension = os.path.splitext(original_filename)

    # Generate a unique name using UUID
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    
    # Build the full path and save the file
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(upload_path)
    
    return unique_filename