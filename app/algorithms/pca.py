import time 
from .reducer.reducer import Reducer
from sklearn.decomposition import PCA as pca_algorithm

class PCA(Reducer):
    def __init__(self, database, sample_rate=1.0, target=None, dimension=None, plot_type=None, scaler=None):
        super().__init__(
            database=database,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )
        self.algorithm_name = "PCA"
        self.explained_variance = None 

    def process_algorithm(self, features, target):
        # print("⚙️ Running PCA...")
        start = time.time()
        pca = pca_algorithm(n_components=self.dimension)
        transformed = pca.fit_transform(features)
        end = time.time()
        self.time = round(end - start, 5)
        self.explained_variance = round(pca.explained_variance_ratio_.sum() * 100, 2)
        # print(f"✅ PCA completed in {self.time} seconds.")
        # print(f"🎯 Explained variance: {self.explained_variance}%")

        return transformed
    