import time 
import numpy as np
from .reducer.reducer import Reducer
from sklearn.manifold import LocallyLinearEmbedding as lle_algorithm

class LLE(Reducer): 
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "LLE"
        self.variancia = None 

    def processar_algoritmo(self, features, target):
        inicio = time.time()
        lle = lle_algorithm(n_components=self.dimensao)
        x_lle = lle.fit_transform(features)
        fim = time.time()
        self.tempo = round(fim - inicio, 5)

        explained_variance = np.var(x_lle, axis=0)
        explained_variance_ratio = explained_variance / np.sum(explained_variance)
        self.variancia = explained_variance_ratio[0] * 100

        return x_lle

# Testando funcionamento do algoritmo LLE
if __name__ == "__main__":
    mobile = LLE(
        "LLE-MOBILE-2D",    
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
