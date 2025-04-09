import os
import pandas as pd

def retirar_amostragem(dataset_path, amostragem, nome_saida="amostragem.csv"):
    
    print(f"🔍 Lendo o dataset original: {dataset_path}")
    dataset_completo = pd.read_csv(dataset_path, delimiter=",")
    print(f"✅ Dataset carregado com {len(dataset_completo)} linhas")

    valor_amostragem = int(len(dataset_completo) * amostragem)
    print(f"🎯 Gerando amostragem de {valor_amostragem} linhas ({amostragem*100:.0f}%)")

    amostra = dataset_completo.sample(n=valor_amostragem, random_state=42)

    # Garante que a pasta 'samples' exista
    samples_path = os.path.join("samples")
    if not os.path.exists(samples_path):
        os.makedirs(samples_path)
        print(f"📁 Pasta 'samples/' criada")

    output_path = os.path.join(samples_path, nome_saida)
    amostra.to_csv(output_path, index=False)
    print(f"✅ Amostragem salva em: {output_path}")
    
    return output_path
