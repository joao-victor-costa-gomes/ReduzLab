from ..form_validator import validate_base_parameters
from flask_babel import gettext as _

def validate_pca_parameters(form, df):
    # validate all the base parameters
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    # validate the PCA-specific advanced parameters
    
    # 'whiten' is a checkbox. The key 'whiten' will be in the form if it was checked.
    params['whiten'] = 'whiten' in form
    # 'svd_solver'
    svd_solver = form.get('svd_solver', 'auto')
    allowed_solvers = ['auto', 'full', 'covariance_eigh', 'arpack', 'randomized']
    if svd_solver not in allowed_solvers:
        return None, _("Invalid SVD solver selected.")
    params['svd_solver'] = svd_solver
    # 'random_state' is optional
    random_state_str = form.get('random_state')
    if random_state_str: # If the user provided a value
        try:
            params['random_state'] = int(random_state_str)
        except (ValueError, TypeError):
            return None, _("Random State must be a valid integer.")
    else:
        params['random_state'] = None

    return params, None