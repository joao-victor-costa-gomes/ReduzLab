import os 
from datetime import datetime
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def generate_timestamped_filename(original_filename):
    name, extension = os.path.splitext(secure_filename(original_filename))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'{timestamp}{extension}'

def save_csv_file(file, filename):
    upload_path = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_path, exist_ok=True)  # Create uploads folder if it doesn't exists
    unique_filename = generate_timestamped_filename(filename)
    file.save(os.path.join(upload_path, unique_filename))