from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

def process_data_for_reduction(df, params):
    """
    Prepares the dataframe for a dimensionality reduction algorithm.
    - Applies Stratified sampling (if a target is present)
    - Separates features and target
    - Applies scaling
    """
    target_col = params['target_column']
    frac_rate = float(params['sample_rate'])
    
    # 1. Aplicar Amostragem Estratificada
    if target_col in df.columns and 0.0 < frac_rate < 1.0:
        # Agrupa pelas classes do target e extrai a amostra proporcional de cada uma
        df_sampled = df.groupby(target_col, group_keys=False).apply(
            lambda x: x.sample(frac=frac_rate, random_state=42)
        )
    elif frac_rate < 1.0:
        # Fallback: Amostragem simples caso o target falhe ou não exista
        df_sampled = df.sample(frac=frac_rate, random_state=42)
    else:
        # Se a taxa for 1.0 (100%), usa o dataset inteiro sem gastar CPU amostrando
        df_sampled = df.copy()

    # 2. Separar features (X) e target (y)
    target_series = df_sampled[target_col]
    features_df = df_sampled.drop(columns=[target_col])
    
    # 3. Selecionar apenas colunas numéricas para os algoritmos
    X = features_df.select_dtypes(include='number')

    # 4. Aplicar o scaler (padronização dos dados)
    if params['scaler'] == 'standard':
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    elif params['scaler'] == 'minmax':
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

    return X, target_series