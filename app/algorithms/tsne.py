import time
from sklearn.manifold import TSNE as SklearnTSNE
from .reducer_base import ReducerBase

class TSNE(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the T-SNE algorithm and stores the results.
        """
        try:
            start_time = time.time()

            # Parameters
            n_components = self.params['dimension']

            # Pass all the parameters to the scikit-learn T-SNE object
            tsne_instance = SklearnTSNE(
                n_components=n_components,
            )
            
            reduced_data = tsne_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message