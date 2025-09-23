from ..form_validator import validate_base_parameters
from flask_babel import gettext as _

def validate_nca_parameters(form, df):
    # validate all the base parameters
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    # validate the NCA-specific advanced parameters
    try:
        # Initialization Method
        init_method = form.get('init', 'auto')
        allowed_inits = ['auto', 'pca', 'lda', 'identity', 'random']
        if init_method not in allowed_inits:
            return None, _("Invalid Initialization Method selected.")
        params['init'] = init_method

        # Max Iterations
        params['max_iter'] = int(form.get('max_iter', 50))
        if params['max_iter'] <= 0:
            return None, _("Max Iterations must be a positive number.")
            
        # Tolerance
        params['tol'] = float(form.get('tol', 1e-5))
        if params['tol'] < 0:
            return None, _("Tolerance cannot be negative.")

        # Random State (optional)
        random_state_str = form.get('random_state')
        params['random_state'] = int(random_state_str) if random_state_str else None

    except (ValueError, TypeError) as e:
        return None, _('Invalid value in advanced parameters: %(error)s', error=e)

    return params, None