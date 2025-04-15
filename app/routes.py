import os
import pandas as pd
from flask import Blueprint, render_template, request, session, send_from_directory, current_app, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from .utils.file_handler import save_csv_file
from .utils.file_validator import validate_file
from .utils.param_validator import validate_sample_rate, validate_target_column

from .services import read_data_preview
from .algorithms.pca import PCA

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pca', methods=['GET', 'POST'])
def reduction_pca():
    message = None
    message_type = None
    table_html = None
    graph_url = None
    plot_type = None
    time = None
    explained_variance = None

    if request.method == 'POST':
        form_type = request.form.get("form_type")

        # PARAMETERS FORM
        if form_type == "params":
            dataset_path = session.get("uploaded_dataset_path")
            if not dataset_path or not os.path.exists(dataset_path):
                message = "Dataset not found. Please upload the file again."
                message_type = 'error'
                return render_template(
                    'pca_page.html',
                    message=message,
                    message_type=message_type,
                    table_html=None
                )

            # Reloads the preview table
            table_html = read_data_preview(dataset_path)                      

            # ----- sample_rate VALIDATION -----
            sample_rate_str = request.form.get('sample_rate')    
            sample_rate, error_response = validate_sample_rate(request.form, table_html)
            if error_response:
                return error_response

            # ----- target VALIDATION -----
            target = request.form.get('target')
            df = pd.read_csv(session.get("uploaded_dataset_path"))

            is_valid_target, error_response = validate_target_column(target, df, read_data_preview(df))
            if error_response:
                return error_response

            # RECEBA
            dimension_str = request.form.get('dimension')             
            plot_type = request.form.get('plot_type')                 
            scaler = request.form.get('scaler') 

            pca = PCA(
                database=dataset_path,
                sample_rate=sample_rate,
                target=target,
                dimension=int(dimension_str),
                plot_type=plot_type,
                scaler=scaler
            )

            pca.run()

            time = pca.time
            explained_variance = pca.explained_variance
            graph_url = url_for('main.results_file_path', filename=pca.graph_path) if pca.graph_path else None

            message = (
                f"✅ Sample generated with {sample_rate * 100:.0f}% of the data. "
                f"Target: '{target}', "
                f"Dimension: {dimension_str}, "
                f"Plot Type: {plot_type.upper()}, "
                f"Scaler: {scaler.capitalize()}."
            )
            message_type = 'success'


        #  FILE UPLOAD FORM
        else:
            try:
                file = request.files.get('file')
                if file:
                    filename = secure_filename(file.filename)
                    if filename.endswith(('.csv', '.xlsx')):
                        is_valid, error_message = validate_file(file, filename)

                        if is_valid:
                            saved_path = save_csv_file(file, filename)
                            table_html = read_data_preview(saved_path)
                            session['uploaded_dataset_path'] = saved_path  # Saves the path in the session
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

    print("graph_url:", graph_url, type(graph_url))
    print("plotype:", plot_type)

    return render_template(
        'pca_page.html',
        message=message,
        message_type=message_type,
        table_html=table_html,
        graph_url=graph_url,
        plot_type=plot_type,
        time=time,
        explained_variance=explained_variance
    )

@main.route('/results/<path:filename>')
def results_file_path(filename):
    return send_from_directory(current_app.config['RESULTS_FOLDER'], filename)