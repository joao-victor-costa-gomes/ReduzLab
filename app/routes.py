import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from .utils.file_handler import save_csv_file

from .services import read_data_preview

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reduction', methods=['GET', 'POST'])
def reduction_page():
    message = None
    message_type = None
    table_html = None

    if request.method == 'POST':
        try:

            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                filename = secure_filename(file.filename)
                saved_path = save_csv_file(file, filename)
                print(saved_path)
                table_html = read_data_preview(saved_path)
                print(table_html)
                message = f"The file '{filename}' was uploaded successfully!"
                message_type = 'success'
            else:
                message = f"Cannot upload the file '{filename}'."
                message_type = 'error'

        except RequestEntityTooLarge:
            message = "The file is too large. Please upload a file smaller than 100MB."
            message_type = 'error'

    return render_template(
        'reduction_page.html',
        message=message,
        message_type=message_type,
        table_html=table_html
    )
