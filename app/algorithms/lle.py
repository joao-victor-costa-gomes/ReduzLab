import time
from sklearn.manifold import LocallyLinearEmbedding as SklearnLLE
from .reducer_base import ReducerBase

class LLE(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the LLE algorithm and stores the results.
        LLE is unsupervised and does not use the target variable 'y'.
        """
        try:
            start_time = time.time()

            lle_params = {
                'n_components': self.params.get('dimension'),
                'n_neighbors': self.params.get('n_neighbors', 10),
                'reg': self.params.get('reg', 1e-3),
                'method': self.params.get('method', 'standard'),
                'eigen_solver': self.params.get('eigen_solver', 'auto'),
                'neighbors_algorithm': self.params.get('neighbors_algorithm', 'auto'),
                'random_state': self.params.get('random_state'),
                'n_jobs': self.params.get('n_jobs')
            }

            # Pass all the parameters to the scikit-learn LLE object
            lle_instance = SklearnLLE(**lle_params)
            
            # Run the algorithm
            reduced_data = lle_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message