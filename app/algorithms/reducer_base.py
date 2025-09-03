from abc import ABC, abstractmethod

class ReducerBase(ABC):
    def __init__(self, params):
        self.params = params
        self.results = {}

    @abstractmethod
    def fit_transform(self, X, y=None):
        """
        All subclasses must implement this method.
        It should run the algorithm and populate self.results.
        """
        pass