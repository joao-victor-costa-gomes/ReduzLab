def validate_dataframe(df):
    """
    Validates a pandas DataFrame for non-numeric columns and null values.

    Args:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        dict: A dictionary containing validation results, including a list
              of non-numeric columns and a dictionary of columns with null counts.
    """
    # Find columns that are not numeric (excluding boolean types)
    non_numeric_cols = df.select_dtypes(exclude=['number', 'bool']).columns.tolist()

    # Find columns with null values and count them
    null_counts = df.isnull().sum()
    null_info = null_counts[null_counts > 0].to_dict()

    validation_results = {
        'non_numeric_cols': non_numeric_cols,
        'null_info': null_info
    }
    
    return validation_results