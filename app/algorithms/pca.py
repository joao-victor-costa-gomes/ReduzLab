import time 
from .reducer.reducer import Reducer
from sklearn.decomposition import PCA as pca_algorithm

class PCA(Reducer):
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None):
        # All base parameters
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
        try:
            # Start measuring the execution time
            start = time.time()
            pca = pca_algorithm(n_components=self.dimension)
            transformed = pca.fit_transform(features)
            # End time measurement
            end = time.time()
            self.time = round(end - start, 5) # Store the total time of processing (in seconds)
            # Store the total explained variance (e.g., 95.32%)
            self.explained_variance = round(pca.explained_variance_ratio_.sum() * 100, 2)
            # Return the transformed dataset (features in reduced dimensions)
            return transformed    

        except Exception as e:
            # If an error occurs during the algorithm execution, store the message
            self.error_message = str(e)
            return None  
