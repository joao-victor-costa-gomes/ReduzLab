from ..form_validator import validate_base_parameters
from flask_babel import gettext as _

def validate_lda_parameters(form, df):
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    # Validate Solver
    solver = form.get('solver', 'svd')
    if solver not in ['svd', 'lsqr', 'eigen']:
        return None, "Invalid solver selected."
    params['solver'] = solver

    # Validate Shrinkage
    shrinkage_str = form.get('shrinkage')
    if solver == 'svd' and shrinkage_str:
        return None, _("Shrinkage cannot be used with the 'svd' solver.")
    
    if not shrinkage_str:
        params['shrinkage'] = None
    elif shrinkage_str.lower() == 'auto':
        params['shrinkage'] = 'auto'
    else:
        try:
            shrinkage_float = float(shrinkage_str)
            if not 0 <= shrinkage_float <= 1:
                return None, _("Shrinkage value must be between 0 and 1.")
            params['shrinkage'] = shrinkage_float
        except (ValueError, TypeError):
            return None, _("Shrinkage must be 'auto' or a valid number.")

    return params, None