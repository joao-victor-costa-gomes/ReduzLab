# LIBRARIES
import os
import pandas as pd
from app.main import bp
from werkzeug.exceptions import RequestEntityTooLarge
from flask import render_template, request, current_app, redirect, url_for, flash, session
# LOCAL FUNCTIONS
from app.utils.file_handler import allowed_file, save_uploaded_file
from app.utils.data_preview import generate_preview
from app.utils.data_validator import validate_dataframe
from app.utils.decorators import require_dataset


# ========== HOME PAGE ==========
@bp.route('/', methods=['GET', 'POST'])
def index_page():
    # variables for feedback messages
    upload_error = None
    upload_success = None
    preview_success = None
    preview_error = None 
    table_html= None
    validation_results = None

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
                unique_filename = save_uploaded_file(file)
                upload_success = f"File '{file.filename}' uploaded successfully!"
                # Use the unique name to build the full path for previewing
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                # Use the utility function to generate the preview
                df, table_html, preview_error = generate_preview(upload_path)
                if not preview_error:
                    preview_success = "Data preview generated successfully!"
                    session['uploaded_filename'] = unique_filename
                    # Reading again to detect not numeric (excluding boolean types) columns
                    validation_results = validate_dataframe(df)
                # Clear success message from upload if preview fails
                else: 
                    upload_success = None
            # Handle the case of a non-allowed file extension
            else:
                upload_error = "Invalid file type. Please upload a .csv or .xlsx file."
        
    # The template is now rendered in all cases, passing the message variables.
    return render_template('index.html', 
                           upload_error=upload_error, 
                           upload_success=upload_success,
                           preview_error=preview_error,
                           preview_success=preview_success,
                           table_html=table_html,
                           validation_results=validation_results)

# ========== ALGORITHM PAGES ==========

@bp.route('/pca', methods=['GET', 'POST'])
@require_dataset
def pca_page(df, table_html, validation_results):

    return render_template('algorithms/pca_page.html',
                           algorithm_name="PCA",
                           table_html=table_html,
                           preview_success="Data loaded successfully.",
                           validation_results=validation_results)


@bp.route('/tsne')
def tsne_page():
    return "T-SNE Algorithm Page - Work in Progress"

@bp.route('/nca')
def nca_page():
    return "NCA Algorithm Page - Work in Progress"

@bp.route('/lle')
def lle_page():
    return "LLE Algorithm Page - Work in Progress"

@bp.route('/lda')
def lda_page():
    return "LDA Algorithm Page - Work in Progress"

@bp.route('/kpca')
def kpca_page():
    return "KPCA Algorithm Page - Work in Progress"

# ========== OTHER ERROR HANDLERS ==========

@bp.app_errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash(f"File is too large. The maximum allowed size is {current_app.config['MAX_CONTENT_LENGTH'] / 1024 / 1024:.0f} MB.")
    return redirect(url_for('main.index_page'))