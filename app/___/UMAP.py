import time 
import numpy as np
from .reducer.reducer import Reducer
import umap.umap_ as umap 

class UMAP(Reducer): 
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "UMAP"
        self.variancia = None 

    def processar_algoritmo(self, features, target):
        inicio = time.time()

        umap_object = umap.UMAP(n_components=self.dimensao)
        x_umap = umap_object.fit_transform(features)

        fim = time.time()
        self.tempo = round(fim - inicio, 5)

        explained_variance = np.var(x_umap, axis=0)
        explained_variance_ratio = explained_variance / np.sum(explained_variance)
        self.variancia = explained_variance_ratio[0] * 100

        return x_umap

# Testando funcionamento do algoritmo UMAP
if __name__ == "__main__":
    mobile = UMAP(
        "UMAP-MOBILE-2D",    
        "mobile_devices.csv", 
        1.0,
        ['price_range'],
        2,
        'png',
        ""
    )
    mobile.run() 
    print(f"Tempo de processamento: {mobile.tempo}")
    print(f"Variância total: {mobile.variancia}")
