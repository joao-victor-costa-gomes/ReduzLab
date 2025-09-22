from ..form_validator import validate_base_parameters
from flask_babel import gettext as _

def validate_lle_parameters(form, df):
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    try:
        # Number of Neighbors
        params['n_neighbors'] = int(form.get('n_neighbors', 10))
        if params['n_neighbors'] <= 0:
            return None, _("Number of Neighbors must be a positive number.")

        # Regularization
        params['reg'] = float(form.get('reg', 1e-3))

        # Dropdowns
        params['method'] = form.get('method', 'standard')
        if params['method'] not in ['standard', 'hessian', 'modified', 'ltsa']:
            return None, _("Invalid Method selected.")
            
        params['eigen_solver'] = form.get('eigen_solver', 'auto')
        if params['eigen_solver'] not in ['auto', 'arpack', 'dense']:
            return None, _("Invalid Eigen Solver selected.")

        params['neighbors_algorithm'] = form.get('neighbors_algorithm', 'auto')
        allowed_algos = ['auto', 'brute', 'kd_tree', 'ball_tree']
        if params['neighbors_algorithm'] not in allowed_algos:
            return None, _("Invalid Neighbors Algorithm selected.")

        # Optional Integers
        rs_str = form.get('random_state')
        params['random_state'] = int(rs_str) if rs_str else None

        n_jobs_str = form.get('n_jobs')
        params['n_jobs'] = int(n_jobs_str) if n_jobs_str else None

    except (ValueError, TypeError) as e:
        return None, _('Invalid value in advanced parameters: %(error)s', error=e)

    return params, None