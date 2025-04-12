import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from .utils import extract_sample, delete_sample_file, save_plot_image

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

    # 7) Create labels for the graph
    def get_axis_labels(self):
        if self.dimension == 2:
            return [f"{self.algorithm_name}1", f"{self.algorithm_name}2"]
        elif self.dimension == 3:
            return [f"{self.algorithm_name}1", f"{self.algorithm_name}2", f"{self.algorithm_name}3"]


    # 8) Create a plot with the reduced data
    def create_plot(self, df_with_target):
        axis_labels = self.get_axis_labels()

        if self.dimension == 2:
            fig = px.scatter(
                df_with_target,
                x=axis_labels[0],
                y=axis_labels[1],
                title=self.algorithm_name,
                color=self.target
            )
            fig.update_layout(
                xaxis_title_font={"size": 20},
                yaxis_title_font={"size": 20},
                title_font={"size": 24}
            )
            return fig

        elif self.dimension == 3:
            fig = px.scatter_3d(
                df_with_target,
                x=axis_labels[0],
                y=axis_labels[1],
                z=axis_labels[2],
                title=self.algorithm_name,
                color=self.target
            )
            fig.update_layout(
                scene=dict(
                    xaxis_title_font={"size": 18},
                    yaxis_title_font={"size": 18},
                    zaxis_title_font={"size": 18},
                ),
                title_font={"size": 24}
            )
            return fig

        else:
            raise ValueError("Invalid dimension. Only 2D or 3D plots are supported.")


    # 9) It creates the entire graphical representation and save it, basically
    def plot_graph(self, transformed_features, target_series):
        # Creates a DataFrame with the reduced data
        axis_labels = self.get_axis_labels()
        df_reduced = pd.DataFrame(data=transformed_features, columns=axis_labels)
        # Concatenate with targets
        df_with_target = pd.concat([df_reduced, target_series], axis=1)
        # Creates the graph plot
        figure = self.create_plot(df_with_target)
        # Saves the plotted graph
        self.graph_path = save_plot_image(
            figure=figure,
            file_type=self.plot_type,
            name=self.algorithm_name 
        )


    # 10) Runs the entire proccess of data reduction and graph creation
    def run(self):
        features, target = self.preprocess()
        transformed_features = self.process_algorithm(features, target)
        self.plot_graph(transformed_features, target)



