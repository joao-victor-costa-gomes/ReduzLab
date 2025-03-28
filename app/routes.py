import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from .utils.file_handler import save_csv_file

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reduction', methods=['GET', 'POST'])
def reduction_page():
    message = None

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            save_csv_file(file, filename)
            message = f"The file '{filename}' was uploaded successfully!"
        else:
            message = f"Cannot upload the file '{filename}'."

    return render_template('reduction_page.html', message=message)
