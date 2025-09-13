from ..form_validator import validate_base_parameters

def validate_tsne_parameters(form, df):
    """
    Validates all parameters for the T-SNE algorithm.
    First validates base parameters, then T-SNE specific advanced parameters.
    """
    # 1. First, validate all the base parameters
    params, error = validate_base_parameters(form, df)
    if error:
        return None, error

    # 2. Now, validate the T-SNE-specific advanced parameters
    
    # Perplexity
    try:
        perplexity = float(form.get('perplexity', 30.0))
        if not (5 <= perplexity < len(df)):
            return None, f"Perplexity must be between 5 and the number of samples ({len(df)})."
        params['perplexity'] = perplexity
    except (ValueError, TypeError):
        return None, "Perplexity must be a valid number."

    # Learning Rate
    learning_rate_str = form.get('learning_rate', 'auto')
    if learning_rate_str != 'auto':
        try:
            learning_rate = float(learning_rate_str)
            if not (10.0 <= learning_rate <= 1000.0):
                return None, "Learning Rate should typically be between 10.0 and 1000.0."
            params['learning_rate'] = learning_rate
        except (ValueError, TypeError):
            return None, "Learning Rate must be a valid number or 'auto'."
    else:
        params['learning_rate'] = 'auto'

    # Max Iterations
    try:
        max_iter = int(form.get('max_iter', 1000))
        if max_iter < 250:
            return None, "Max Iterations should be at least 250."
        params['max_iter'] = max_iter
    except (ValueError, TypeError):
        return None, "Max Iterations must be a valid integer."

    # Initialization Method
    init_method = form.get('init', 'pca')
    if init_method not in ['pca', 'random']:
        return None, "Invalid Initialization Method selected."
    params['init'] = init_method

    # Random State
    random_state_str = form.get('random_state')
    if random_state_str:
        try:
            params['random_state'] = int(random_state_str)
        except (ValueError, TypeError):
            return None, "Random State must be a valid integer."
    else:
        params['random_state'] = None
        
    # --- Fine-tuning parameters ---
    
    # Early Exaggeration
    try:
        early_exaggeration = float(form.get('early_exaggeration', 12.0))
        if early_exaggeration < 1.0:
            return None, "Early Exaggeration must be at least 1.0."
        params['early_exaggeration'] = early_exaggeration
    except (ValueError, TypeError):
        return None, "Early Exaggeration must be a valid number."
        
    # Method
    method = form.get('method', 'barnes_hut')
    if method not in ['barnes_hut', 'exact']:
        return None, "Invalid Method selected."
    params['method'] = method

    # Metric
    metric = form.get('metric', 'euclidean')
    allowed_metrics = ['euclidean', 'cosine', 'manhattan', 'chebyshev', 'correlation']
    if metric not in allowed_metrics:
        return None, "Invalid Distance Metric selected."
    params['metric'] = metric

    # n_jobs
    n_jobs_str = form.get('n_jobs')
    if n_jobs_str:
        try:
            params['n_jobs'] = int(n_jobs_str)
        except (ValueError, TypeError):
            return None, "Parallel Jobs (n_jobs) must be a valid integer."
    else:
        params['n_jobs'] = None

    return params, None