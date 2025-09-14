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

            n_components = self.params['dimension']

            # Pass all the parameters to the scikit-learn NCA object
            nca_instance = SklearnNCA(
                n_components=n_components
            )
            
            # Run the algorithm 
            # NCA requires both X and the target 'y'
            reduced_data = nca_instance.fit_transform(X, y)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message