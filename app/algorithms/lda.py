import time
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as SklearnLDA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from .reducer_base import ReducerBase

class LDA(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the LDA algorithm and stores the results.
        LDA is supervised and requires the target variable 'y'.
        """
        try:
            # TRAVA DE SEGURANÇA 1: Requer coluna Target
            if y is None:
                return None, "Erro: LDA é um algoritmo supervisionado e requer uma coluna Target (y) para funcionar."
            
            start_time = time.time()

            lda_params = {
                'n_components': self.params.get('dimension', 2),
                'solver': self.params.get('solver', 'svd'),
                'shrinkage': self.params.get('shrinkage')
            }

            # Pass all the parameters to the scikit-learn LDA object
            lda_instance = SklearnLDA(**lda_params)
            
            # Run the algorithm
            reduced_data = lda_instance.fit_transform(X, y)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time

            # Variância Explicada e Extração de Pesos (Loadings)
            if lda_params['solver'] in ['svd', 'eigen']:
                self.results['explained_variance'] = lda_instance.explained_variance_ratio_.sum() * 100
                
                # EXTRAÇÃO PARA O ARTIGO: Quais variáveis pesam mais em cada eixo?
                if hasattr(lda_instance, 'scalings_'):
                    scalings = lda_instance.scalings_
                    features = X.columns
                    
                    # Top 3 variáveis que mais puxam os pontos no eixo LDA1 (Horizontal)
                    if scalings.shape[1] >= 1:
                        # Pegamos o valor absoluto para ver o impacto (positivo ou negativo)
                        lda1_weights = np.abs(scalings[:, 0])
                        top_lda1_idx = lda1_weights.argsort()[-3:][::-1]
                        self.results['lda1_top'] = ", ".join([f"{features[i]} ({scalings[i, 0]:.2f})" for i in top_lda1_idx])
                    
                    # Top 3 variáveis que mais puxam os pontos no eixo LDA2 (Vertical)
                    if scalings.shape[1] >= 2:
                        lda2_weights = np.abs(scalings[:, 1])
                        top_lda2_idx = lda2_weights.argsort()[-3:][::-1]
                        self.results['lda2_top'] = ", ".join([f"{features[i]} ({scalings[i, 1]:.2f})" for i in top_lda2_idx])
            else:
                self.results['explained_variance'] = 'N/A'

            self.results['reduced_data'] = reduced_data

            if y is not None and len(set(y)) > 1:
                self.results['silhouette_score'] = silhouette_score(reduced_data, y)
                self.results['davies_bouldin'] = davies_bouldin_score(reduced_data, y)
            else:
                self.results['silhouette_score'] = 'N/A'
                self.results['davies_bouldin'] = 'N/A'
            
            return self.results, None 
            
        except Exception as e:
            if "n_components cannot be larger than min(n_features, n_classes - 1)" in str(e):
                dim = self.params.get('dimension', 2)
                return None, f"Erro do LDA: Impossível gerar gráfico em {dim}D. O LDA exige que o número de dimensões seja menor que a quantidade de categorias únicas no seu Target."
            return None, str(e)