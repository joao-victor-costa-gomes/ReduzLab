from ..form_validator import validate_base_parameters

def validate_kpca_parameters(form, df):
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    try:
        # Kernel
        kernel = form.get('kernel', 'linear')
        allowed_kernels = ['linear', 'poly', 'rbf', 'sigmoid', 'cosine']
        if kernel not in allowed_kernels:
            return None, "Invalid Kernel selected."
        params['kernel'] = kernel

        # Kernel-specific params
        gamma_str = form.get('gamma')
        params['gamma'] = float(gamma_str) if gamma_str else None

        degree_str = form.get('degree')
        params['degree'] = int(degree_str) if degree_str else 3

        coef0_str = form.get('coef0')
        params['coef0'] = float(coef0_str) if coef0_str else 1
        
        # Solver
        eigen_solver = form.get('eigen_solver', 'auto')
        if eigen_solver not in ['auto', 'dense', 'arpack', 'randomized']:
            return None, "Invalid Eigen Solver selected."
        params['eigen_solver'] = eigen_solver

        # Optional Integers
        rs_str = form.get('random_state')
        params['random_state'] = int(rs_str) if rs_str else None

        n_jobs_str = form.get('n_jobs')
        params['n_jobs'] = int(n_jobs_str) if n_jobs_str else None

    except (ValueError, TypeError) as e:
        return None, f"Invalid value in advanced parameters: {e}"

    return params, None