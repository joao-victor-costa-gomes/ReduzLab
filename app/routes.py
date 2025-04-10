import os
from flask import Blueprint, render_template, request, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from .utils.file_handler import save_csv_file
from .utils.file_validator import validate_file
from .services import read_data_preview
from .reduction.reducer import Reducer

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pca', methods=['GET', 'POST'])
def reduction_pca():
    message = None
    message_type = None
    table_html = None

    if request.method == 'POST':
        form_type = request.form.get("form_type")


        # PARAMETERS FORM (after successfully file upload)
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

            # 🆕 Recarrega a tabela de preview da base original
            table_html = read_data_preview(dataset_path)

            # Get the form parameters
            sample_rate_str = request.form.get('sample_rate')         # Ex: "80"
            target = request.form.get('target')                       # Ex: "price_range"
            dimension_str = request.form.get('dimension')             # Ex: "2" ou "3"
            plot_type = request.form.get('plot_type')                 # Ex: "png" ou "html"
            scaler = request.form.get('scaler')                       # Ex: "none", "standard", "minmax"

            try:
                sample_rate = float(sample_rate_str) / 100
                if not 0 < sample_rate <= 1:
                    raise ValueError("Invalid sample rate range.")
            except ValueError:
                message = "Invalid sample rate. Please enter a value between 1 and 100."
                message_type = 'error'
                return render_template(
                    'pca_page.html',
                    message=message,
                    message_type=message_type,
                    table_html=table_html  # ✅ Mantém a tabela na tela mesmo com erro
                )

            reducer = Reducer(database=dataset_path, sample_rate=sample_rate)
            reducer.preprocess()

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

    return render_template(
        'pca_page.html',
        message=message,
        message_type=message_type,
        table_html=table_html
    )
