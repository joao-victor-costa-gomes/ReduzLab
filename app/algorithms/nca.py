import time
from sklearn.neighbors import NeighborhoodComponentsAnalysis as SklearnNCA
from .reducer_base import ReducerBase

class NCA(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the NCA algorithm and stores the results.
        NCA is supervised and requires the target variable 'y'.
        """
        try:
            start_time = time.time()

            nca_params = {
                'n_components': self.params.get('dimension'),
                'init': self.params.get('init', 'auto'),
                'max_iter': self.params.get('max_iter', 50),
                'tol': self.params.get('tol', 1e-5),
                'random_state': self.params.get('random_state')
            }

            # Pass all the parameters to the scikit-learn NCA object
            nca_instance = SklearnNCA(**nca_params)
            
            # Run the algorithm 
            # NCA requires both X and the target 'y'
            reduced_data = nca_instance.fit_transform(X, y)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message