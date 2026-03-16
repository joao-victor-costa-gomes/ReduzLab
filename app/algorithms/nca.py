import time
from sklearn.neighbors import NeighborhoodComponentsAnalysis as SklearnNCA
from .reducer_base import ReducerBase
from sklearn.metrics import silhouette_score, davies_bouldin_score

class NCA(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the NCA algorithm and stores the results.
        NCA is supervised and requires the target variable 'y'.
        """
        try:
            # TRAVA DE SEGURANÇA: Retorna um erro claro se o front-end não enviar o Target
            if y is None:
                return None, "Erro: NCA é um algoritmo supervisionado e requer uma coluna Target (y) para funcionar."
            start_time = time.time()

            nca_params = {
                'n_components': self.params.get('dimension', 2),
                'init': self.params.get('init', 'auto'),
                'max_iter': self.params.get('max_iter', 50),
                'tol': self.params.get('tol', 1e-5),
                'random_state': self.params.get('random_state')
            }

            # Pass all the parameters to the scikit-learn NCA object
            nca_instance = SklearnNCA(**nca_params)
            
            # Run the algorithm 
            # NCA requires both X and the target 'y'
            reduced_data = nca_instance.fit_transform(X, y)

            # --- NOVO CÁLCULO DE MÉTRICAS DE CLUSTERIZAÇÃO ---
            if y is not None and len(set(y)) > 1:
                self.results['silhouette_score'] = silhouette_score(reduced_data, y)
                self.results['davies_bouldin'] = davies_bouldin_score(reduced_data, y)
            else:
                self.results['silhouette_score'] = 'N/A'
                self.results['davies_bouldin'] = 'N/A'
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message