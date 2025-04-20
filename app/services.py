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

# ========== ALGORITHMS PIPELINES ==========

def run_pca_pipeline(pca_instance):
    features, target_series = pca_instance.preprocess()
    transformed = pca_instance.process_algorithm(features, target_series)

    if transformed is None:
        return None, None, None, f"An error occurred while generating the PCA graph: {pca_instance.error_message}"

    pca_instance.plot_graph(transformed, target_series)

    return pca_instance.graph_path, pca_instance.time, pca_instance.explained_variance, None
