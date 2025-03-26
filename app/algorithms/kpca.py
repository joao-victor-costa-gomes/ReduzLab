import time 
import numpy as np
from .reducer.reducer import Reducer
from sklearn.decomposition import KernelPCA as kpca_algorithm

# Valores para o kernel = "linear"(padrão), "poly", "rbf", "sigmoid", "cosine", "precomputed"

class KPCA(Reducer):
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, kernel='linear', standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "KPCA"
        self.variancia = None
        self.kernel = kernel 

    def processar_algoritmo(self, features, target):
        inicio = time.time()
        kpca = kpca_algorithm(n_components=self.dimensao, kernel=self.kernel) 
        x_kpca = kpca.fit_transform(features)
        fim = time.time()
        self.tempo = round(fim - inicio, 5)

        explained_variance = np.var(x_kpca, axis=0)
        explained_variance_ratio = explained_variance / np.sum(explained_variance)
        self.variancia = explained_variance_ratio[0] * 100
        
        return x_kpca 

# Testando funcionamento do algoritmo KPCA
if __name__ == "__main__":
    mobile = KPCA(
        "KPCA-MOBILE-2D",    
        "mobile_devices.csv", 
        1.0,
        ['price_range'],
        2,
        'png',
        kernel='poly', 
        standardscaler=False
    )
    mobile.run() 
    print(f"Tempo de processamento: {mobile.tempo}")
    print(f"Variância total: {mobile.variancia}")
