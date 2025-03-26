import time 
from .reducer.reducer import Reducer
from sklearn.decomposition import PCA as pca_algorithm

class PCA(Reducer):
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "PCA"
        self.variancia = None 

    def processar_algoritmo(self, features, target):
        inicio = time.time()
        pca = pca_algorithm(n_components=self.dimensao)
        x_pca = pca.fit_transform(features)
        fim = time.time()
        self.tempo = round(fim - inicio, 5)
        self.variancia = pca.explained_variance_ratio_.sum() * 100
        return x_pca

# Testando funcionamento do algoritmo PCA
if __name__ == "__main__":
    mobile = PCA(
        "PCA-MOBILE-2D",    
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
