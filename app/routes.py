from flask import Blueprint, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from .services import read_data_preview
from .utils.file_handler import save_uploaded_file
from .utils.validators import validate_file         

main = Blueprint('main', __name__)

# ========== MAIN PAGE ==========

@main.route('/', methods=['GET', 'POST'])
def index():
    # Feedback messages for the upload section
    upload_error = None
    upload_success = None
    # Feedback messages for the table_preview section
    preview_error = None
    preview_success = None

    table_html = None

    try:
        # Handle file upload form submission
        if request.method == 'POST' and request.form.get("form_type") == "upload":
            file = request.files.get("file") 

            # UPLOAD SECTION HANDLER
            if file and file.filename:
                # Validate file type and content
                is_valid, validation_error = validate_file(file, file.filename)  
                if is_valid:
                    # Save the file to the uploads folder
                    saved_path = save_uploaded_file(file, file.filename)
                    table_html = read_data_preview(saved_path) 
                    # TABLE PREVIEW SECTION HANDLER 
                    if table_html is None:
                        preview_error = "Failed to generate preview table. The file might be corrupted or unsupported."
                    else:
                        preview_success = "Preview table generated successfully!"
                    upload_success = "File uploaded and validated successfully!"  
                else:
                    # Can't read the file or corrupted file
                    upload_error = f"File validation failed: {validation_error}"  
            else:
                # No file was provided in the form
                upload_error = "No file selected."  

    except RequestEntityTooLarge:
        # If the file is larger than 100MB
        upload_error = "The file is too large. Please upload a file smaller than 100MB."

    return render_template(
    'index.html',
    upload_error=upload_error,
    upload_success=upload_success,
    preview_error=preview_error,
    preview_success=preview_success,
    table_html=table_html
    )

# ========== PCA PAGE ==========

@main.route('/pca')
def pca_page():
    return render_template('pca_page.html')
