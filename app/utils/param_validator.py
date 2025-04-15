from flask import render_template
import pandas as pd

def validate_sample_rate(request_form, table_html):
    sample_rate_str = request_form.get('sample_rate')
    try:
        sample_rate = float(sample_rate_str) / 100
        if not 0 < sample_rate <= 1:
            raise ValueError
        return sample_rate, None
    except (TypeError, ValueError):
        return None, render_template(
            'pca_page.html',
            message="Invalid sample rate. Please enter a value between 1 and 100.",
            message_type='error',
            table_html=table_html
        )

def validate_target_column(target, df, table_html):
    if not target or target.strip() == "":
        return False, render_template(
            'pca_page.html',
            message="Please provide a valid target column name.",
            message_type='error',
            table_html=table_html
        )

    if target not in df.columns:
        available = ", ".join(df.columns.tolist())
        return False, render_template(
            'pca_page.html',
            message=f"The column '{target}' does not exist in the dataset. Available columns: {available}.",
            message_type='error',
            table_html=table_html
        )

    return True, None

def validate_dimension(dimension_str, table_html):
    try:
        dimension = int(dimension_str)
        if dimension not in [2, 3]:
            raise ValueError
        return dimension, None
    except (TypeError, ValueError):
        return None, render_template(
            'pca_page.html',
            message="Invalid dimension. Please enter '2' or '3'.",
            message_type='error',
            table_html=table_html
        )

def validate_plot_type(plot_type, table_html):
    if plot_type not in ['png', 'html']:
        return None, render_template(
            'pca_page.html',
            message="Invalid plot type. Please select 'png' or 'html'.",
            message_type='error',
            table_html=table_html
        )
    return plot_type, None

def validate_scaler(scaler, table_html):
    if scaler not in ['none', 'standard', 'minmax']:
        return None, render_template(
            'pca_page.html',
            message="Invalid scaler type. Please select 'none', 'standard' or 'minmax'.",
            message_type='error',
            table_html=table_html
        )
    return scaler, None