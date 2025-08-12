import pandas as pd
from flask import render_template, request, session, url_for
from .utils.validators import validate_all_parameters

# ========== OTHERS ==========

def read_data_preview(file_path, n_rows=5):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return None 
        return df.head(n_rows).to_html(classes='data-table', index=False)
    except Exception as e:
        print(f"[Erro reading file] {e}")
        return None

def is_valid_target_column(df, target, table_html, column_options):
    if target not in df.columns:
        return render_template(
            'pca_page.html',
            table_html=table_html,
            column_options=column_options,
            param_error=f"The column '{target}' does not exist in the dataset."
        )
    if not pd.api.types.is_numeric_dtype(df[target]):
        return render_template(
            'pca_page.html',
            table_html=table_html,
            column_options=column_options,
            param_error=f"The selected target column '{target}' contains non-numeric values. Please choose a column with numeric or encoded categorical values."
        )
    return None  


# ========== ALGORITHM PAGE BASE ==========

def handle_algorithm_request(request, session_key, algorithm_cls, pipeline_func, template_name, algorithm_name):
    table_html = None
    preview_error = None
    preview_success = None
    param_error = None
    param_success = None
    graph_url = None
    reduced_data_url = None
    time = None
    explained_variance = None
    column_options = None

    dataset_path = session.get(session_key)

    if dataset_path:
        df = pd.read_csv(dataset_path)
        table_html = df.head(5).to_html(classes='data-table', index=False)
        column_options = df.columns.tolist()

        if table_html is None:
            preview_error = "Failed to load preview table. The file might be corrupted or missing."
        else:
            preview_success = "Preview table loaded successfully!"
    else:
        preview_error = f'No uploaded file found in session. Please <a href="{url_for("main.index")}">upload a file</a> first.'

    if request.method == 'POST' and request.form.get("form_type") == "params":
        sample_rate, target, dimension, plot_type, scaler, error_response = validate_all_parameters(
            request.form, dataset_path, table_html
        )

        if error_response:
            return error_response

        target_check = is_valid_target_column(df, target, table_html, column_options)
        if target_check:
            return target_check

        algorithm = algorithm_cls(
            database=dataset_path,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )

        graph_path, time, explained_variance, pipeline_error = pipeline_func(algorithm)

        if pipeline_error:
            param_error = pipeline_error
        else:
            graph_url = url_for('main.results_file_path', filename=graph_path)
            reduced_data_url = url_for('main.download_file', filename=algorithm.reduced_data_path)
            param_success = f"{algorithm_name} completed successfully! Output: {dimension}D - Scaler: {scaler}"

    return render_template(
        template_name,
        table_html=table_html,
        preview_error=preview_error,
        preview_success=preview_success,
        column_options=column_options,
        param_error=param_error,
        param_success=param_success,
        graph_url=graph_url,
        time=time,
        explained_variance=explained_variance,
        reduced_data_url=reduced_data_url
    )

# ========== ALGORITHMS PIPELINES ==========

def run_pca_pipeline(pca_instance):
    features, target_series = pca_instance.preprocess()
    transformed = pca_instance.process_algorithm(features, target_series)
    if transformed is None:
        return None, None, None, f"An error occurred while generating the PCA graph: {pca_instance.error_message}"
    pca_instance.plot_graph(transformed, target_series)
    return pca_instance.graph_path, pca_instance.time, pca_instance.explained_variance, None

def run_tsne_pipeline(tsne_instance):
    features, target_series = tsne_instance.preprocess()
    transformed = tsne_instance.process_algorithm(features, target_series)
    if transformed is None:
        return None, None, None, f"An error occurred while generating the T-SNE graph: {tsne_instance.error_message}"
    tsne_instance.plot_graph(transformed, target_series)
    return tsne_instance.graph_path, tsne_instance.time, None, None

def run_lda_pipeline(lda_instance):
    features, target_series = lda_instance.preprocess()
    transformed = lda_instance.process_algorithm(features, target_series)
    if transformed is None:
        return None, None, None, f"An error occurred while generating the LDA graph: {lda_instance.error_message}"
    lda_instance.plot_graph(transformed, target_series)
    return lda_instance.graph_path, lda_instance.time, lda_instance.explained_variance, None

def run_nca_pipeline(nca_instance):
    features, target_series = nca_instance.preprocess()
    transformed = nca_instance.process_algorithm(features, target_series)
    if transformed is None:
        return None, None, None, f"An error occurred while generating the NCA graph: {nca_instance.error_message}"
    nca_instance.plot_graph(transformed, target_series)
    return nca_instance.graph_path, nca_instance.time, None, None

def run_lle_pipeline(lle_instance):
    try:
        features, target_series = lle_instance.preprocess()
        if features is None:
            return None, None, None, "Preprocessing failed. Check your target column or sample rate."

        transformed = lle_instance.process_algorithm(features, target_series)
        if transformed is None:
            return None, None, None, lle_instance.error_message

        lle_instance.plot_graph(transformed, target_series)
        return lle_instance.graph_path, lle_instance.time, lle_instance.explained_variance, None
    except Exception as e:
        return None, None, None, str(e)

def run_umap_pipeline(umap_instance):
    try:
        features, target_series = umap_instance.preprocess()
        if features is None:
            return None, None, None, "Preprocessing failed. Check your target column or sample rate."
        transformed = umap_instance.process_algorithm(features, target_series)
        if transformed is None:
            return None, None, None, umap_instance.error_message
        umap_instance.plot_graph(transformed, target_series)
        return umap_instance.graph_path, umap_instance.time, None, None
    except Exception as e:
        return None, None, None, str(e)

def run_kpca_pipeline(kpca_instance):
    features, target_series = kpca_instance.preprocess()
    transformed = kpca_instance.process_algorithm(features, target_series)
    if transformed is None:
        return None, None, None, f"An error occurred while generating the KPCA graph: {kpca_instance.error_message}"
    kpca_instance.plot_graph(transformed, target_series)
    return kpca_instance.graph_path, kpca_instance.time, kpca_instance.variance, None
