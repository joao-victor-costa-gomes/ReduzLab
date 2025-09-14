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

            n_components = self.params['dimension']

            # Pass all the parameters to the scikit-learn PCA object
            pca_instance = SklearnPCA(
                n_components=n_components,
            )
            
            # Run the algorithm
            reduced_data = pca_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            if isinstance(n_components, int) and n_components <= X.shape[1]:
                 self.results['explained_variance'] = pca_instance.explained_variance_ratio_.sum() * 100
            else:
                 self.results['explained_variance'] = 'N/A for selected n_components'
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message