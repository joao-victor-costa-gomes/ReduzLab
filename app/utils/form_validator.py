import pandas as pd
from flask_babel import gettext as _

# ========== SINGLE PARAMETER VALIDATORS ==========

def _validate_sample_rate(form):
    """Validates the sample rate parameter."""
    try:
        sample_rate = float(form.get('sample_rate'))
        if not 1 <= sample_rate <= 100:
            return None, _("Sample Rate must be between 1 and 100.")
        return sample_rate / 100.0, None 
    except (ValueError, TypeError):
        return None, _("Sample Rate must be a valid number.")

def _validate_target_column(form, df):
    """Validates the target column parameter."""
    target_column = form.get('target_column')
    if not target_column:
        return None, _("You must select a Target Column.")
    if target_column not in df.columns:
        return None, _('Error: Column "%(column)s" not found in the dataset.', column=target_column)
    return target_column, None

def _validate_dimension(form):
    """Validates the output dimension parameter."""
    try:
        dimension = int(form.get('dimension'))
        if dimension not in [2, 3]:
            return None, _("Dimension must be 2D or 3D.")
        return dimension, None
    except (ValueError, TypeError):
        return None, _("Dimension must be a valid number (2 or 3).")

def _validate_scaler(form):
    """Validates the scaler parameter."""
    scaler = form.get('scaler', 'none')
    if scaler not in ['none', 'standard', 'minmax']:
        return None, _("Invalid scaler selected.")
    return scaler, None

def _validate_plot_options(form):
    """Validates the plot-related parameters."""
    plot_params = {}
    plot_params['plot_type'] = form.get('plot_type', 'png')
    plot_params['plot_title'] = form.get('plot_title', '') 
    
    if plot_params['plot_type'] not in ['png', 'html']:
        return None, _("Invalid plot type selected.")

    axis_params = ['x_min', 'x_max', 'y_min', 'y_max']
    for param_name in axis_params:
        param_value = form.get(param_name)
        if param_value:
            try:
                plot_params[param_name] = float(param_value)
            except ValueError:
                return None, _('Axis range value for "%(param)s" must be a valid number.', param=param_name)
        else:
            plot_params[param_name] = None
            
    return plot_params, None

# ========== GENERAL VALIDATOR ==========

def validate_base_parameters(form, df):
    """
    Validates all base parameters by calling individual validation functions.
    Stops and returns the first error found.
    """
    params = {}
    
    # --- Algorithm Parameters ---
    sample_rate, error = _validate_sample_rate(form)
    if error: return None, error
    params['sample_rate'] = sample_rate

    target_column, error = _validate_target_column(form, df)
    if error: return None, error
    params['target_column'] = target_column

    dimension, error = _validate_dimension(form)
    if error: return None, error
    params['dimension'] = dimension

    scaler, error = _validate_scaler(form)
    if error: return None, error
    params['scaler'] = scaler
    
    # --- Graph Parameters ---
    plot_options, error = _validate_plot_options(form)
    if error: return None, error
    params.update(plot_options) # Merge the plot options dict into params

    return params, None