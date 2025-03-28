import os 
from flask import current_app

def save_csv_file(file, filename):
    upload_path = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_path, exist_ok=True)  # Create uploads folder if it doesn't exists
    file.save(os.path.join(upload_path, filename))