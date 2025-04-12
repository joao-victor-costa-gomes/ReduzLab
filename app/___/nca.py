import time 
import numpy as np
from .reducer.reducer import Reducer
from sklearn.neighbors import NeighborhoodComponentsAnalysis as nca_algorithm

class NCA(Reducer):
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "NCA" 
        self.variancia = None 

    def processar_algoritmo(self, features, target):
        inicio = time.time()
        nca = nca_algorithm(n_components=self.dimensao)
        x_nca = nca.fit_transform(X=features, y=target.values.ravel())
        fim = time.time()
        self.tempo = round(fim - inicio, 5)

        explained_variance = np.var(x_nca, axis=0)
        explained_variance_ratio = explained_variance / np.sum(explained_variance)
        self.variancia = explained_variance_ratio[0] * 100

        return x_nca

# Testando funcionamento do algoritmo NCA
if __name__ == "__main__":
    mobile = NCA(
        "NCA-MOBILE-2D",    
        "mobile_devices.csv", 
        1.0,
        ['price_range'],
        2,
        'png',
        False
    )
    mobile.run() 
    print(f"Tempo de processamento: {mobile.tempo}")
    print(f"Variância total: {mobile.variancia}")
