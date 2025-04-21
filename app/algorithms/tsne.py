import time
import numpy as np
from .reducer.reducer import Reducer
from sklearn.manifold import TSNE as tsne_algorithm

class TSNE(Reducer):
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None):
        super().__init__(
            database=database,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )
        self.algorithm_name = "TSNE"
        self.variance_ratio = None  # not standard, but we can estimate

    def process_algorithm(self, features, target):
        try:
            start = time.time()

            # t-SNE does not support more than 3 components
            if self.dimension not in [2, 3]:
                raise ValueError("T-SNE supports only 2 or 3 dimensions.")

            tsne = tsne_algorithm(n_components=self.dimension, random_state=42)
            transformed = tsne.fit_transform(features)

            end = time.time()
            self.time = round(end - start, 5)

            # Estimate "variance" for user feedback (not part of TSNE natively)
            explained_variance = np.var(transformed, axis=0)
            total_variance = np.sum(explained_variance)
            self.variance_ratio = [round(v / total_variance * 100, 2) for v in explained_variance]

            return transformed

        except Exception as e:
            self.error_message = str(e)
            return None
