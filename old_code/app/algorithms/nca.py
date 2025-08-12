import time
import numpy as np
from .reducer.reducer import Reducer
from sklearn.neighbors import NeighborhoodComponentsAnalysis as nca_algorithm

class NCA(Reducer):
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None):
        super().__init__(
            database=database,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )
        self.algorithm_name = "NCA"
        self.variancia = None

    def process_algorithm(self, features, target):
        try:
            start = time.time()
            nca = nca_algorithm(n_components=self.dimension)
            transformed = nca.fit_transform(X=features, y=target.values.ravel())
            end = time.time()
            self.time = round(end - start, 5)

            explained_variance = np.var(transformed, axis=0)
            explained_variance_ratio = explained_variance / np.sum(explained_variance)
            self.variancia = explained_variance_ratio[0] * 100  # opcional
            return transformed

        except Exception as e:
            self.error_message = str(e)
            return None