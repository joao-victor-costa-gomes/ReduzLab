import time
from sklearn.decomposition import PCA as SklearnPCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from .reducer_base import ReducerBase

class PCA(ReducerBase):
    def fit_transform(self, X, y=None):
        """
        Executes the PCA algorithm and stores the results.
        """
        try:
            start_time = time.time()

            n_components = self.params.get('dimension', 2)
            whiten = self.params.get('whiten', False)
            svd_solver = self.params.get('svd_solver', 'auto')
            random_state = self.params.get('random_state')

            # Pass all the parameters to the scikit-learn PCA object
            pca_instance = SklearnPCA(
                n_components=n_components,
                whiten=whiten,
                svd_solver=svd_solver,
                random_state=random_state
            )
            
            # Run the algorithm
            reduced_data = pca_instance.fit_transform(X)
            
            # --- Store results and metrics ---
            self.results['execution_time'] = time.time() - start_time
            if isinstance(n_components, int) and n_components <= X.shape[1]:
                 self.results['explained_variance'] = pca_instance.explained_variance_ratio_.sum() * 100
            else:
                 self.results['explained_variance'] = 'N/A'
            
            self.results['reduced_data'] = reduced_data

            # --- NOVO CÁLCULO DE MÉTRICAS DE CLUSTERIZAÇÃO ---
            if y is not None and len(set(y)) > 1:
                self.results['silhouette_score'] = silhouette_score(reduced_data, y)
                self.results['davies_bouldin'] = davies_bouldin_score(reduced_data, y)
            else:
                self.results['silhouette_score'] = 'N/A'
                self.results['davies_bouldin'] = 'N/A'
            
            return self.results, None # Return results, no error
            
        except Exception as e:
            return None, str(e) # Return no results, an error message