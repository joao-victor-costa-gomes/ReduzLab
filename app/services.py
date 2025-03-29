import pandas as pd

def read_csv_preview(file_path, n_rows=10):
    try:
        df = pd.read_csv(file_path)
        return df.head(n_rows).to_html(classes='data-table', index=False)
    except Exception as e:
        print(f"[Erro ao ler CSV] {e}")
        return None