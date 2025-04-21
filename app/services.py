import pandas as pd
from flask import render_template

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

# ========== ALGORITHMS PIPELINES ==========

def run_pca_pipeline(pca_instance):
    features, target_series = pca_instance.preprocess()
    transformed = pca_instance.process_algorithm(features, target_series)
    if transformed is None:
        return None, None, None, f"An error occurred while generating the PCA graph: {pca_instance.error_message}"
    pca_instance.plot_graph(transformed, target_series)
    return pca_instance.graph_path, pca_instance.time, pca_instance.explained_variance, None

def run_tsne_pipeline(tsne_instance):
    try:
        features, target_series = tsne_instance.preprocess()
        if features is None:
            return None, None, None, "Preprocessing failed. Check your target column or sample rate."
        transformed = tsne_instance.process_algorithm(features, target_series)
        if transformed is None:
            return None, None, None, tsne_instance.error_message
        tsne_instance.plot_graph(transformed, target_series)
        return tsne_instance.graph_path, tsne_instance.time, None, None
    except Exception as e:
        return None, None, None, str(e)

