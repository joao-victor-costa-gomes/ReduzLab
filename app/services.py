import pandas as pd

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
