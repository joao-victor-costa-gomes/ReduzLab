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
            
            tsne_params = {
                'n_components': self.params.get('dimension'),
                'perplexity': self.params.get('perplexity', 30.0),
                'learning_rate': self.params.get('learning_rate', 'auto'),
                'max_iter': self.params.get('max_iter', 1000),
                'early_exaggeration': self.params.get('early_exaggeration', 12.0),
                'init': self.params.get('init', 'pca'),
                'method': self.params.get('method', 'barnes_hut'),
                'metric': self.params.get('metric', 'euclidean'),
                'random_state': self.params.get('random_state'),
                'n_jobs': self.params.get('n_jobs')
            }

            # Pass all the parameters to the scikit-learn T-SNE object
            tsne_instance = SklearnTSNE(**tsne_params)
            
            reduced_data = tsne_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            self.results['reduced_data'] = reduced_data
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message