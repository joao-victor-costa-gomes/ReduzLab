import time
from sklearn.decomposition import PCA as SklearnPCA
from .reducer_base import ReducerBase

class PCA(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the PCA algorithm and stores the results.
        """
        try:
            start_time = time.time()

            # The dimension is taken from the validated params
            pca_instance = SklearnPCA(n_components=self.params['dimension'])
            
            # Run the algorithm
            reduced_data = pca_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['explained_variance'] = pca_instance.explained_variance_ratio_.sum() * 100
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message