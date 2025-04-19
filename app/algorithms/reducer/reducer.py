import os 
import pandas as pd
import plotly.express as px
from flask import current_app
from sklearn.preprocessing import StandardScaler, MinMaxScaler


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


    def extract_sample(self, dataset_path):
        # Reading the dataset and extracting sample
        df = pd.read_csv(dataset_path, delimiter=",")
        sample_size = int(len(df) * self.sample_rate)
        sample = df.sample(n=sample_size, random_state=42)
        # Prepare the output filename
        original_filename = os.path.basename(dataset_path)
        name_without_ext = os.path.splitext(original_filename)[0]
        output_filename = f"{name_without_ext}_sample.csv"
        # Ensure the samples folder exists
        samples_folder = current_app.config['SAMPLES_FOLDER']
        if not os.path.exists(samples_folder):
            os.makedirs(samples_folder)
        output_path = os.path.join(samples_folder, output_filename)
        sample.to_csv(output_path, index=False)
        # Returning sample file path
        return output_path


    def delete_sample_file(self, sample_path):
        if sample_path and os.path.exists(sample_path):
            os.remove(sample_path)
            # print(f"🗑️ Sample file deleted: {sample_path}")
        else:
            # print("⚠️ No sample file to delete or file already removed.")
            pass


    def select_features(self, columns, target):
        return [col for col in columns if col != target]


    def preprocess(self):
        # 1) Create the sample file
        self.sample_path = self.extract_sample(self.database)
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
        self.delete_sample_file(self.sample_path)
        self.sample_path = None
        # 6) Apply scaler (if provided)
        if self.scaler_type == "standard":
            scaler = StandardScaler()
            features = scaler.fit_transform(features)
        elif self.scaler_type == "minmax":
            scaler = MinMaxScaler()
            features = scaler.fit_transform(features)
        # Returning features and target data
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
                # title=self.algorithm_name,
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
                # title=self.algorithm_name,
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


    def save_plot_image(self, figure, file_type, name):
        results_folder = current_app.config['RESULTS_FOLDER']
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        file_name = f"{name.replace(' ', '_')}.{file_type}"
        full_path = os.path.join(results_folder, file_name)

        if file_type == "html":
            figure.write_html(full_path)
        elif file_type == "png":
            figure.write_image(full_path)
        else:
            raise ValueError("File type must be 'html' or 'png'.")
        
        return file_name


    # 9) It creates the entire graphical representation and save it, basically
    def plot_graph(self, transformed_features, target_series):
        # Creates a DataFrame with the reduced data
        axis_labels = self.get_axis_labels()
        df_reduced = pd.DataFrame(data=transformed_features, columns=axis_labels)
        # Concatenate with targets
        df_with_target = pd.concat([df_reduced, target_series], axis=1)
        # Creates the graph plot
        figure = self.create_plot(df_with_target)
        # Uses the same name as the uploaded database
        base_name = os.path.splitext(os.path.basename(self.database))[0]
        unique_name = base_name
        # Saves the plotted graph
        self.graph_path = self.save_plot_image(
            figure=figure,
            file_type=self.plot_type,
            name=unique_name 
        )


    # 10) Runs the entire proccess of data reduction and graph creation
    def run(self):
        features, target = self.preprocess()
        transformed_features = self.process_algorithm(features, target)
        self.plot_graph(transformed_features, target)