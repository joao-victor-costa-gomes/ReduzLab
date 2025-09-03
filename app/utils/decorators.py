import os
from functools import wraps
from flask import session, flash, redirect, url_for, current_app
from .data_preview import generate_preview
from .data_validator import validate_dataframe

def require_dataset(f):
    """
    A decorator that checks if a valid dataset filename is in the session.
    If not, it redirects to the home page.
    If it is, it loads the dataset, validates it, and passes the results
    to the decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        filename = session.get('uploaded_filename')

        # Check if a filename exists in the session
        if not filename:
            flash("Please upload a dataset first to continue.")
            return redirect(url_for('main.index_page'))

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Check if the file physically exists on the server
        if not os.path.exists(file_path):
            flash("The uploaded file could not be found. Please upload it again.")
            session.pop('uploaded_filename', None) # Clean up the stale session variable
            return redirect(url_for('main.index_page'))

        # Try to load and process the data
        df, table_html, preview_error = generate_preview(file_path)

        if preview_error:
            flash(f"An error occurred while reading your file: {preview_error}")
            return redirect(url_for('main.index_page'))
        
        # If all checks pass, run the validation
        validation_results = validate_dataframe(df)

        # Call the original route function (e.g., pca_page), passing the loaded data as keyword arguments.
        return f(df=df, table_html=table_html, validation_results=validation_results, *args, **kwargs)

    return decorated_function