import time
import numpy as np
import umap.umap_ as umap
from .reducer.reducer import Reducer

class UMAP(Reducer): 
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None):
        super().__init__(
            database=database,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )
        self.algorithm_name = "UMAP"
        self.variance = None

    def process_algorithm(self, features, target):
        try:
            start = time.time()
            reducer = umap.UMAP(n_components=self.dimension)
            x_umap = reducer.fit_transform(features)
            end = time.time()
            self.time = round(end - start, 5)

            explained_variance = np.var(x_umap, axis=0)
            explained_variance_ratio = explained_variance / np.sum(explained_variance)
            self.variance = explained_variance_ratio[0] * 100

            return x_umap
        except Exception as e:
            self.error_message = str(e)
            return None
