import pandas as pd
from flask import Blueprint, render_template, request, session, url_for, current_app, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from .services import read_data_preview

# algorithms imports
from .algorithms.pca import PCA

# utils.py imports
from .utils.file_handler import save_uploaded_file
from .utils.validators import validate_file, validate_sample_rate, validate_target_column, validate_dimension,  validate_plot_type, validate_scaler
        

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
            # ---------- UPLOAD SECTION HANDLER ----------
            if file and file.filename:
                # Validate file type and content
                is_valid, validation_error = validate_file(file, file.filename)  
                if is_valid:
                    # Save the file to the uploads folder
                    saved_path = save_uploaded_file(file, file.filename)
                    session['uploaded_dataset_path'] = saved_path
                    table_html = read_data_preview(saved_path) 
                    # ---------- TABLE PREVIEW SECTION HANDLER ----------
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

@main.route('/pca', methods=['GET', 'POST'])
def pca_page():
    table_html = None
    # Feedback messages for the table_preview section
    preview_error = None
    preview_success = None
    # PCA variables
    param_error = None
    param_success = None
    graph_url = None
    # Post-processing values
    time = None
    explained_variance = None

    dataset_path = session.get('uploaded_dataset_path')

    if dataset_path:
        table_html = read_data_preview(dataset_path)
        # ---------- TABLE PREVIEW SECTION HANDLER ----------
        if table_html is None:
            preview_error = "Failed to load preview table. The file might be corrupted or missing."
        else:
            preview_success = "Preview table loaded successfully!"
    else:
        preview_error = f'No uploaded file found in session. Please <a href="{url_for("main.index")}">upload a file</a> first.'

    # ---------- PCA PARAMETERS HANDLER ----------
    if request.method == 'POST' and request.form.get("form_type") == "params":
        df = pd.read_csv(dataset_path)

        sample_rate, error_response = validate_sample_rate(request.form, table_html)
        if error_response: return error_response

        target = request.form.get('target')
        is_valid_target, error_response = validate_target_column(target, df, table_html)
        if error_response: return error_response

        dimension, error_response = validate_dimension(request.form.get('dimension'), table_html)
        if error_response: return error_response

        plot_type, error_response = validate_plot_type(request.form.get('plot_type'), table_html)
        if error_response: return error_response

        scaler, error_response = validate_scaler(request.form.get('scaler'), table_html)
        if error_response: return error_response

        pca = PCA(
            database=dataset_path,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )

        features, target_series = pca.preprocess()
        transformed = pca.process_algorithm(features, target_series)

        if transformed is None:
            param_error = f"An error occurred while generating the PCA graph: {pca.error_message}"
        else:
            pca.plot_graph(transformed, target_series)
            graph_url = url_for('main.results_file_path', filename=pca.graph_path)
            time = pca.time
            explained_variance = pca.explained_variance
            param_success = f"PCA completed successfully! Output: {dimension}D - Scaler: {scaler}"

    return render_template(
        'pca_page.html',
        table_html=table_html,
        preview_error=preview_error,
        preview_success=preview_success,
        param_error=param_error,
        param_success=param_success,
        graph_url=graph_url,
        time=time,
        explained_variance=explained_variance
    )

@main.route('/results/<path:filename>')
def results_file_path(filename):
    return send_from_directory(current_app.config['RESULTS_FOLDER'], filename)