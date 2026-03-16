import time
from sklearn.decomposition import KernelPCA as SklearnKPCA
from .reducer_base import ReducerBase
from sklearn.metrics import silhouette_score, davies_bouldin_score

class KPCA(ReducerBase):
    def fit_transform(self, X, y=None):
        try:
            start_time = time.time()

            kpca_params = {
                'n_components': self.params.get('dimension', 2),
                'kernel': self.params.get('kernel', 'linear'),
                'gamma': self.params.get('gamma'),
                'degree': self.params.get('degree', 3),
                'coef0': self.params.get('coef0', 1),
                'eigen_solver': self.params.get('eigen_solver', 'auto'),
                'random_state': self.params.get('random_state'),
                'n_jobs': self.params.get('n_jobs')
            }

            kpca_instance = SklearnKPCA(**kpca_params)
            
            reduced_data = kpca_instance.fit_transform(X)

            # --- NOVO CÁLCULO DE MÉTRICAS DE CLUSTERIZAÇÃO ---
            if y is not None and len(set(y)) > 1:
                self.results['silhouette_score'] = silhouette_score(reduced_data, y)
                self.results['davies_bouldin'] = davies_bouldin_score(reduced_data, y)
            else:
                self.results['silhouette_score'] = 'N/A'
                self.results['davies_bouldin'] = 'N/A'
            
            self.results['execution_time'] = time.time() - start_time

            # NOVA MÉTRICA PARA O ARTIGO: Soma dos Autovalores (Eigenvalues)
            # Retorna a soma se o atributo existir (depende do solver utilizado)
            if hasattr(kpca_instance, 'eigenvalues_') and kpca_instance.eigenvalues_ is not None:
                self.results['eigenvalues_sum'] = float(kpca_instance.eigenvalues_.sum())
            else:
                self.results['eigenvalues_sum'] = 'N/A'

            self.results['reduced_data'] = reduced_data
            
            return self.results, None
            
        except Exception as e:
            return None, str(e)