from ..form_validator import validate_base_parameters

def validate_tsne_parameters(form, df):
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    try:
        # Main Advanced Parameters
        params['perplexity'] = float(form.get('perplexity', 30.0))
        if not (1 <= params['perplexity'] < len(df)):
            return None, f"Perplexity must be between 1 and the number of samples ({len(df)})."

        lr_str = form.get('learning_rate', 'auto')
        params['learning_rate'] = 'auto' if lr_str == 'auto' else float(lr_str)

        params['max_iter'] = int(form.get('max_iter', 1000))
        if params['max_iter'] < 250:
            return None, "Max Iterations must be at least 250."

        params['early_exaggeration'] = float(form.get('early_exaggeration', 12.0))

        # Dropdowns
        params['init'] = form.get('init', 'pca')
        if params['init'] not in ['pca', 'random']: return None, "Invalid Init Method."
        
        params['method'] = form.get('method', 'barnes_hut')
        if params['method'] not in ['barnes_hut', 'exact']: return None, "Invalid Method."

        params['metric'] = form.get('metric', 'euclidean')
        if params['metric'] not in ['euclidean', 'cosine', 'manhattan', 'chebyshev']: return None, "Invalid Metric."

        # Optional Integers
        rs_str = form.get('random_state')
        params['random_state'] = int(rs_str) if rs_str else None

        n_jobs_str = form.get('n_jobs')
        params['n_jobs'] = int(n_jobs_str) if n_jobs_str else None

    except (ValueError, TypeError) as e:
        return None, f"Invalid value in advanced parameters: {e}"

    return params, None