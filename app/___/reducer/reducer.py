import os 
from . import utils
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Reducer:
    def __init__(self, nome=None, base_dados=None, amostragem=None, target_data=None, dimensao=None, tipo_imagem=None, standardscaler=False):
        # Valores de pré-processamento
        self.nome = nome
        self.base_dados = f"datasets/{base_dados}"
        self.amostragem = amostragem
        self.target_data = target_data #data2
        self.dimensao = dimensao
        self.tipo_imagem = tipo_imagem
        self.standardscaler = standardscaler
        self.nome_algo = None
        # Valores de pós-processamento 
        self.tempo = None  
        self.imagem = None

    def selecionar_features(self, colunas, target):
        return [col for col in colunas if col != target]
    
    def preprocessar_dados(self):
        utils.retirar_amostragem(self.base_dados, self.amostragem)
        # Carregando arquivo CSV da amostragem e definindo vírgula como delimitador dos dados
        dataset = pd.read_csv('datasets/amostragem.csv', delimiter=",")

        features_data = self.selecionar_features(dataset.columns.tolist(), self.target_data[0])

        features = dataset[features_data]              # Valores que serão usados na construção do gráfico
        target = dataset[self.target_data].astype(str) # Valores que serão plotados como pontos no gráfico 
        utils.excluir_arquivo_amostragem()
        # Se o usuário desejar, ele pode aplicar o scaler
        if self.standardscaler == "Standard":
            scaler = StandardScaler()
            features = scaler.fit_transform(features)
        elif self.standardscaler == "MinMax":
            scaler = MinMaxScaler()
            features = scaler.fit_transform(features)
        # Retornando valores para a classe filha
        return features, target

    def numero_colunas(self):
        if self.dimensao == 2:
            return [self.nome_algo+"1", self.nome_algo+"2"]
        elif self.dimensao == 3:
            return [self.nome_algo+"1", self.nome_algo+"2", self.nome_algo+"3"]

    def criar_grafico(self, DF_with_target, target, nome=None):
        # Cria o gráfico com base na dimensão
        if self.dimensao == 2:
            figure = px.scatter(DF_with_target, x=self.nome_algo+"1", y=self.nome_algo+"2", title=self.nome, color=self.target_data[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            return figure 
        elif self.dimensao == 3:
            figure = px.scatter_3d(DF_with_target, x=self.nome_algo+"1", y=self.nome_algo+"2", z=self.nome_algo+"3", title=self.nome, color=self.target_data[0])
            figure.update_layout(xaxis_title_font={"size": 20}, yaxis_title_font={"size": 20}, title_font={"size": 24})
            return figure

    def plotar_grafico(self, transformed_features, target):
        # Criando DataFrame para plotar o gráfico
        DF = pd.DataFrame(data=transformed_features, columns=self.numero_colunas())
        DF_with_target = pd.concat([DF, target], axis=1)
        # Criando gráfico com o algoritmo aplicado
        figure = self.criar_grafico(DF_with_target, target)
        # Baixa imagem na pasta "datasets"
        self.imagem = utils.baixar_imagem(figure, self.tipo_imagem, self.nome, self.imagem)

    def run(self):
        features, target = self.preprocessar_dados()
        transformed_features = self.processar_algoritmo(features, target)
        self.plotar_grafico(transformed_features, target)
