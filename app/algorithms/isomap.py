import time
from sklearn.manifold import Isomap as SklearnIsomap
from .reducer_base import ReducerBase

class Isomap(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the Isomap algorithm and stores the results.
        Isomap is unsupervised and does not use the target variable 'y'.
        """
        try:
            start_time = time.time()

            isomap_params = {
                'n_components': self.params.get('dimension'),
                'n_neighbors': self.params.get('n_neighbors', 10),
                'metric': self.params.get('metric', 'minkowski'),
                'eigen_solver': self.params.get('eigen_solver', 'auto'),
                'path_method': self.params.get('path_method', 'auto'),
                'neighbors_algorithm': self.params.get('neighbors_algorithm', 'auto'),
                'n_jobs': self.params.get('n_jobs')
            }

            # Create the Isomap instance from scikit-learn
            isomap_instance = SklearnIsomap(**isomap_params)
            
            # Run the algorithm
            reduced_data = isomap_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message