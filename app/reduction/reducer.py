import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from .utils import extract_sample, delete_sample_file

class Reducer:
    def __init__(self, database, sample_rate=1.0, target=None, dimension=None, plot_type=None, scaler=None):
        # Pre-processing values
        self.database = database
        self.sample_rate = sample_rate
        self.sample_path = None
        self.df_sample = None
        self.target = target
        self.features = None
        self.dimension = dimension 
        self.plot_type = plot_type
        self.scaler_type = scaler 
        # Post-processing values
        self.time = None 
        self.graph_path = None
  
    def select_features(self, columns, target):
        return [col for col in columns if col != target]

    def preprocess(self):
        # 1) Create the sample file
        self.sample_path = extract_sample(self.database, self.sample_rate)

        # 2) Load the sample as DataFrame
        self.df_sample = pd.read_csv(self.sample_path)

        # 3) Validate and select features
        if self.target and self.target in self.df_sample.columns:
            self.features = self.select_features(self.df_sample.columns.tolist(), self.target)
        else:
            return None, None

        # 4) Split into X and y
        features = self.df_sample[self.features]
        target = self.df_sample[self.target].astype(str)

        # 5) Delete sample file to save space
        delete_sample_file(self.sample_path)
        self.sample_path = None

        # 6) Apply scaler (if provided)
        if self.scaler_type == "standard":
            scaler = StandardScaler()
            features = scaler.fit_transform(features)
        elif self.scaler_type == "minmax":
            scaler = MinMaxScaler()
            features = scaler.fit_transform(features)

        return features, target

    def get_axis_labels(self):
        if self.dimension == 2:
            return [f"{self.algorithm_name}1", f"{self.algorithm_name}2"]
        elif self.dimension == 3:
            return [f"{self.algorithm_name}1", f"{self.algorithm_name}2", f"{self.algorithm_name}3"]
