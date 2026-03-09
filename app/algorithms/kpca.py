import time
from sklearn.decomposition import KernelPCA as SklearnKPCA
from .reducer_base import ReducerBase

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