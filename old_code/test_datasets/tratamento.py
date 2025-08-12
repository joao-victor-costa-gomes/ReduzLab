import pandas as pd
from sklearn.impute import SimpleImputer

# Função para remover colunas
def remove_columns_from_csv(input_path, output_path, columns_to_remove):
    df = pd.read_csv(input_path)
    if isinstance(columns_to_remove, str):
        columns_to_remove = [columns_to_remove]
    existing_cols = [col for col in columns_to_remove if col in df.columns]
    missing_cols = [col for col in columns_to_remove if col not in df.columns]
    df = df.drop(columns=existing_cols, errors='ignore')
    df.to_csv(output_path, index=False)
    if existing_cols:
        print(f"\n✅ Colunas removidas: {', '.join(existing_cols)}\n")
    if missing_cols:
        print(f"⚠️ As seguintes colunas não estavam no arquivo e foram ignoradas: {', '.join(missing_cols)}")
    print(f"📁 Arquivo salvo em: {output_path}")

# Função para substituir nomes por números
def label_encode_columns(df, columns):
    df_encoded = df.copy()
    mappings = {}

    for col in columns:
        if col in df_encoded.columns:
            unique_values = sorted(df_encoded[col].dropna().unique())
            mapping = {v: i for i, v in enumerate(unique_values)}
            df_encoded[col] = df_encoded[col].map(mapping)
            mappings[col] = mapping
            print(f"\n📦 Mapeamento para '{col}':")
            for k, v in mapping.items():
                print(f"  '{k}' → {v}")
        else:
            print(f"⚠️ Coluna '{col}' não encontrada.")
    
    return df_encoded, mappings

# Função para tratar valores ausentes
def handle_missing_values(df):
    # Separando as colunas numéricas e categóricas
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns  # Colunas numéricas
    cat_cols = df.select_dtypes(include=['object']).columns  # Colunas categóricas
    
    # Imputação para colunas numéricas (usando a média)
    num_imputer = SimpleImputer(strategy='mean')
    df[num_cols] = num_imputer.fit_transform(df[num_cols])
    
    # Imputação para colunas categóricas (usando a moda)
    cat_imputer = SimpleImputer(strategy='most_frequent')
    df[cat_cols] = cat_imputer.fit_transform(df[cat_cols])
    
    return df

# ---------- EXECUÇÃO DE CÓDIGOS ----------

if __name__ == "__main__":
    input_path = r'D:\- PROJETOS\SOFTWARE TCC\test_datasets\pokemon.csv'  # Caminho do arquivo original
    output_path = r'D:\- PROJETOS\SOFTWARE TCC\test_datasets\pokemon_tratado.csv'  # Caminho do arquivo tratado

    # Remover colunas indesejadas
    remove_columns_from_csv(
        input_path=input_path,
        output_path=output_path,
        columns_to_remove=['abilities', 'name', 'japanese_name', 'classfication']
    )

    # Carregar o DataFrame tratado
    df = pd.read_csv(output_path)

    # Tratar valores ausentes
    df_imputed = handle_missing_values(df)

    # Codificar colunas
    df_encoded, map_dict = label_encode_columns(df_imputed, columns=["type1", "type2"])

    # Salvar o DataFrame final
    df_encoded.to_csv(output_path, index=False)

    print("✅ Arquivo final salvo com valores ausentes tratados e colunas codificadas.")
