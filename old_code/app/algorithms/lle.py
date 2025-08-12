import time
import numpy as np
from .reducer.reducer import Reducer
from sklearn.manifold import LocallyLinearEmbedding as lle_algorithm

class LLE(Reducer):
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None):
        super().__init__(
            database=database,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )
        self.algorithm_name = "LLE"
        self.explained_variance = None

    def process_algorithm(self, features, target):
        try:
            start = time.time()
            lle = lle_algorithm(n_components=self.dimension)
            transformed = lle.fit_transform(features)
            end = time.time()
            self.time = round(end - start, 5)

            explained_variance = np.var(transformed, axis=0)
            explained_variance_ratio = explained_variance / np.sum(explained_variance)
            self.explained_variance = round(np.sum(explained_variance_ratio) * 100, 2)

            return transformed
        except Exception as e:
            self.error_message = str(e)
            return None
