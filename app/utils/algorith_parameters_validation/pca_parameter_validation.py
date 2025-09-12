from ..form_validator import validate_base_parameters

def validate_pca_parameters(form, df):
    # validate all the base parameters
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    # validate the PCA-specific advanced parameters
    params['whiten'] = 'whiten' in form

    svd_solver = form.get('svd_solver', 'auto')
    allowed_solvers = ['auto', 'full', 'covariance_eigh', 'arpack', 'randomized']
    if svd_solver not in allowed_solvers:
        return None, "Invalid SVD solver selected."
    params['svd_solver'] = svd_solver

    random_state_str = form.get('random_state')
    if random_state_str: 
        try:
            params['random_state'] = int(random_state_str)
        except (ValueError, TypeError):
            return None, "Random State must be a valid integer."
    else:
        params['random_state'] = None

    return params, None