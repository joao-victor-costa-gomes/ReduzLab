import time 
from .reducer.reducer import Reducer
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda_algorithm

class LDA(Reducer):
    def __init__(self, nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler=False):
        super().__init__(nome, base_dados, amostragem, target_data, dimensao, tipo_imagem, standardscaler)
        self.nome_algo = "LDA"
        self.variancia = None 

    def processar_algoritmo(self, features, target):
        inicio = time.time()
        lda = lda_algorithm(n_components=self.dimensao)
        x_lda = lda.fit_transform(X=features, y=target.values.ravel())
        fim = time.time()
        self.tempo = round(fim - inicio, 5)
        self.variancia = lda.explained_variance_ratio_.sum() * 100
        return x_lda

# Testando funcionamento do algoritmo LDA
if __name__ == "__main__":
    mobile = LDA(
        "LDA-MOBILE-2D",    
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
