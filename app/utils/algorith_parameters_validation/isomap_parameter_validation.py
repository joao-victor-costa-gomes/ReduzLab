from ..form_validator import validate_base_parameters

def validate_isomap_parameters(form, df):
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    try:
        # n_neighbors
        params['n_neighbors'] = int(form.get('n_neighbors', 10))
        if params['n_neighbors'] <= 0:
            return None, "Number of Neighbors must be a positive number."

        # Dropdowns
        params['metric'] = form.get('metric', 'minkowski')
        if params['metric'] not in ['minkowski', 'cosine', 'manhattan']:
            return None, "Invalid Metric selected."

        params['eigen_solver'] = form.get('eigen_solver', 'auto')
        if params['eigen_solver'] not in ['auto', 'arpack', 'dense']:
            return None, "Invalid Eigen Solver selected."

        params['path_method'] = form.get('path_method', 'auto')
        if params['path_method'] not in ['auto', 'FW', 'D']:
            return None, "Invalid Path Method selected."

        params['neighbors_algorithm'] = form.get('neighbors_algorithm', 'auto')
        if params['neighbors_algorithm'] not in ['auto', 'brute', 'kd_tree', 'ball_tree']:
            return None, "Invalid Neighbors Algorithm selected."

        # Optional Integer
        n_jobs_str = form.get('n_jobs')
        params['n_jobs'] = int(n_jobs_str) if n_jobs_str else None

    except (ValueError, TypeError) as e:
        return None, f"Invalid value in advanced parameters: {e}"

    return params, None