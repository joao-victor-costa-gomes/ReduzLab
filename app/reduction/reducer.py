import pandas as pd

from .utils import extract_sample 

class Reducer:
    def __init__(self, database, sample_rate=1.0, target=None):
        self.database = database              
        self.sample_rate = sample_rate        
        self.sample_path = None              
        self.df_sample = None               
        self.target = target
        self.features = None       

    def select_features(self, columns, target):
        return [col for col in columns if col != target]

    def preprocess(self):
        # 1) Creating the sample file
        self.sample_path = extract_sample(self.database, self.sample_rate)
        
        # 2) Reads the sample file and create a DataFrame
        self.df_sample = pd.read_csv(self.sample_path)

        # 3) Selecting target and features
        if self.target:
            if self.target in self.df_sample.columns:
                self.features = self.select_features(self.df_sample.columns.tolist(), self.target)
            else:
                self.features = None
        else:
            self.features = None
