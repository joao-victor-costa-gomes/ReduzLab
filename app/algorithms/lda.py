import time
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as SklearnLDA
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
            # Passing both X and the target 'y'
            reduced_data = lda_instance.fit_transform(X, y)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time

            # NOVA MÉTRICA PARA O ARTIGO: Variância Explicada 
            # O LDA só calcula isso quando usa os solvers 'svd' ou 'eigen'
            if lda_params['solver'] in ['svd', 'eigen']:
                self.results['explained_variance'] = lda_instance.explained_variance_ratio_.sum() * 100
            else:
                self.results['explained_variance'] = 'N/A'

            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            # TRAVA DE SEGURANÇA 2: Tratamento amigável para o limite matemático do LDA
            if "n_components cannot be larger than min(n_features, n_classes - 1)" in str(e):
                dim = self.params.get('dimension', 2)
                return None, f"Erro do LDA: Impossível gerar gráfico em {dim}D. O LDA exige que o número de dimensões seja menor que a quantidade de categorias únicas no seu Target."
            return None, str(e) # Return no results, an error message