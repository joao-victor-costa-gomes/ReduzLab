import time
from sklearn.decomposition import KernelPCA as SklearnKPCA
from .reducer_base import ReducerBase

class KPCA(ReducerBase):
    def fit_transform(self, X, y=None):
        try:
            start_time = time.time()

            n_components = self.params['dimension']
            
            # The 'kernel' parameter is the core of KPCA. 
            kernel = 'linear'

            kpca_instance = SklearnKPCA(
                n_components=n_components,
                kernel=kernel
            )
            
            reduced_data = kpca_instance.fit_transform(X)
            
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None
            
        except Exception as e:
            return None, str(e)