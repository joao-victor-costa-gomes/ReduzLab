import time
from .reducer.reducer import Reducer
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda_algorithm

class LDA(Reducer):
    def __init__(self, database, sample_rate, target=None, dimension=None, plot_type=None, scaler=None):
        super().__init__(
            database=database,
            sample_rate=sample_rate,
            target=target,
            dimension=dimension,
            plot_type=plot_type,
            scaler=scaler
        )
        self.algorithm_name = "LDA"
        self.explained_variance = None

    def process_algorithm(self, features, target):
        try:
            start = time.time()
            lda = lda_algorithm(n_components=self.dimension)
            transformed = lda.fit_transform(X=features, y=target.values.ravel())
            end = time.time()
            self.time = round(end - start, 5)
            self.explained_variance = round(lda.explained_variance_ratio_.sum() * 100, 2)
            return transformed
        except Exception as e:
            self.error_message = str(e)
            return None
