import time
import numpy as np
from .reducer.reducer import Reducer
from sklearn.decomposition import KernelPCA as kpca_algorithm

class KPCA(Reducer):
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None, kernel='linear'):
        super().__init__(database, sample_rate, target, dimension, plot_type, scaler)
        self.algorithm_name = "KPCA"
        self.kernel = kernel
        self.variance = None

    def process_algorithm(self, features, target):
        try:
            start = time.time()
            kpca = kpca_algorithm(n_components=self.dimension, kernel=self.kernel)
            transformed = kpca.fit_transform(features)
            end = time.time()
            self.time = round(end - start, 5)
            explained_variance = np.var(transformed, axis=0)
            explained_variance_ratio = explained_variance / np.sum(explained_variance)
            self.variance = round(explained_variance_ratio[0] * 100, 2)
            return transformed
        except Exception as e:
            self.error_message = str(e)
            return None
