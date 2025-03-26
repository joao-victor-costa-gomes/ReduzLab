import time 
import numpy as np
from .reducer.reducer import Reducer
from sklearn.manifold import TSNE as tsne_algorithm

class TSNE(Reducer):
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "TSNE"
        self.variancia = None 

    def processar_algoritmo(self, features, target):
        inicio = time.time()
        tsne = tsne_algorithm(n_components=self.dimensao)
        x_tsne = tsne.fit_transform(features)
        fim = time.time()
        self.tempo = round(fim - inicio, 5)

        explained_variance = np.var(x_tsne, axis=0)
        explained_variance_ratio = explained_variance / np.sum(explained_variance)
        self.variancia = explained_variance_ratio[0] * 100

        return x_tsne

# Testando funcionamento do algoritmo TSNE
if __name__ == "__main__":
    mobile = TSNE(
        "TSNE-MOBILE-2D",    
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
