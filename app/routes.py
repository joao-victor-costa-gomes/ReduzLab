from flask import Blueprint, render_template, request, session, current_app, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge

# servives imports
from .services import read_data_preview, handle_algorithm_request

# algorithms imports
from .algorithms.pca import PCA
from .services import run_pca_pipeline

from .algorithms.tsne import TSNE
from .services import run_tsne_pipeline

from .algorithms.lda import LDA
from .services import run_lda_pipeline

from .algorithms.nca import NCA
from .services import run_nca_pipeline

from .algorithms.lle import LLE
from .services import run_lle_pipeline, handle_algorithm_request

# utils.py imports
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
    # Preview table data
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

# ========== ALGORITHMS VIEWS ==========

@main.route('/pca', methods=['GET', 'POST'])
def pca_page():
    return handle_algorithm_request(
        request=request,
        session_key='uploaded_dataset_path',
        algorithm_cls=PCA,
        pipeline_func=run_pca_pipeline,
        template_name='pca_page.html',
        algorithm_name='PCA'
    )

@main.route('/tsne', methods=['GET', 'POST'])
def tsne_page():
    return handle_algorithm_request(
        request=request,
        session_key='uploaded_dataset_path',
        algorithm_cls=TSNE,
        pipeline_func=run_tsne_pipeline,
        template_name='tsne_page.html',
        algorithm_name='T-SNE'
    )

@main.route('/lda', methods=['GET', 'POST'])
def lda_page():
    return handle_algorithm_request(
        request=request,
        session_key='uploaded_dataset_path',
        algorithm_cls=LDA,
        pipeline_func=run_lda_pipeline,
        template_name='lda_page.html',
        algorithm_name='LDA'
    )

@main.route('/nca', methods=['GET', 'POST'])
def nca_page():
    return handle_algorithm_request(
        request=request,
        session_key='uploaded_dataset_path',
        algorithm_cls=NCA,
        pipeline_func=run_nca_pipeline,
        template_name='nca_page.html',
        algorithm_name='NCA'
    )

@main.route('/lle', methods=['GET', 'POST'])
def lle_page():
    return handle_algorithm_request(
        request=request,
        session_key='uploaded_dataset_path',
        algorithm_cls=LLE,
        pipeline_func=run_lle_pipeline,
        template_name='lle_page.html',
        algorithm_name='LLE'
    )

# ========== OTHERS ==========

@main.route('/results/<path:filename>')
def results_file_path(filename):
    return send_from_directory(current_app.config['RESULTS_FOLDER'], filename)

@main.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(
        current_app.config['RESULTS_FOLDER'],
        filename,
        as_attachment=True
    )