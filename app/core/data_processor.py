from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

def process_data_for_reduction(df, params):
    """
    Prepares the dataframe for a dimensionality reduction algorithm.
    - Applies sampling
    - Separates features and target
    - Applies scaling
    """
    # Apply sampling (in-memory)
    df_sampled = df.sample(frac=params['sample_rate'], random_state=42)

    # Separate features (X) and target (y)
    target_series = df_sampled[params['target_column']]
    features_df = df_sampled.drop(columns=[params['target_column']])
    
    # Select only numeric features for the algorithm
    X = features_df.select_dtypes(include='number')

    # Apply scaler if specified
    if params['scaler'] == 'standard':
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns)
    elif params['scaler'] == 'minmax':
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns)

    return X, target_series