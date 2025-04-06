import pandas as pd

def validate_file(file, filename):
    file.seek(0)  # Read from the beginning of the file
    try:
        if filename.endswith('.csv'):
            pd.read_csv(file)  # Try read as CSV file
        elif filename.endswith('.xlsx'):
            pd.read_excel(file)  # Try read as CSV XSLX file
        else:
            raise ValueError("Unsupported file extension.")
        file.seek(0)  # Go back to the begnning after validation
        return True, None
    except Exception as e:
        file.seek(0)  # Go back to the begnning (dk why but it's important)
        return False, str(e)
