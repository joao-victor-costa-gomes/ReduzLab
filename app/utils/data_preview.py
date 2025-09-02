import pandas as pd

def generate_preview(file_path):
    """
    Reads a data file from the given path and returns a tuple:
    (html_table, error_message).
    One of the two will be None.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else: # .xlsx
            df = pd.read_excel(file_path)
        
        # Convert the first 10 rows to an HTML table
        table_html = df.head(10).to_html(classes='data-table', index=False)
        return table_html, None # Success: return table, no error
    except Exception as e:
        error_message = f"Error reading or processing file: {e}"
        return None, error_message # Failure: return no table, an error message