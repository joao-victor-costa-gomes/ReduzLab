import os
from app.main import bp
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask import render_template, request, current_app, redirect, url_for, flash

# List of allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# home page of the application
@bp.route('/', methods=['GET', 'POST'])
def index_page():
    # variables for feedback messages
    upload_error = None
    upload_success = None

    if request.method == 'POST':
        # Check if the file part is in the request. 
        if 'file' not in request.files:
            upload_error = "No file part in request. Please try again."
        else:
            file = request.files['file']
            # Check if a file was selected by the user
            if file.filename == '':
                upload_error = "No file selected. Please choose a file to upload."
            # Check if the file has an allowed extension and process it
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                upload_success = f"File '{filename}' uploaded successfully!"
            # Handle the case of a non-allowed file extension
            else:
                upload_error = "Invalid file type. Please upload a .csv or .xlsx file."
        
    # The template is now rendered in all cases, passing the message variables.
    return render_template('index.html', 
                           upload_error=upload_error, 
                           upload_success=upload_success)

@bp.app_errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """
    Handles the 'RequestEntityTooLarge' exception, which occurs
    when an uploaded file exceeds the configured MAX_CONTENT_LENGTH.
    """
    # Using flash to send a message to the next request.
    # This is a common pattern for handling errors with redirects.
    flash(f"File is too large. The maximum allowed size is {current_app.config['MAX_CONTENT_LENGTH'] / 1024 / 1024:.0f} MB.")
    return redirect(url_for('main.index_page'))