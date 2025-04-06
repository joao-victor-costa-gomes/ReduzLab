import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from .utils.file_handler import save_csv_file
from .utils.file_validator import validate_file
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
            file = request.files.get('file')
            if file:
                filename = secure_filename(file.filename)
                if filename.endswith(('.csv', '.xlsx')):

                    # Validating if the file is not corrupted
                    is_valid, error_message = validate_file(file, filename)

                    if is_valid:
                        saved_path = save_csv_file(file, filename)
                        table_html = read_data_preview(saved_path)
                        message = f"The file '{filename}' was uploaded successfully!"
                        message_type = 'success'
                    else:
                        message = f"Error processing file: {error_message}"
                        message_type = 'error'

                else:
                    message = "Only .csv and .xlsx files are allowed. Please upload a valid file."
                    message_type = 'error'

            else:
                message = "No file uploaded. Please choose a file to upload."
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
