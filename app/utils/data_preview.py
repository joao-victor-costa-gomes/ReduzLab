import pandas as pd

def generate_preview(file_path):
    """
    Reads a data file and returns a tuple: (dataframe, html_table, error_message).
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else: # .xlsx
            df = pd.read_excel(file_path)
        
        # Convert the first 5 rows to an HTML table
        table_html = df.head(10).to_html(classes='table table-hover table-bordered text-nowrap', index=False)
        # Return the full DataFrame, the HTML table, and no error
        return df, table_html, None
    except Exception as e:
        error_message = f"Error reading or processing file: {e}"
        # Return None for the DataFrame and table, and the error message
        return None, None, error_message