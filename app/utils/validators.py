from flask import render_template
import pandas as pd


# ========== FILE VALIDATORS ==========

# UPLOADED FILE
def validate_file(file, filename):
    file.seek(0)  # Read from the beginning of the file
    try:
        if filename.endswith('.csv'):
            pd.read_csv(file)  # Try read as CSV file
        elif filename.endswith('.xlsx'):
            pd.read_excel(file)  # Try read as CSV XSLX file
        else:
            raise ValueError("Unsupported file extension.")
        file.seek(0)  # Go back to the begnning after validation
        return True, None
    except Exception as e:
        file.seek(0)  # Go back to the begnning (dk why but it's important)
        return False, str(e)


# ========== PARAMETERS VALIDATORS ==========

# SAMPLE RATE
def validate_sample_rate(request_form):
    sample_rate_str = request_form.get('sample_rate')
    try:
        sample_rate = float(sample_rate_str) / 100
        if not 0 < sample_rate <= 1:
            raise ValueError
        return sample_rate, None
    except (TypeError, ValueError):
        return None, "Invalid sample rate. Please enter a value between 1 and 100."

# TARGET
def validate_target_column(target, df):
    if not target or target.strip() == "":
        return False, "Please provide a valid target column name."

    if target not in df.columns:
        available = ", ".join(df.columns.tolist())
        return False, f"The column '{target}' does not exist in the dataset. Available columns: {available}."

    return True, None

# DIMENSION VALUE
def validate_dimension(dimension_str):
    try:
        dimension = int(dimension_str)
        if dimension not in [2, 3]:
            raise ValueError
        return dimension, None
    except (TypeError, ValueError):
        return None, "Invalid dimension. Please enter '2' or '3'."

# PLOT TYPE
def validate_plot_type(plot_type):
    if plot_type not in ['png', 'html']:
        return None, "Invalid plot type. Please select 'png' or 'html'."
    return plot_type, None

# SCALER
def validate_scaler(scaler):
    if scaler not in ['none', 'standard', 'minmax']:
        return None, "Invalid scaler type. Please select 'none', 'standard' or 'minmax'."
    return scaler, None

# GENERAL VALIDATOR
def validate_all_parameters(form_data, dataset_path, table_html):
    df = pd.read_csv(dataset_path)
    # Validate Sample Rate
    sample_rate, error_msg = validate_sample_rate(form_data)
    if error_msg:
        return None, None, None, None, None, render_template(
            'pca_page.html',
            param_error=error_msg,
            table_html=table_html
        )
    # Validate Target
    target = form_data.get('target')
    is_valid_target, error_msg = validate_target_column(target, df)
    if error_msg:
        return None, None, None, None, None, render_template(
            'pca_page.html',
            param_error=error_msg,
            table_html=table_html
        )
    # Validate Dimension
    dimension, error_msg = validate_dimension(form_data.get('dimension'))
    if error_msg:
        return None, None, None, None, None, render_template(
            'pca_page.html',
            param_error=error_msg,
            table_html=table_html
        )
    # Validate Plot Type
    plot_type, error_msg = validate_plot_type(form_data.get('plot_type'))
    if error_msg:
        return None, None, None, None, None, render_template(
            'pca_page.html',
            param_error=error_msg,
            table_html=table_html
        )
    # Validate Scaler
    scaler, error_msg = validate_scaler(form_data.get('scaler'))
    if error_msg:
        return None, None, None, None, None, render_template(
            'pca_page.html',
            param_error=error_msg,
            table_html=table_html
        )
    # If all validations pass, return the clean values
    return sample_rate, target, dimension, plot_type, scaler, None